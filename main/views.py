from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .models import Question, Questionnaire, LikertAnswer, YesNoAnswer, PlainTextAnswer
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .forms import NewUserForm, GroupSelectionForm, QuestionForm, QuestionModelFormSet, SessionForm
from .forms import LikertForm, YesNoForm, PlainTextForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import EmailMessage

# TODO: Add user group checks for relevant functionality (using decorators?)
# TODO: Comment code
# TODO: Create homepage dashboard view
# TODO: Add individual session view
# TODO: Messages on completion of forms

def create_session(request):
    '''View session'''

    if request.method == 'POST':
        session_form = SessionForm(request.POST, request.FILES, current_user=request.user)

        if session_form.is_valid():
            session = session_form.save(commit=False)
            session.tutor = request.user
            session.save()

            return redirect('main:home')

        else:
            return render(request,
                            template_name='main/session_form.html',
                            context={'form':session_form})

    else:
        session_form = SessionForm(current_user=request.user)

        return render(request,
                        template_name='main/session_form.html',
                        context={'form':session_form})

def questionnaire(request, tutor, session_slug, questionnaire_slug):
    '''View questionnaire to fill in'''

    selected_questionnaire = Questionnaire.objects.get(slug=questionnaire_slug,user__username=tutor)
    linked_questions = selected_questionnaire.question_set.all()

    # Get correct answer form based on question category
    answer_forms = []
    for question in linked_questions:
        if question.question_category == 'likert':
            answer_form = LikertForm()
        elif question.question_category == 'yes_no':
            answer_form = YesNoForm()
        elif question.question_category == 'plain_text':
            answer_form = PlainTextForm()

        answer_forms.append(answer_form)

    # Get questions
    question_texts = []
    for each_question in linked_questions:
        question_texts.append(each_question.question)

    # Submitted answers
    if request.method == 'POST':
        raw_post = dict(request.POST)
        answer_list = raw_post['answer']

        # Iterate through responses depending on question category
        i = 0
        for question in linked_questions:
            raw_post['answer'] = answer_list[i]
            if question.question_category == 'likert':
                answer_form = LikertForm(raw_post)
            elif question.question_category == 'yes_no':
                answer_form = YesNoForm(raw_post)
            elif question.question_category == 'plain_text':
                answer_form = PlainTextForm(raw_post)
            i+=1

            print(answer_form)
            # Save and assign extra fields
            if answer_form.is_valid():
                answer = answer_form.save()
                answer.user = request.user
                answer.question = question
                answer.session = Session.objects.get(tutor=tutor, slug=session_slug)
                answer.save()

            else:
                messages.error(request,'Enter a valid response')

        return redirect('main:home')

    else:
        question_and_answer = zip(question_texts,answer_forms)

        return render(request,
                        template_name='main/questionnaire.html',
                        context={'question_and_answer':question_and_answer})

def create_questionnaire(request):
    '''Allow tutors to create new questionnaires.'''

    if request.method == 'POST':
        questionnaire_formset = QuestionModelFormSet(request.POST)

        if questionnaire_formset.is_valid():

            # Create new questionnaire instance and link to newly created questions
            current_number_questionnaires = Questionnaire.objects.filter(user=request.user).count()
            new_questionnaire_name = 'Questionnaire ' + str(current_number_questionnaires+1)
            new_questionnaire = Questionnaire(name=new_questionnaire_name, user=request.user)
            new_questionnaire.save()

            # Iterate through questions and assign to new questionnaire instance
            for form in questionnaire_formset:
                question = form.save()
                question.questionnaire = new_questionnaire
                question.save()

            return redirect('main:home')

        else:
            return render(request,
                            template_name='main/questionnaire_form.html',
                            context={'formset':questionnaire_formset})
    else:
        questionnaire_formset = QuestionModelFormSet(queryset=Question.objects.none())  # queryset set to none for empty formset
        return render(request,
                        template_name='main/questionnaire_form.html',
                        context={'formset':questionnaire_formset})

def home(request):

    if request.user.is_authenticated:
        return render(request = request,
                      template_name='main/home.html',
                      )
    else:
        return redirect('main:login')

# TODO: Create default questionnaire on registering as tutor
def register(request):

    if request.method == "POST":
        user_form = NewUserForm(request.POST)

        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            messages.success(request, f"New Account Created {username}")
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('main:select_group')
        else:
            for msg in user_form.error_messages:
                messages.error(request, f"{msg}: {user_form.error_messages}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"user_form":user_form})


    user_form = NewUserForm()

    return render(request=request,
    template_name='main/register.html',
    context={'user_form':user_form})

def select_group(request):

    user = request.user

    if request.method == 'POST':
        group_form = GroupSelectionForm(request.POST)

        if group_form.is_valid():
            account_type = group_form.cleaned_data.get('account_type')

            if account_type == 'tutor':
                group = Group.objects.get(name='Tutors')
                group.user_set.add(user)
            elif account_type == 'student':
                group = Group.objects.get(name='Students')
                group.user_set.add(user)

            return redirect('main:index')

        else:
            for msg in user_form.error_messages:
                messages.error(request, f"{msg}: {user_form.error_messages}")

            return render(request = request,
                          template_name = "main/group_form.html",
                          context={"group_form":group_form})

    group_form = GroupSelectionForm()
    return render(request = request,
                  template_name = "main/group_form.html",
                  context={'form':group_form})

def logout_request(request):

    logout(request)
    messages.info(request, "Logged out successfully!")

    return redirect("main:home")

def login_request(request):

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            if user is not None:
                messages.success(request, "Logged in successfully!")
                return redirect("main:home")
            else:
                messages.error(request, "Incorrect username or password")

        else:
            messages.error(request, "Incorrect username or password")

    form = AuthenticationForm
    return render(request, "main/login.html", context={"form": form})
