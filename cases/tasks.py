from background_task import background
from lawyers.models import User
from schedules.models import Schedule, MeetingSession


@background(schedule=60)
def notify_user(msg1, msg2, user_id):
    # lookup user by id and send them a message
    user = User.objects.get(pk=user_id)
    user.email_user(msg1, msg2)

    print('sent')


def notify_staff(user_id, msg1, msg2):
    # lookup user by id and send them a message
    user = User.objects.get(pk=user_id)
    user.email_user(msg1, msg2)
    print('sent')


def notify_approve(user_id, msg1, msg2):
    # lookup user by id and send them a message
    user = User.objects.get(pk=user_id)
    user.email_user(msg1, msg2)
    print('sent')


@background
def start_schedule(shedule_id, user_id):
    shedule = MeetingSession.objects.get(id=shedule_id)
    user = User.objects.get(pk=user_id)
    message = 'Dear {}, your session in the {} room will start at {}'.format(
        user.first_name, shedule.room, shedule.start_time)
    user.email_user("Start Session", message)


@background
def end_schedule(shedule_id, user_id):
    shedule = MeetingSession.objects.get(id=shedule_id)
    shedule.expired = True
    shedule.save()
    user = User.objects.get(pk=user_id)
    message = 'Dear {} your session ends at {}'.format(
        user.first_name, shedule.end_time)
    user.email_user("End Session", message)
