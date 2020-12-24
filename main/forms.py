from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question, LikertAnswer, YesNoAnswer, PlainTextAnswer, Questionnaire, Session
from bootstrap_datepicker_plus import DateTimePickerInput


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email","first_name","last_name", "password1", "password2")


class GroupSelectionForm(forms.Form):

    ACCOUNT_CHOICES = (('tutor','Tutor'),('student','Student'))
    account_type = forms.ChoiceField(label='Group',widget=forms.Select(attrs={'class': 'browser-default'}),choices=ACCOUNT_CHOICES)


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('question','question_category')

QuestionModelFormSet = forms.modelformset_factory(model=Question,fields=('question','question_category'),extra=1,
                                                widgets={'question_category':forms.Select(attrs={'class': 'browser-default'})})


class LikertForm(forms.ModelForm):

    class Meta:
        model = LikertAnswer
        fields = ('answer',)
        widgets = {'answer':forms.Select(attrs={'class': 'browser-default'})}
        labels = {'answer':''}

    # FIXME: Change empty label
    # def __init__(self, *args, **kwargs):
    #     super(LikertForm, self).__init__(*args, **kwargs)
    #     self.fields['answer'].empty_label = '(Select option)'


class YesNoForm(forms.ModelForm):

    class Meta:
        model = YesNoAnswer
        fields = ('answer',)
        widgets = {'answer':forms.Select(attrs={'class': 'browser-default'})}
        labels = {'answer':''}


class PlainTextForm(forms.ModelForm):

    class Meta:
        model = PlainTextAnswer
        fields = ('answer',)
        widgets = {'answer':forms.Textarea(attrs={'placeholder':'Write your answer here'})}
        labels = {'answer':''}


class SessionForm(forms.ModelForm):

    class Meta:
        model =  Session
        fields = ('name','start_datetime','end_datetime','type','additional_tutors','questionnaire','resources')
        widgets = {'start_datetime': DateTimePickerInput(),
                    'end_datetime': DateTimePickerInput(),
                    'type':forms.Select(attrs={'class': 'browser-default'}),
                    'additional_tutors':forms.SelectMultiple(attrs={'class': 'browser-default'}),
                    'questionnaire': forms.Select(attrs={'class': 'browser-default'}),
                    'resources': forms.ClearableFileInput(attrs={'multiple': True}),
                    }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user',None)
        super(SessionForm, self).__init__(*args, **kwargs)
        self.fields['questionnaire'].queryset = Questionnaire.objects.filter(user=current_user)
