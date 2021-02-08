from .metrics import Metrics
import numpy as np

class LeftBar:

    def __init__(self,user):

        user_metrics = Metrics(user,time_period_unit='all_time')
        self.all_time_rating = np.nanmean(user_metrics.rating()).astype('int')
        self.total_hours_taught = user_metrics.hours_taught().sum()
