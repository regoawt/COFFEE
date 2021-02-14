from .metrics import Metrics
import numpy as np
from .utils import Utils
from .models import Session

class LeftBar:

    def __init__(self,user,session=None,time_period='all_time'):

        if session == None:
            if time_period == 'all_time':
                self.time_period = 'All time'
            elif time_period == 'week':
                self.time_period = 'Past week'
            elif time_period == 'month':
                self.time_period = 'Past month'
        else:
            self.time_period = 'This session'

        if Utils.is_group(user, 'Tutors'):
            user_metrics = Metrics(user,session=session,time_period_unit=time_period)

            self.rating = user_metrics.rating().average().value
            self.total_hours_taught = user_metrics.hours_taught().value.sum()

        else:
            self.attended_sessions = Session.objects.filter(submitted_questionnaire=user).order_by('-start_datetime').count()
