from background_task import background
from lawyers.models import User


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


def notify_approve(user_id):
    # lookup user by id and send them a message
    user = User.objects.get(pk=user_id)
    user.email_user(msg1, msg2)
    print('sent')
