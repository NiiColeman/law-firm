from django.utils.dateparse import parse_date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
# Create your views here.
from .models import Schedule, Room, MeetingSession
from .forms import ScheduleForm, SessionForm
from cases.tasks import start_schedule, end_schedule
from django.utils import timezone
import datetime
# form django.contrib import messages
from django.contrib import messages
from datetime import date
from django.contrib.auth.decorators import login_required
from datetime import timedelta, time
from django.conf import settings
from django.utils.timezone import make_aware
# from datetime import datetime
# book conference room


@login_required
def schedule_room(request):

    if request.method == "POST":

        start = request.POST.get("start_time")
        end = request.POST.get("end_time")
        purpose = request.POST.get("purpose")
        print(start.strip('T'))
        print(end.strip('T'))
        s1 = start.replace("T", " ")
        e1 = end.replace("T", " ")

        start1 = datetime.datetime.strptime(
            s1, '%Y-%m-%d %H:%M')
        end1 = datetime.datetime.strptime(
            e1, '%Y-%m-%d %H:%M')

        print(end1.month)
        print(purpose)
        start_date = datetime.datetime(
            year=start1.year, month=start1.month, day=start1.day, hour=start1.hour, minute=start1.minute, second=0)
        end_date = datetime.datetime(year=end1.year, month=end1.month,
                                     day=end1.day, hour=end1.hour, minute=end1.minute, second=00)
        print(start_date)
        schedule = Schedule.objects.create(
            user=request.user, start_time=start_date, end_time=end_date, purpose=purpose)
        print('success')
        start_schedule(schedule.id, request.user.id, schedule=start_date)
        end_schedule(schedule.id, request.user.id, schedule=end_date)

        messages.success(
            request, "You have Scheduled to use the Conference Room at {}".format(start_date))
        return redirect('schedules:list')

    else:
        print('failed to schdule room')

    return render(request, 'schedules/add.html')


@login_required
def list_schedules(request):
    schedule_list = Schedule.objects.filter(
        start_time__icontains=datetime.date.today())
    print(schedule_list)
    print(datetime.date.today())

    context = {
        'schedule_list': schedule_list

    }

    return render(request, "schedules/list.html", context)


@login_required
def delete_booking(request, pk):
    sch = get_object_or_404(Schedule, pk=pk)

    if sch:
        sch.delete()

        messages.success(request, "Your Booking has been deleted")
        return redirect('schedules:list')
    else:
        messages.error(request, "Your Booking could not be deleted")
        return redirect('schedules:list')

    return render(request, "schedules/list.html", context)


@login_required
def list_sessions(request):
    # today = datetime.now().date()?
    form = SessionForm()
    today = date.today()
    pink = MeetingSession.objects.filter(room__id=1, start_time__date=today)
    yellow = MeetingSession.objects.filter(room__id=2, start_time__date=today)
    purple = MeetingSession.objects.filter(room__id=3, start_time__date=today)
    start1 = timezone.now()
    # pink_check = False

    if pink:
        for i in pink:
            s1 = i.start_time < start1

        s2 = i.end_time >= start1
        if (s1 and s2):
            request.session['pink_'] = False
        else:
            request.session['pink_'] = True
    else:
        request.session['pink_'] = True

    if yellow:
        for i in yellow:
            s1 = i.start_time < start1

        s2 = i.end_time >= start1
        if (s1 and s2):
            request.session['yellow_'] = False
        else:
            request.session['yellow_'] = True
    else:
        request.session['yellow_'] = True

    if purple:
        for i in purple:
            s1 = i.start_time < start1

        s2 = i.end_time >= start1
        if (s1 and s2):
            request.session['purple_'] = False
        else:
            request.session['purple_'] = True
    else:
        request.session['purple_'] = True

    # print(pink_check)
    # for i in pink:
    #     if start1 in range(i.start_time, i.end_time):
    #         print("this room is currently not available")
    #     else:
    #         print('room is available')

    context = {
        'pink': pink,
        'purple': purple,
        'yellow': yellow,
        'form': form,
        # 'pink_check'
    }

    return render(request, "schedules/meetings.html", context)


@login_required
def add_session(request):
    if request.method == "POST":
        form = SessionForm(request.POST or None)
        if form.is_valid():

            purpose = form.instance.purpose
            room = form.instance.room
            start = request.POST.get("start_time")
            end = request.POST.get("end_time")
            s1 = start.replace("T", " ")
            e1 = end.replace("T", " ")

            start1 = datetime.datetime.strptime(
                s1, '%Y-%m-%d %H:%M')
            end1 = datetime.datetime.strptime(
                e1, '%Y-%m-%d %H:%M')

            settings.TIME_ZONE
            start1 = make_aware(start1)
            end1 = make_aware(end1)

            # print("start time {} - endtime {}".format(start1, end1))
            # print("room {} -- purpose {}" .format(room, purpose))
            # print(type(start1))

            pink = MeetingSession.objects.filter(room__id=1)
            yellow = MeetingSession.objects.filter(room__id=2)
            purple = MeetingSession.objects.filter(room__id=3)

            # object = MeetingSession.objects.create(
            #     purpose=purpose, room=room, start_time=start1, end_time=end1, lawyer=request.user)
            # start_t = MeetingSession.objects.filter(
            #     room=room, start_time__gt=start1, end_time__lt=start1)
            # end_t = MeetingSession.objects.filter(
            #     room=room, start_time__gt=end1, end_time__lt=end1)

            print(start1)
            print(end1)

            # for i in pink:

            #     s1 = i.start_time < start1

            #     s2 = i.end_time >= start1

            #     e1 = i.start_time < end1
            #     e2 = i.end_time >= end1
            #     if (s1 and s2) or (e1 and e2):
            #         print('this room is not available at  this time')
            #     else:
            #         print('good to go !!!!!')

            check = check_availability(
                room, start1, end1)

            print(check)

            if check == True:
                messages.error(
                    request, "The {} room is not availble at this time, please check the list and select another time ".format(room))
                return redirect('schedules:sessions')

            else:
                schedule = MeetingSession.objects.create(
                    room=room, purpose=purpose, start_time=start1, end_time=end1, lawyer=request.user)
                start_schedule(schedule.id, request.user.id, schedule=start1)
        end_schedule(schedule.id, request.user.id, schedule=end1)
        messages.success(
            request, "Booking has been added, your session starts at {}".format(start1))
        return redirect('schedules:sessions')

        #     else:
        #         print('error')
        #         return redirect('schedules:sessions')

    else:
        form = SessionForm

    return render(request, 'schedules/meetings.html', {'form': form})


def check_availability(room, start1, end1):
    room_qs = MeetingSession.objects.filter(room=room)

    for i in room_qs:

        s1 = i.start_time < start1

        s2 = i.end_time >= start1

        e1 = i.start_time < end1
        e2 = i.end_time >= end1
        if (s1 and s2) or (e1 and e2):
            print('this room is not available at  this time')

            return True
        else:
            return False


@login_required
def delete_session(request, pk):
    sch = get_object_or_404(MeetingSession, pk=pk)

    if sch:
        sch.delete()

        messages.success(request, "Your Session has been deleted")
        return redirect('schedules:sessions')
    else:
        messages.error(request, "Your Session could not be deleted")
        return redirect('schedules:sessions')

    return render(request, "schedules/meetings.html", context)
