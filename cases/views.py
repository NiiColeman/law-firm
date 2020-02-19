from django.shortcuts import render, redirect, get_object_or_404
from .models import Case, Category, Status, CaseTask,Appointment,CaseFile
from lawyers.models import Lawyer, OtherStaff, User
# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, DeleteView,DetailView
from .forms import CaseForm,CaseTaskForm,CaseFileForm,CaseArchiveForm
from django.urls import reverse
from accounts.decorators import group_required, groups_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import CaseArchive
from django.utils.crypto import get_random_string

@login_required
def case_list(request):
    form = CaseForm()

    cases = Case.objects.all()
    # completed_cases = Case.objects.select_related('status').filter(status__title == "Complete")
    # pending_cases = Case.objects.select_related('status').filter(status__title == "Pending")

    context = {
        'cases': cases,
        'form': form
        # 'completed_cases': completed_cases,
        # 'pending_cases': pending_cases
    }

    return render(request, 'cases/case.html', context)



@login_required
def pending_list(request):
    form = CaseForm()

    
    # completed_cases = Case.objects.select_related('status').filter(status__title == "Complete")
    # pending_cases = Case.objects.select_related('status').filter(status__title == "Pending")
    pending=Case.objects.select_related('status').filter(status__title="Pending")

    request.session['pending']=pending.count()
    print(pending)

    context = {
      
        'form': form,
        # 'completed_cases': completed_cases,
        'pending': pending
    }

    return render(request, 'cases/pending.html', context)



@login_required
def completed_list(request):
    form = CaseForm()

    
    completed=Case.objects.select_related('status').filter(status__title="Complete")
    # pending=Case.objects.select_related('status').filter(status__title="Pending")
    request.session['completed']=completed.count()
    print(completed)


    context = {
        
        'form': form,
        'completed': completed,
        # 'pending_cases': pending_cases
    }

    return render(request, 'cases/completed.html', context)




@login_required
def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    task_form=CaseTaskForm()
    file_form=CaseFileForm(request.POST or None, request.FILES or None)


    lawyers = case.lawyer.all()
    task_list = CaseTask.objects.filter(case=case)
    print(lawyers)
    form = CaseForm(instance=case)
    case_files=CaseFile.objects.filter(case=case)

    context = {
        'case': case,
        'lawyers': lawyers,
        'form': form,
        'task_list': task_list,
        'task_form':task_form,
        'file_form':file_form,
        'case_files':case_files,

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



def upload_files(request,pk):
    case=get_object_or_404(Case,pk=pk)

    if request.method=="POST":

        file_form=CaseFileForm(request.POST or None, request.FILES or None)
        files=request.FILES.getlist('file')
        if file_form.is_valid():
            for f in files:
                unique_id=get_random_string(length=2)
                case_title="{}".format(f.name)
                new_files=CaseFile.objects.create(case=case,title=case_title,file=f)
                print(f.name)
                print(new_files)



            messages.success(request,"Files have been added")
            return HttpResponseRedirect(reverse('cases:case_detail' , args=[case.pk]))


        else:
                # return HttpResponseRedirect('')
            messages.error(request,"Failed to add Files, please check your form")
            return HttpResponseRedirect(reverse('cases:case_detail' , args=[case.pk]))
    else:
        file_form=CaseFileForm()
        return render(request,"cases/case_detail.html",{'file_form':file_form})


    
        











def new_case(request):
    
    if request.method == "POST":
        form = CaseForm(request.POST or None)
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
            print(form.errors)
            messages.error(
                request, "Oops Something went wrong , please try again")
            return redirect('cases:case_list')
            
    else:
        form = CaseForm()

    return render(request, "cases/new_case.html", {'form': form})

@login_required
def archive_list_view(request):
    archives=CaseArchive.objects.all()

    context={
        'archives':archives
    }


    return render(request,'cases/archives/archives.html',context)


@login_required
def archive_detail_view(request,pk):
    arhcive=get_object_or_404(CaseArchive,pk=pk)
    context={
        'archive':archive
    }

    return render(request,"cases/archives/detail.html",context)

@login_required
def add_to_archives(request,pk):
    case=get_object_or_404(Case,pk=pk)
    if request.method=="POST":
        form=CaseArchiveForm(request.POST or None)
        if form.is_valid():
            staff=get_staff(request.user)
            try:
                archive=CaseArchive.objects.create(case=case,archived_by=staff,archive_location=form.instance.archive_location)
                messages.success(request,"Case Has Already Been Archived")
                return redirect('cases:archive_list')
            except:
                messages.error(request,"Case Has Already Been Archived")
                return redirect('cases:archive_list')
                
           
        else:
            print(form.errors)
            messages.error(request,"Failed to archive case")
        
    else:
        form=CaseArchiveForm()

    return render(request,"cases/archives/add_archive.html",{'form':form})

            


        
            
        
    

def get_staff(user):
    qs=OtherStaff.objects.get(user=user)
    if qs:
        return qs
    else:
        return None





