# Utility functions called in app
from .models import Questionnaire, Question, Session, Answer, LikertAnswer, YesNoAnswer, PlainTextAnswer, FiveScaleAnswer
from django.conf import settings
from datetime import datetime
from plotly.io import to_html
import plotly.graph_objs as go
import numpy as np
import csv

class Utils:

    ANSWER_CLASS_CHOICES = {1:LikertAnswer, 2:YesNoAnswer, 3:PlainTextAnswer, 4:FiveScaleAnswer}
    ANSWER_MAPPING = {1:{1:'Strongly disagree', 2:'Disagree', 3:'Neutral', 4:'Agree', 5:'Strongly agree',},
                    2:{0:'No', 1:'Yes'}}

    def is_group(user, group):
        return user.groups.filter(name=group).exists()

    def get_domain():
        if settings.DEBUG:
            return 'http://192.168.1.123:8000'
        else:
            return'http://www.hone-app.co.uk'

    def get_default_questionnaire():
        question_list = [
                        ['The objectives of this session were met.', 1],
                        ['Please rate your knowledge before the session.', 4],
                        ['Please rate your knowledge after the session.',4],
                        ['Please rate the presentation skills of the instructor.', 4],
                        ["Please rate the instructor's knowledge of the subject.", 4],
                        ['The session was delivered at the appropriate level.', 1],
                        ['The session was delivered in the appropriate teaching environment.', 1],
                        ['What was done well in this session?', 3],
                        ['What could be improved in future sessions?', 3],
                        ['Any other comments:', 3]
                        ]

        return question_list


    def create_default_questionnaire(user):
        default_questionnaire = Questionnaire(name='Default questionnaire', user=user)
        default_questionnaire.save()

        question_list = Utils.get_default_questionnaire()

        # FIXME: Should Question model have user attribute? All questions in default questionnaire will be
        # duplicated for every user. Do get or create first
        for question in question_list:
            question_ = Question(question=question[0], user=user, question_category=question[1])
            question_.save()
            question_.questionnaire.add(default_questionnaire)


    def get_next_session(user):
        future_sessions = Session.objects.filter(tutor=user,start_datetime__gt=datetime.now()).order_by('start_datetime')

        if future_sessions.count() > 0:
            next_session = future_sessions[0]
        else:
            next_session = None

        return next_session


    def get_default_questionnaire_traces(user,metrics):
        question_list = Utils.get_default_questionnaire()
        traces = []
        titles = []
        bar_names = []
        for q in question_list:
            question = Question.objects.get(question=q[0],user=user,questionnaire__name='Default questionnaire')
            if question.question_category != 3:     # Filter out plain text questions
                question_response = metrics.responses(question)
                traces.append(question_response.value)
                titles.append(question_response.title)
                bar_names.append(question_response.bar_names)
        return traces,titles,bar_names


    def get_session_questionnaire_traces(user,metrics,session):
        traces = []
        titles = []
        bar_names = []
        plain_texts = []
        plain_text_titles = []
        for question in Question.objects.filter(questionnaire=session.questionnaire):
            question_response = metrics.responses(question)
            if question.question_category != 3:     # Filter out plain text questions
                traces.append(question_response.value)
                titles.append(question_response.title)
                bar_names.append(question_response.bar_names)
            else:
                plain_texts.append(question_response.value)
                plain_text_titles.append(question_response.title)
        return traces,titles,bar_names,plain_texts,plain_text_titles


    def plotly_multitrace(x,traces,titles,bar_names):
        plots = []
        for i in range(len(traces)):
            plots.append(Utils.plotly_trace(x,traces[i],titles[i],bar_names[i]))

        return plots

    def plotly_trace(x,y,title,bar_name):
        '''Generate HTML for plot of response data for dashboard'''

        y_array = np.array(y)
        fig = go.Figure()

        # Plot as stacked bars against session date for home dashboard
        if np.shape(y)[0] > 1:
            for i in range(np.shape(y)[1]):
                bar_stack_y = y_array[:,i]
                fig.add_trace(go.Bar(name=bar_name[i],x=x,y=bar_stack_y,opacity=0.8))
            fig.update_layout(autosize=True,height=400,barmode='stack')
            fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,font=dict(
            size=10
            )))
        # Normal bar chart for individual session data
        else:
            fig.add_trace(go.Bar(x=bar_name,y=y_array[0],opacity=0.8))
            fig.update_layout(autosize=True,height=400)
        plot_div = to_html(fig,include_plotlyjs=False,full_html=False,config={'displayModeBar': False})

        return plot_div


    def find_plot_id(plot):
        '''Get plot ID from generated plot HTML'''

        start_index = plot.index('=')+2
        end_index = plot.index('class')-2
        id = plot[start_index:end_index]

        return id


    def session_data_to_csv(response, session):
        '''Generate CSV file to download from session responses'''

        questions = Question.objects.filter(questionnaire=session.questionnaire)
        respondents = [answer.user for answer in list(Answer.objects.filter(session=session, question=questions[0]))]
        header_row = ['Question']
        header_row.extend(['Respondent {}'.format(i+1) for i in range(len(respondents))])

        writer = csv.writer(response)
        writer.writerow(header_row)

        for question in questions:
            row = ['{}'.format(question.question)]
            raw_answers = [answer.answer for answer in list(Utils.ANSWER_CLASS_CHOICES[question.question_category].objects.filter(session=session, question=question))]

            # Convert numerical answers to related string for relevant question categories
            if question.question_category == 1 or question.question_category == 2:
                answers = [Utils.ANSWER_MAPPING[question.question_category][answer] for answer in raw_answers]
            else:
                answers = raw_answers
            row.extend(answers)
            writer.writerow(row)

        return response
