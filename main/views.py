from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .forms import NewUserForm, GroupSelectionForm, QuestionForm, QuestionModelFormSet
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import EmailMessage

def generate_questionnaire(request):

    if request.method == 'POST':
        formset = QuestionModelFormSet(request.POST)

        if formset.is_valid():
            formset.save()
            # TODO: Method to automatically assign questionnaire FK
            
            return redirect('main:home')
    else:
        formset = QuestionModelFormSet()
        return render(request,
                        template_name='main/generate_questionnaire.html',
                        context={'formset':formset})

def home(request):

    if request.user.is_authenticated:
        return render(request = request,
                      template_name='main/home.html',
                      )
    else:
        return redirect('main:login')

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

            return redirect('main:group_selection')
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

def group_selection(request):

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
                          template_name = "main/group_selection.html",
                          context={"group_form":group_form})

    group_form = GroupSelectionForm()
    return render(request = request,
                  template_name = "main/group_selection.html",
                  context={"group_form":group_form})

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
