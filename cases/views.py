from django.shortcuts import render, redirect, get_object_or_404
from .models import Case, Category, Status, CaseTask,Appointment
from lawyers.models import Lawyer, OtherStaff, User
# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, DeleteView,DetailView
from .forms import CaseForm,CaseTaskForm
from django.urls import reverse
from accounts.decorators import group_required, groups_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

@login_required
def case_list(request):
    form = CaseForm(request.POST or None)

    cases = Case.objects.all()
    # completed_cases = Case.objects.filter(status__title == "Complete")
    # pending_cases = Case.objects.filter(status__title == "Pending")

    context = {
        'cases': cases,
        'form': form
        # 'completed_cases': completed_cases,
        # 'pending_cases': pending_cases
    }

    return render(request, 'cases/case_list.html', context)

@login_required
def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    task_form=CaseTaskForm()

    lawyers = case.lawyer.all()
    task_list = CaseTask.objects.filter(case=case)
    print(lawyers)
    form = CaseForm(instance=case)

    context = {
        'case': case,
        'lawyers': lawyers,
        'form': form,
        'task_list': task_list,
        'task_form':task_form,
    }

    return render(request, 'cases/case_detail.html', context)


@login_required
def add_case(request):

    if request.method == "POST":
        form = CaseForm(request.POST or None, request.FILES or None)
        # files = request.FILES.getlist('attachments')

        if form.is_valid():
            form.instance.added_by = request.user
            print("this is  {}".format(request.user))
            # for file in files:
            #     Attachment.objects.create(file=file)

            form.save()
            messages.success(request, "Case has been added")
            return redirect('cases:case_list')
        else:
            messages.success(
                request, "Oops Something went wrong , please try again")
    else:
        form = CaseForm()

    return render(request, "cases/add_case.html", {'form': form})



@login_required
def update_case(request, pk):
    case = get_object_or_404(Case, pk=pk)

    if request.method == "POST":
        form = CaseForm(request.POST or None,
                        request.FILES or None, instance=case)
        # files = request.FILES.getlist('attachments')

        if form.is_valid():
            form.instance.user = request.user
            # file_list=[]
            # for file in files:
            #     obj,created=Attachement.objects.get_or_create(file=f)

            form.save()
            messages.success(request, 'the case has been updated')
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.id]))
        else:

            messages.error(request, 'something went horribly wrong')

            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.id]))

    else:
        form = CaseForm(request.POST or None,
                        request.FILES or None, instance=case)

    return render(request, 'cases/case_detail.html', {'form': form})


@login_required
def delete_case(request, pk):
    case = get_object_or_404(Case, pk=pk)

    if request.method == "Post":

        case.delete()
        messages.success(request, 'case has been deleted')
        return redirect('cases:case_list')

    return render(request, 'cases/case_list.html', {'cases': Case.objects.all})






@login_required
def add_task(request,pk):
    case=get_object_or_404(Case,pk=pk)

    if request.method=="POST":
        task_form=CaseTaskForm(request.POST or None)

        if task_form.is_valid():
            task_form.instance.case=case
            task_form.save()
            messages.success(request,"Task has been added")
            return HttpResponseRedirect(reverse('cases:case_detail' , args=[case.pk]))
        else:
            messages.error(request,"Failed to add task, please check your form")
            return HttpResponseRedirect(reverse('cases:case_detail' , args=[case.pk]))
    
    else:
        task_form=CaseTaskForm()

    
    return render(request,"cases/case_detail.html",{'task_form':task_form})
            


class AppointmentCreateView(SuccessMessageMixin, CreateView):
    """Powers a form to create a new appointment"""

    model = Appointment
    fields = ['name', 'phone_number', 'time', 'time_zone']
    success_message = 'Appointment successfully created.'
    template_name='reminders/appointment_form'



class AppointmentListView(ListView):
    """Shows users a list of appointments"""

    model = Appointment
    template_name='reminders/appointment_list'



class AppointmentDetailView(DetailView):
    """Shows users a single appointment"""

    model = Appointment


class AppointmentUpdateView(SuccessMessageMixin, UpdateView):
    """Powers a form to edit existing appointments"""

    model = Appointment
    fields = ['name', 'phone_number', 'time', 'time_zone']
    template_name='reminders/appointment_form'

    success_message = 'Appointment successfully updated.'

class AppointmentDeleteView(DeleteView):
    """Prompts users to confirm deletion of an appointment"""

    model = Appointment
    success_url = reverse_lazy('list_appointments')