from .models import Session, LikertAnswer, YesNoAnswer, FiveScaleAnswer
from .utils import Utils
from datetime import datetime
import numpy as np

class Metrics:
    '''Calculate metrics for given user'''

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


    def na_check(self,metric):
        '''Check if all values in metric array are NaNs'''

        if np.isnan(np.asarray(metric)).all() == True:
            return 'N/A'
        else:
            return metric


    # Define av and sum funcs
    def average(self):
        '''Average of output metric including N/A check'''

        if self.value is not 'N/A':
            self.value = np.nanmean(self.value).astype('int')

        return self

# TODO: AA - add self.title attributes
    def hours_taught(self):

        hours = []
        if self.num_sessions > 0:
            for session in self.sessions:
                session_duration = session.end_datetime - session.start_datetime
                session_duration_hours = session_duration.total_seconds()/3600
                hours.append(session_duration_hours)
        else:
            hours = [0]

        self.value = np.asarray(hours)

        return self


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
            self.value = self.na_check(rating)
        else:
            self.value = 'N/A'

        return self


    def objectives(self):

        objectives_score = []
        if self.num_sessions > 0:
            for session in self.sessions:
                answers = LikertAnswer.objects.filter(session=session,question__question=self.question_list[0][0])
                if answers.count() > 0:
                    score = 0
                    for answer in answers:
                        score += (5-answer.answer)/4

                    objectives_score.append(int(100*score/answers.count()))
                else:
                    objectives_score.append(np.nan)
            self.value = self.na_check(objectives_score)
        else:
            self.value = 'N/A'

        return self


    def effectiveness(self):

        effectiveness_score = []
        if self.num_sessions > 0:
            for session in self.sessions:
                score = 0
                count = 0
                if session.submitted_questionnaire.count() > 0:
                    for user in session.submitted_questionnaire:
                        answer_before = FiveScaleAnswer.objects.get(session=session,question__question=self.question_list[1][0],user=user)
                        answer_after = FiveScaleAnswer.objects.get(session=session,question__question=self.question_list[2][0],user=user)
                        score += (answer_after-answer_before)/5
                        count += 1
                    effectiveness_score.append(int(100*score/count))
                else:
                    effectiveness_score.append(np.nan)
            self.value = self.na_check(effectiveness_score)
        else:
            self.value = 'N/A'

        return self
