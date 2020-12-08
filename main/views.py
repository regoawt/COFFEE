from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm, GroupSelectionForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import EmailMessage

def index(request):

    if request.user.is_authenticated:
        return HttpResponse('Test')
    else:
        return redirect('main:register')

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
