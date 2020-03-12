from background_task import background
from lawyers.models import User
from schedules.models import Schedule


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
def start_schedule(shedule_id, msg, user_id):
    shedule = Schedule.objects.get(id=shedule_id)
    user = User.objects.get(pk=user_id)
    user.email_user(msg)

    print('your schedule has started')


@background
def end_schedule(shedule_id, msg, user_id):
    shedule = Schedule.objects.get(id=shedule_id)
    shedule.expired = True
    shedule.save()
    user = User.objects.get(pk=user_id)
    user.email_user(msg)

    print('your schedule has ended')
