from .models import Session, LikertAnswer, YesNoAnswer, FiveScaleAnswer

class Metrics:
    '''Calculate metrics for given user'''

    def __init__(self,user):
        self.user = user
        self.sessions = Session.objects.filter(tutor=self.user)

    def total_hours_taught(self):

        hours = 0
        for session in self.sessions:
            session_duration = session.end_datetime - session.start_datetime
            session_duration_hours = session_duration.total_seconds()/3600
            hours += session_duration_hours

        return hours

    def rating(self,session):

        fivescale_answers = FiveScaleAnswer.objects.filter(session=session)
        likert_answers = LikertAnswer.objects.filter(session=session)
        yesno_answers = YesNoAnswer.objects.filter(session=session)

        if likert_answers.count() + yesno_answers.count() > 0:
            fivescale_score = 0
            for answer in fivescale_answers:
                fivescale_score += answer.answer/5

            likert_score = 0
            for answer in likert_answers:
                likert_score += (5-answer.answer)/4

            yesno_score = 0
            for answer in yesno_answers:
                yesno_score += answer.answer

            rating = int(100*(fivescale_score + likert_score + yesno_score)/(fivescale_answers.count() + likert_answers.count() + yesno_answers.count()))

        else:
            rating = 'N/A'

        return rating
