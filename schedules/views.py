from django.utils.dateparse import parse_date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
# Create your views here.
from .models import Schedule
from .forms import ScheduleForm
from cases.tasks import start_schedule, end_schedule
from django.utils import timezone
import datetime
# form django.contrib import messages
from django.contrib import messages
from datetime import date


# from datetime import datetime
# book conference room


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
        start_schedule(schedule.id, "Your session has started",



                       request.user.id, schedule=start_date)
        end_schedule(schedule.id, "Your has ended, kindly move out of the meeting room",
                     request.user.id, schedule=end_date)

        messages.success(
            request, "You have Scheduled to use the Conference Room at {}".format(start_date))
        return redirect('schedules:list')

    else:
        print('failed to schdule room')

    return render(request, 'schedules/add.html')


def list_schedules(request):
    schedule_list = Schedule.objects.filter(
        start_time__icontains=datetime.date.today())
    print(schedule_list)
    print(datetime.date.today())

    context = {
        'schedule_list': schedule_list

    }

    return render(request, "schedules/list.html", context)


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
