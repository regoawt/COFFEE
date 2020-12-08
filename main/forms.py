from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email","first_name","last_name", "password1", "password2")

ACCOUNT_CHOICES = (('tutor','Tutor'),('student','Student'))
class GroupSelectionForm(forms.Form):
    account_type = forms.ChoiceField(label='Group',widget=forms.Select(attrs={'class': 'browser-default'}),choices=ACCOUNT_CHOICES)
