# Utility functions called in app
from .models import Questionnaire, Question, Session
from django.conf import settings
from datetime import datetime
from plotly.io import to_html
import plotly.graph_objs as go
import numpy as np

class Utils:

    def is_group(user, group):
        return user.groups.filter(name=group).exists()

    def get_domain():
        if settings.DEBUG:
            return 'http://192.168.1.123'
        else:
            return'http://www.hone-app.co.uk'

    def get_default_questionnaire():
        question_list = [
                        ['How well were the objectives of this session met?', 4],
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


    def plotly_trace(x,y):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x,y=y,opacity=0.8, marker_color='green'))
        fig.update_yaxes(title_text='Hours taught')
        fig.update_layout(autosize=True,height=400)
        plot_div = to_html(fig,include_plotlyjs=False,full_html=False)

        return plot_div


    def find_plot_id(plot):
        start_index = plot.index('=')+2
        end_index = plot.index('class')-2
        id = plot[start_index:end_index]

        return id
