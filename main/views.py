from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User, Group
from .models import Question, Questionnaire, LikertAnswer, YesNoAnswer, PlainTextAnswer, FiveScaleAnswer, Session, Resource
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .forms import NewUserForm, GroupSelectionForm, QuestionForm, QuestionModelFormSet, SessionForm
from .forms import LikertForm, YesNoForm, PlainTextForm, FiveScaleForm, ResourceForm, EmailForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import EmailMessage
from qr_code.qrcode.utils import QRCodeOptions
from .utils import Utils
from datetime import datetime
from .metrics import Metrics
from plotly.io import to_html
import plotly.graph_objs as go
import numpy as np
from .bar import LeftBar

# TODO: Comment code
# TODO: Create homepage dashboard view
# TODO: Messages on completion of forms

def enter_email(request, session_slug):
    '''Enter email to be able to receive link to resources even as anonymous user'''

    session = Session.objects.get(slug=session_slug)
    domain = Utils.get_domain()
    dl_resources_url = '/sessions/{}/download/'.format(session.slug)

    if request.method == 'POST':
        email_form = EmailForm(request.POST)

        if email_form.is_valid():
            address = email_form.cleaned_data.get('email_address')
            subject = 'Link to download resources for {}'.format(session.name)
            body = 'Thank you for completing the questionnaire. Please use the following link to access your resources {}{}'.format(domain,dl_resources_url)
            message = EmailMessage(subject=subject,body=body,to=[address])
            message.send()

            return redirect('main:home')

        else:
            return render(request,
                            template_name='main/enter_email.html',
                            context={'form':email_form})

    else:
        email_form = EmailForm()
        return render(request,
                        template_name='main/enter_email.html',
                        context={'form':email_form})

@login_required
def upload_resources(request, session_slug):
    '''Upload resources'''

    if Utils.is_group(request.user,'Tutors'):
        session = Session.objects.get(slug=session_slug)

        if request.method == 'POST':
            resource_form = ResourceForm(request.POST, request.FILES)
            files = request.FILES.getlist('file')

            if resource_form.is_valid():
                for file in files:
                    resource = Resource(session=session, file=file)
                    resource.save()

                return redirect('main:session', session.slug)

            else:
                return render(request,
                                template_name='main/resource_form.html',
                                context={'form':resource_form})

        else:
            resource_form = ResourceForm()
            return render(request,
                            template_name='main/resource_form.html',
                            context={'form':resource_form})

    else:
        messages.error(request,'Students cannot access this area!')

        return redirect('main:home')


def download_resources(request, session_slug):
    '''Download resources'''

    resources = [resource.file for resource in list(Resource.objects.filter(session__slug=session_slug))]
    return render(request,
                    template_name='main/download_resources.html',
                    context={'resources':resources})

# TODO: Include delete session button in card
@login_required
def sessions(request, session_slug):
    '''View all sessions'''

    domain = Utils.get_domain()
    if Utils.is_group(request.user,'Tutors'):
        if session_slug == 'future':
            sessions = Session.objects.filter(tutor=request.user,start_datetime__gt=datetime.now()).order_by('start_datetime')
        elif session_slug == 'past':
            sessions = Session.objects.filter(tutor=request.user,start_datetime__lt=datetime.now()).order_by('-start_datetime')
        else:
            return session(request, session_slug)


        qr_urls = ['{}/sessions/{}/questionnaire/{}/'.format(domain,session.slug,session.questionnaire.slug) for session in sessions]
        zipped_data = zip(sessions, qr_urls)

        left_bar = LeftBar(request.user)

        return render(request,
                        template_name='main/sessions.html',
                        context={'zipped_data':zipped_data,
                                    'sessions':sessions,
                                    'left_bar':left_bar
                                    })

    else:
        messages.error(request,'Students cannot access this area!')

        return redirect('main:home')


@login_required
def session(request, session_slug):
    '''View session'''

    session = Session.objects.get(slug=session_slug)
    domain = Utils.get_domain()
    dl_resources_url = '/sessions/{}/download/'.format(session.slug)

    if Utils.is_group(request.user, 'Tutors'):
        # FIXME: Case where session.questionnaire is null for qr_url and questionnaire_url
        qr_options = QRCodeOptions(size='l', border=6, error_correction='M')
        qr_url = '{}/sessions/{}/questionnaire/{}/'.format(domain,session.slug,session.questionnaire.slug)
        resource_form_url = '/sessions/{}/upload/'.format(session.slug)
        questionnaire_url = '/sessions/{}/questionnaire/{}/'.format(session.slug, session.questionnaire.slug)
        rating = Metrics(request.user,session=session).rating().mean().astype('int')
        print(rating)

        return render(request,
                        template_name='main/session_tutors.html',
                        context={'session':session,
                                    'qr_options':qr_options,
                                    'qr_url':qr_url,
                                    'resource_form_url':resource_form_url,
                                    'dl_resources_url':dl_resources_url,
                                    'questionnaire_url':questionnaire_url,
                                    'rating':rating})

    else:

        return render(request,
                        template_name='main/session_students.html',
                        context={'session':session,
                                    'dl_resources_url':dl_resources_url})


@login_required
def edit_session(request, session_slug):
    '''Edit session'''

    if Utils.is_group(request.user, 'Tutors'):

        session = Session.objects.get(slug=session_slug)
        if request.method == 'POST':
            session_form = SessionForm(request.POST, instance=session, current_user=request.user)

            if session_form.is_valid():
                session = session_form.save()

                # Redirect to page of newly created session
                return redirect('main:session', session.slug)

            else:
                return render(request,
                                template_name='main/session_form.html',
                                context={'form':session_form})
        else:
            session_form = SessionForm(instance=session, current_user=request.user)
            return render(request,
                            template_name='main/session_form.html',
                            context={'form':session_form})

@login_required
def create_session(request):
    '''Create session'''

    if Utils.is_group(request.user, 'Tutors'):
        if request.method == 'POST':
            session_form = SessionForm(request.POST, request.FILES, current_user=request.user)

            if session_form.is_valid():
                session = session_form.save(commit=False)
                session.tutor = request.user
                session.save()

                # Redirect to page of newly created session
                return redirect('main:session', session.slug)

            else:
                return render(request,
                                template_name='main/session_form.html',
                                context={'form':session_form})

        else:
            session_form = SessionForm(current_user=request.user)

            return render(request,
                            template_name='main/session_form.html',
                            context={'form':session_form})

    else:
        messages.error(request,'Students cannot access this area!')

        return redirect('main:home')


def questionnaire(request, session_slug, questionnaire_slug):
    '''View questionnaire to fill in'''

    selected_questionnaire = Questionnaire.objects.get(slug=questionnaire_slug)
    linked_questions = selected_questionnaire.question_set.all()

    # Get correct answer form based on question category
    answer_forms = []
    for question in linked_questions:
        if question.question_category == 1:
            answer_form = LikertForm()
        elif question.question_category == 2:
            answer_form = YesNoForm()
        elif question.question_category == 3:
            answer_form = PlainTextForm()
        elif question.question_category == 4:
            answer_form = FiveScaleForm()

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
            if question.question_category == 1:
                answer_form = LikertForm(raw_post)
            elif question.question_category == 2:
                answer_form = YesNoForm(raw_post)
            elif question.question_category == 3:
                answer_form = PlainTextForm(raw_post)
            elif question.question_category == 4:
                answer_form = FiveScaleForm(raw_post)
            i+=1

            # Save and assign extra fields
            # BUG: If one answer form is invalid, are all previously saved answers duplicated on second post?
            if answer_form.is_valid():
                answer = answer_form.save()
                if request.user.is_authenticated:
                    answer.user = request.user
                answer.question = question
                answer.session = Session.objects.get(slug=session_slug)
                answer.save()

            else:
                return render(request,
                                template_name='main/questionnaire.html',
                                context={'question_and_answer':question_and_answer})

        if request.user.is_authenticated:
            session = Session.objects.get(slug=session_slug)
            session.submitted_questionnaire.add(request.user)

            return redirect('main:home')
        else:
            return redirect('main:enter_email', session_slug=session_slug)

    else:
        question_and_answer = zip(question_texts,answer_forms)

        return render(request,
                        template_name='main/questionnaire.html',
                        context={'question_and_answer':question_and_answer})


@login_required
def create_questionnaire(request):
    '''Allow tutors to create new questionnaires.'''

    if Utils.is_group(request.user, 'Tutors'):
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

    else:
        messages.error(request,'Students cannot access this area!')

        return redirect('main:home')


@login_required
def home(request):

    if Utils.is_group(request.user, 'Students'):

        attended_sessions = Session.objects.filter(submitted_questionnaire=request.user).order_by('-start_datetime')

        return render(request = request,
                      template_name='main/home_students.html',
                      context={'attended_sessions':attended_sessions})
    else:

        user_metrics = Metrics(request.user,time_period_unit='all_time')
        hours_taught = user_metrics.hours_taught()
        session_dates = user_metrics.session_dates

        left_bar = LeftBar(request.user)

        plot_div = Utils.plotly_trace(session_dates,hours_taught)
        id = Utils.find_plot_id(plot_div)

        domain = Utils.get_domain()
        next_session = Utils.get_next_session(request.user)
        qr_url = '{}/sessions/{}/questionnaire/{}/'.format(domain,next_session.slug,next_session.questionnaire.slug)
        return render(request = request,
                      template_name='main/home_tutors.html',
                      context={'hours_taught':hours_taught,
                                'left_bar':left_bar,
                                'plot_div':plot_div,
                                'plot_id':id,
                                'next_session':next_session,
                                'qr_url':qr_url})


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

            return render(request = request,
                          template_name = "main/register.html",
                          context={"user_form":user_form})

    else:
        user_form = NewUserForm()

        return render(request=request,
        template_name='main/register.html',
        context={'user_form':user_form})


@login_required
def select_group(request):

    user = request.user

    if request.method == 'POST':
        group_form = GroupSelectionForm(request.POST)

        if group_form.is_valid():
            account_type = group_form.cleaned_data.get('account_type')

            if account_type == 'tutor':
                group = Group.objects.get(name='Tutors')
                user.groups.add(group)

                # Create default questionnaire
                Utils.create_default_questionnaire(user)

            elif account_type == 'student':
                group = Group.objects.get(name='Students')
                user.groups.add(group)


            return redirect('main:home')

        else:
            return render(request = request,
                          template_name = "main/group_form.html",
                          context={"group_form":group_form})

    group_form = GroupSelectionForm()
    return render(request = request,
                  template_name = "main/group_form.html",
                  context={'form':group_form})


@login_required
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
