from .metrics import Metrics
import numpy as np

class LeftBar:

    def __init__(self,user,session=None,time_period='all_time'):

        user_metrics = Metrics(user,session=session,time_period_unit=time_period)
        if session == None:
            if time_period == 'all_time':
                self.time_period = 'All time'
            elif time_period == 'week':
                self.time_period = 'Past week'
            elif time_period == 'month':
                self.time_period = 'Past month'
        else:
            self.time_period = 'This session'

        self.rating = user_metrics.rating().average().value
        self.total_hours_taught = user_metrics.hours_taught().value.sum()
