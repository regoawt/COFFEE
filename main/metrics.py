from .models import Session, LikertAnswer, YesNoAnswer, FiveScaleAnswer
from .utils import Utils
from datetime import datetime
import numpy as np

class Metrics:
    '''Calculate metrics for given user'''
# TODO: Pass third argument time period to give the relevant list for self.sessions
    def __init__(self,user,session=None,time_period=1,time_period_unit='week'):
        self.user = user

        # If no session is specified calculate period averages
        if session == None:
            if time_period_unit == 'day':
                time_period_start = datetime.today() - datetime.timedelta(days=time_period)
                self.sessions = Session.objects.filter(tutor=self.user,start_datetime__gt=time_period_start,
                start_datetime__lt=datetime.now())
            elif time_period_unit == 'week':
                time_period_start = datetime.today() - datetime.timedelta(weeks=time_period)
                self.sessions = Session.objects.filter(tutor=self.user,start_datetime__gt=time_period_start,
                start_datetime__lt=datetime.now())
            elif time_period_unit == 'month':
                time_period_start = datetime.today() - datetime.timedelta(days=(time_period*31))
                self.sessions = Session.objects.filter(tutor=self.user,start_datetime__gt=time_period_start,
                start_datetime__lt=datetime.now())
            elif time_period_unit == 'all_time':
                self.sessions = Session.objects.filter(tutor=self.user,start_datetime__lt=datetime.now())
        else:
            self.sessions = [session]

        self.num_sessions = len(self.sessions)
        if self.num_sessions > 0:
            self.session_dates = [session.start_datetime for session in self.sessions]
        else:
            self.session_dates = None
        self.question_list = Utils.get_default_questionnaire()

    def hours_taught(self):

        hours = []
        if self.num_sessions > 0:
            for session in self.sessions:
                session_duration = session.end_datetime - session.start_datetime
                session_duration_hours = session_duration.total_seconds()/3600
                hours.append(session_duration_hours)
        else:
            hours = [0]

        return np.asarray(hours)


    def rating(self):

        rating = []
        if self.num_sessions > 0:
            for session in self.sessions:

                fivescale_answers = FiveScaleAnswer.objects.filter(session=session)
                likert_answers = LikertAnswer.objects.filter(session=session)
                yesno_answers = YesNoAnswer.objects.filter(session=session)

                total_num_answers = likert_answers.count() + yesno_answers.count() + fivescale_answers.count()
                if total_num_answers > 0:
                    fivescale_score = 0
                    for answer in fivescale_answers:
                        fivescale_score += answer.answer/5

                    likert_score = 0
                    for answer in likert_answers:
                        likert_score += (5-answer.answer)/4

                    yesno_score = 0
                    for answer in yesno_answers:
                        yesno_score += answer.answer

                    rating.append(int(100*(fivescale_score + likert_score + yesno_score)/(total_num_answers)))

                else:
                    rating.append(np.nan)
        else:
            rating = [np.nan]
        return np.asarray(rating)


    def objectives_met(self):

        objectives_score = []
        for session in self.sessions:

            answers = FiveScaleAnswer.objects.filter(session=session,question=self.question_list[0][0])
            if answers.count() > 0:
                score = 0
                for answer in answers:
                    score += answer.answer/5

                objectives_score.append(int(100*objectives_score/answers.count()))
            else:
                objectives_score.append(np.nan)

        return np.asarray(objectives_score)
