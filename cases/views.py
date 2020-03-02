from django.shortcuts import render, redirect, get_object_or_404
from .models import Case, Category, Status, CaseTask, Appointment, CaseFile, LegalArgument
from lawyers.models import Lawyer, OtherStaff, User
# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .forms import CaseForm, CaseTaskForm, CaseFileForm, CaseArchiveForm, CaseForms, CategoryForm, LegalArgumentForm
from django.urls import reverse
from accounts.decorators import group_required, groups_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import CaseArchive
from django.utils.crypto import get_random_string
from .tasks import notify_user
from django.core.paginator import Paginator
from .filters import CaseFilter
# @login_required
# def case_list(request):
#     form = CaseForm()

#     cases = Case.objects.all()
# completed_cases = Case.objects.select_related('status').filter(status__title == "Complete")
# pending_cases = Case.objects.select_related('status').filter(status__title == "Pending")

# context = {
#     'cases': cases,
#     'form': form
# 'completed_cases': completed_cases,
# 'pending_cases': pending_cases
# }

# return render(request, 'cases/case.html', context)


@login_required
def pending_list(request):
    form = CaseForms()

    # completed_cases = Case.objects.select_related('status').filter(status__title == "Complete")
    # pending_cases = Case.objects.select_related('status').filter(status__title == "Pending")
    pending = Case.objects.select_related(
        'status').filter(status__title="Pending")

    request.session['pending'] = pending.count()
    print(pending)

    context = {

        'form': form,
        # 'completed_cases': completed_cases,
        'pending': pending
    }

    return render(request, 'cases/pending.html', context)


@login_required
def completed_list(request):
    form = CaseForms()

    completed = Case.objects.select_related(
        'status').filter(status__title="Complete")
    # pending=Case.objects.select_related('status').filter(status__title="Pending")
    request.session['completed'] = completed.count()
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
    task_form = CaseTaskForm()
    file_form = CaseFileForm(request.POST or None, request.FILES or None)
    arguments = LegalArgument.objects.filter(case=case)[:4]

    lawyers = case.lawyer.all()
# print(case.lawyer_set.user)
    task_list = CaseTask.objects.filter(case=case)[:5]
    # print(lawyers)
    form = CaseForm(instance=case)
    case_files = CaseFile.objects.filter(case=case)[:5]
    # user = lawyer.user.all()
    users = []
    for lawyer in lawyers:
        users.append(lawyer.user)
    print(arguments)

    print(users)

    context = {
        'case': case,
        'lawyers': lawyers,
        'form': form,
        'task_list': task_list,
        'task_form': task_form,
        'file_form': file_form,
        'case_files': case_files,
        'users': users,
        'arg_form': LegalArgumentForm(request.POST or None),
        'arguments': arguments

    }

    return render(request, 'cases/case_detail.html', context)


@login_required
def add_case(request):

    if request.method == "POST":
        form = CaseForms(request.POST or None, request.FILES or None)
        # files = request.FILES.getlist('attachments')

        if form.is_valid():
            form.instance.added_by = request.user
            # print("this is  {}".format(request.user))
            # for file in files:
            #     Attachment.objects.create(file=file)
            # case = Case()
            # case.name = form.instance.name
            # case.description = form.instance.description
            # case.status = get_status(form.instance.status)

            # case.lawyer = form.instance.lawyer
            # case.date_added = form.instance.date_added
            # case.added_by = request.user
            # case.court = form.instance.court
            # case.save()
            form.save()

            messages.success(request, "Case has been added")
            return redirect('cases:case_list')

        else:
            messages.success(
                request, "Oops Something went wrong , please try again")
    else:
        form = CaseForms()

    return render(request, "cases/case_list", {'form': form})


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

    return render(request, 'cases/case_list_view.html', {'cases': Case.objects.all})


@login_required
def add_task(request, pk):
    case = get_object_or_404(Case, pk=pk)

    if request.method == "POST":
        task_form = CaseTaskForm(request.POST or None)

        if task_form.is_valid():

            task_form.instance.case = case
            task_form.save()

            lawyers = case.lawyer.all()
            print(lawyers)

            for l in lawyers:
                msg1 = "NEW TASK : {} !!".format(task_form.instance.task)
                msg2 = "Dear {}, you have a task scheduled for {}.Remember to check your mail for further notifcations".format(
                    l.user,  task_form.instance.deadline)
                notify_user(msg1, msg2, l.user.id, repeat=300,
                            repeat_until=task_form.instance.deadline)

            messages.success(request, "Task has been added")
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))
        else:
            messages.error(
                request, "Failed to add task, please check your form")
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

    else:
        task_form = CaseTaskForm()

    return render(request, "cases/case_detail.html", {'task_form': task_form})


class AppointmentCreateView(SuccessMessageMixin, CreateView):
    """Powers a form to create a new appointment"""

    model = Appointment
    fields = ['name', 'phone_number', 'time', 'time_zone']
    success_message = 'Appointment successfully created.'
    template_name = 'reminders/appointment_form'


class AppointmentListView(ListView):
    """Shows users a list of appointments"""

    model = Appointment
    template_name = 'reminders/appointment_list'


class AppointmentDetailView(DetailView):
    """Shows users a single appointment"""

    model = Appointment


class AppointmentUpdateView(SuccessMessageMixin, UpdateView):
    """Powers a form to edit existing appointments"""

    model = Appointment
    fields = ['name', 'phone_number', 'time', 'time_zone']
    template_name = 'reminders/appointment_form'

    success_message = 'Appointment successfully updated.'


class AppointmentDeleteView(DeleteView):
    """Prompts users to confirm deletion of an appointment"""

    model = Appointment
    success_url = reverse_lazy('list_appointments')


def upload_files(request, pk):
    case = get_object_or_404(Case, pk=pk)

    if request.method == "POST":

        file_form = CaseFileForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('file')
        if file_form.is_valid():
            for f in files:
                unique_id = get_random_string(length=2)
                case_title = "{}".format(f.name)
                new_files = CaseFile.objects.create(
                    case=case, title=case_title, file=f)
                print(f.name)
                print(new_files)

            messages.success(request, "Files have been added")
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

        else:
                # return HttpResponseRedirect('')
            messages.error(
                request, "Failed to add Files, please check your form")
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))
    else:
        file_form = CaseFileForm()
        return render(request, "cases/case_detail.html", {'file_form': file_form})


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
    archives = CaseArchive.objects.all()

    context = {
        'archives': archives
    }

    return render(request, 'cases/archives/archives.html', context)


@login_required
def archive_detail_view(request, pk):
    archive = get_object_or_404(CaseArchive, pk=pk)
    case = archive.case
    task_form = CaseTaskForm()
    file_form = CaseFileForm(request.POST or None, request.FILES or None)
    arguments = LegalArgument.objects.filter(case=case)

    lawyers = case.lawyer.all()
# print(case.lawyer_set.user)
    task_list = CaseTask.objects.filter(case=case)[:5]
    # print(lawyers)
    form = CaseForm(instance=case)
    case_files = CaseFile.objects.filter(case=case)[:5]
    users = []
    for lawyer in lawyers:
        users.append(lawyer.user)
    context = {
        'case': case,
        'archive': archive,
        'lawyers': lawyers,
        'form': form,
        'task_list': task_list,
        'task_form': task_form,
        'file_form': file_form,
        'case_files': case_files,
        'users': users,
        'arg_form': LegalArgumentForm(request.POST or None),
        'arguments': arguments
    }

    return render(request, "cases/archives/detail.html", context)


@login_required
def add_to_archives(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == "POST":
        form = CaseArchiveForm(request.POST or None)
        if form.is_valid():
            staff = get_staff(request.user)
            try:
                archive = CaseArchive.objects.create(
                    case=case, archived_by=staff, archive_location=form.instance.archive_location)
                messages.success(request, "Case Has Already Been Archived")
                return redirect('cases:archive_list')
            except:
                messages.error(request, "Case Has Already Been Archived")
                return redirect('cases:archive_list')

        else:
            print(form.errors)
            messages.error(request, "Failed to archive case")

    else:
        form = CaseArchiveForm()

    return render(request, "cases/archives/add_archive.html", {'form': form})


def get_staff(user):
    qs = OtherStaff.objects.get(user=user)
    if qs:
        return qs
    else:
        return None


class CaseCreateView(CreateView):
    # model = Case
    template_name = "cases/add_case.html"
    form_class = CaseForms()

    def form_valid(self):
        self.form.instance.added_by = request.user
        self.form.save()

        messages.success(self.request, "Case has been added")


class CaseList(ListView):
    model = Case
    template_name = "cases/case_list_view.html"

    def get_context_data(self, **kwargs):
        context = super(CaseList, self).get_context_data(**kwargs)
        context['form'] = CaseForms(self.request.POST or None)
        return context


def get_status(status):

    qs = Status.objects.filter(title=status)
    if qs[0]:
        return
    else:
        return None


class CategoryListView(ListView):
    model = Category
    template_name = "cases/category/cat_list.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['form'] = CategoryForm(self.request.POST or None)
        return context


# class CategoryCreateView(CreateView):
#     form_class = CategoryForm
#     template_name = "cases/category/add.html"
    # success_url = reverse('cases:cat_list')

    # def form_valid(self, form):

    #     self.form.save()
    #     messages.success(self.request, "Category has been added")
    #     return redirect('cases:cat_list.html')


# class CategoryUpdateView(UpdateView):
#     # model = Category
#     form_class = CategoryForm
#     success_url = 'cases:cat_list'

#     template_name = "cases/category/add.html"

#     # def form_valid(self, object):

#     #     self.form.save()
#     #     messages.success(self.request, "Category has been updated")
#     #     return redirect('cases:cat_list.html')

@login_required
def cat_update(request, pk):
    cat = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, "Category has been updated")
            return HttpResponseRedirect(reverse('cases:cat_list'))

        else:
            messages.error(request, "Category was not updated")
            # return redirect('cases:cat_list.html')
            return HttpResponseRedirect(reverse('cases:cat_list'))

    else:
        form = CategoryForm()

    return render(request, "cases/category/delete.html")


@login_required
def cat_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category has been added")
            return redirect('cases:cat_list')

        else:
            messages.error(request, "Category was not added")
            return redirect('cases:cat_list')

    else:
        form = CategoryForm()

    return render(request, "cases/category/delete.html")


@login_required
def delete_cat(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        cat.delete()
        messages.success(request, "Category has been deleted")
        return redirect('cases:cat_list')

    return render(request, "cases/category/delete.html")


@login_required
def add_argument(request, pk):
    case = get_object_or_404(Case, pk=pk)

    if request.method == "POST":
        arg_form = LegalArgumentForm(request.POST or None)

        if arg_form.is_valid():
            arg_form.instance.case = case
            # if not get_arg(arg_form.instance.argument):

            arg_form.save()
            messages.success(request, " Legal Argument has been added")
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

            #
        else:
            messages.error(request, "Please check your form for errors")
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

    else:
        arg_form = LegalArgumentForm()

    return render(request, "cases/case_detail.html", {'arg_form': arg_form})


def get_arg(arg):
    qs = LegalArgument.objects.get(argument=arg)
    if qs:
        return True
    else:
        return False


@login_required
def cat_detail(request, pk):
    cat = get_object_or_404(Category, pk=pk)

    context = {
        'cat': cat,
        'cat_form': CategoryForm(request.POST or None, instance=cat)
    }

    return render(request, 'cases/category/detail.html', context)


def file_list(request, pk):
    case = get_object_or_404(Case, pk=pk)

    file_list = CaseFile.objects.filter(case=case)
    context = {
        'case': case,
        'file_list': file_list,
        'file_form': CaseFileForm(request.POST or None, request.FILES or None)

    }

    return render(request, 'cases/file_list.html', context)


def delete_files(request, pk):
    file = get_object_or_404(CaseFile, pk=pk)
    case = file.case
    if request.method == "POST":
        file.delete()
        messages.success(request, "File Has Been Deleted")
        return HttpResponseRedirect(reverse('cases:file_list', args=[case.pk]))

    return render(request, "cases/file_list.html")


def task_view(request, pk):
    case = get_object_or_404(Case, pk=pk)

    tasks = CaseTask.objects.filter(case=case)
    task_list = CaseTask.objects.filter(case=case)

    paginator = Paginator(task_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    task_form = CaseTaskForm(request.POST or None)
    context = {

        'tasks': tasks,
        'page_obj': page_obj,
        'case': case,
        'task_form': task_form

    }

    return render(request, "cases/task_list.html", context)

# def task_list_view


def task_list_view(request, pk):
    case = get_object_or_404(Case, pk=pk)

    tasks = CaseTask.objects.filter(case=case)
    task_list = CaseTask.objects.filter(case=case)

    paginator = Paginator(task_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    task_form = CaseTaskForm(request.POST or None)
    context = {

        'tasks': tasks,
        'page_obj': page_obj,
        'task_form': task_form,
        'case': case,

    }

    return render(request, "cases/list_tasks.html", context)


def completed(request, pk):

    task = get_object_or_404(CaseTask, pk=pk)
    case = task.case

    if task.complete == False:
        task.complete = True
        task.save()

        messages.success(request, "Task has been completed")
        return HttpResponseRedirect(reverse('cases:list_tasks', args=[case.pk]))

    else:
        task.complete = False
        task.save()
        messages.success(request, "Task has been  masrked as pending")

        return HttpResponseRedirect(reverse('cases:list_tasks', args=[case.pk]))

    return render(request, "cases/list_tasks.html", context)


def delete_task(request, pk):
    task = get_object_or_404(CaseTask, pk=pk)
    case = task.case
    if task:
        task.delete()
        messages.success(request, "Task has been deleted")
        return HttpResponseRedirect(reverse('cases:list_tasks', args=[case.pk]))

    return render(request, "cases/list_tasks.html", context)


def argument_list(request, pk):
    case = get_object_or_404(Case, pk=pk)
    argument_list = LegalArgument.objects.filter(case=case)

    context = {
        'form': LegalArgumentForm(request.POST or None),
        'argument_list': argument_list,
        'case': case
    }

    return render(request, 'cases/arg_list.html', context)


def argument_detail(request, pk):
    arg = get_object_or_404(LegalArgument, pk=pk)
    case = arg.case
    context = {
        'arg': arg,
        'case': case,
        'form': LegalArgumentForm(request.POST or None, instance=arg)
    }

    return render(request, "cases/arg_detail.html", context)


def arg_update(request, pk):
    arg = get_object_or_404(LegalArgument, pk=pk)
    if request.method == "POST":
        form = LegalArgumentForm(request.POST or None, instance=arg)
        if form.is_valid():
            form.save()
            messages.success(request, "Argument has Been Updated")
            return HttpResponseRedirect(reverse('cases:argument_detail', args=[arg.pk]))

        else:
            messages.error(request, "Argument could not be updated")
            return HttpResponseRedirect(reverse('cases:argument_detail', args=[arg.pk]))

    else:
        form = LegalArgumentForm()

    return render(request, 'cases/arg_detail.html', {'form': form, 'case': arg.case})


def arg_delete(request, pk):
    arg = get_object_or_404(LegalArgument, pk=pk)
    case = arg.case

    if arg:
        arg.delete()
        messages.success(request, "Argument has Been Deleted")
        return HttpResponseRedirect(reverse('cases:argument_list', args=[case.pk]))
    else:
        messages.error(request, "Argument could not be deleted")
        return HttpResponseRedirect(reverse('cases:argument_detail', args=[arg.pk]))

    return render(request, 'cases/arg_detail.html')


def case_filter(request):
    f = CaseFilter(request.GET, queryset=Case.objects.all())
    return render(request, 'cases/filter.html', {'filter': f})


