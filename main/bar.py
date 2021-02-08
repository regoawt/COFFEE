from .metrics import Metrics
import numpy as np

class LeftBar:

    def __init__(self,user):

        user_metrics = Metrics(user,time_period_unit='all_time')
        if np.isnan(user_metrics.rating()).all() == True:
            self.all_time_rating = 'N/A'
        else:
            self.all_time_rating = np.nanmean(user_metrics.rating()).astype('int')
        self.total_hours_taught = user_metrics.hours_taught().sum()
