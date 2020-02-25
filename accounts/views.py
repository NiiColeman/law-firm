from django.shortcuts import render, redirect, get_object_or_404
from lawyers.models import Lawyer, OtherStaff, User
from .forms import UserForm, OtherStaffForm, LawyerForm, OtherStaffForm, UpdateUserForm, UpdateForm, StaffUpdateForm, StaffProfileForm, LawyerProfileForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
# Create your views here.
from django.contrib.auth import update_session_auth_hash

from django.http import HttpResponseRedirect
from django.urls import reverse
from cases.models import Case, Status
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import group_required, groups_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from documents.models import DocumentRecord, Document, DocumentStatus
from cases.forms import CaseForms
from principles.forms import PrinciplesForm


def accounts(request):
    lawyer_form = LawyerForm()
    user_form = UserForm()

    context = {
        'lawyer_form': lawyer_form,
        'user_form': user_form,
    }

    return render(request, 'accounts/signup.html', context)


# def lawyer_profile()

# def lawyer_profile_view(request):

#     if request.method == 'POST':


#         user_form = UserForm(request.POST, prefix='UF')
# 	    profile_form = LawyerForm(request.POST, prefix='PF')

#         if user_form.is_valid() and profile_form.is_valid():

# 		    user = user_form.save(commit=False)
# 			user.save()

# 			user.lawyer_profile.bar_number = profile_form.cleaned_data.get('bar_number')
# 			user.lawyer_profile.lawyer_status = profile_form.cleaned_data.get(
# 			    'lawyer_status')
# 			user.lawyer_profile.save()

# 	    else:
# 		    user_form = UserForm(prefix='UF')
# 		    profile_form =LawyerForm(prefix='PF')

# 	return render(request, 'accounts/signup.html',{
# 			'user_form': user_form,
# 			'lawyer_form': profile_form,
# 		})

def lawyer_profile_view(request):

    if request.method == 'POST':
        user_form = UserForm(request.POST or None)
        lawyer_form = LawyerForm(request.POST or None)

        if user_form.is_valid() and lawyer_form.is_valid():
            user = user_form.save(commit=False)

            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password1')
            email = user_form.cleaned_data.get('email')
            user.set_password(password)
            user.save(commit=True)
            user = authenticate(request, username=email, password=password)

            lawyer = lawyer_form.save(commit=False)

            lawyer.user = user
            lawyer.save()

            # Lawyer.objects.create(user=user.username, bar_number=lawyer_form.instance.bar_number,
            #                       lawyer_status=lawyer_form.instance.lawyer_status)
            # messages.success(request, 'Welcome {} !!'.format(user.username))
            print('success')
            login(request, user)
            return redirect('index')

    else:
        print('error')

        lawyer_form = LawyerForm()
        user_form = UserForm()

    return render(request, 'accounts/signup.html', {'user_form': user_form, 'lawyer_form': lawyer_form})


def lawyer_list(request):
    lawyers = Lawyer.objects.all()
    context = {
        'lawyers': lawyers
    }

    return render(request, 'accounts/lawyers.html', context)


def lawyer_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    lawyer = get_lawyer(user)
    user_form = LawyerProfileForm(request.POST or None, instance=request.user)
    lawyer_form = LawyerForm(request.POST or None, instance=lawyer)
    cases = Case.objects.filter(lawyer=lawyer)
    # cases = Case.objects.select_related('lawyer').filter(lawyer__user=user)
    print(cases)
    pending = Case.objects.filter(lawyer=lawyer, status=get_status(1))
    completed = Case.objects.filter(lawyer=lawyer, status=get_status(2))
    case_form = CaseForms()
    context = {
        'lawyer': lawyer,
        'user_form': user_form,
        'lawyer_form': lawyer_form,
        'cases': cases,
        'pending': pending,
        'completed': completed,
        'form': case_form,
        'p_form': PrinciplesForm(request.POST or None)
    }

    return render(request, 'accounts/lawyer-profile.html', context)


def lawyer_detail(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)

    cases = Case.objects.filter(lawyer=lawyer)
    pending = Case.objects.filter(lawyer=lawyer, status=get_status(1))
    completed = Case.objects.filter(lawyer=lawyer, status=get_status(2))
    user_form = StaffUpdateForm(request.POST or None, instance=lawyer.user)
    lawyer_form = LawyerForm(request.POST or None, instance=lawyer)

    print(cases)
    print(cases.count())
    context = {
        'lawyer': lawyer,
        'cases': cases,
        'pending': pending,
        'completed': completed,
        'user_form': user_form,
        'lawyer_form': lawyer_form
    }

    return render(request, 'accounts/lawyer_detail.html', context)


def other_staff(request):
    staff_list = OtherStaff.objects.all()
    staff_form = OtherStaffForm()
    user_form = UserForm()

    context = {
        'staff_list': staff_list,
        'staff_form': staff_form,
        'user_form': user_form
    }

    return render(request, 'accounts/staff_list.html', context)


def get_status(id):
    qs = Status.objects.get(id=id)
    if qs:
        return qs
    else:
        return None


def update_lawyer_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    lawyer = get_lawyer(user)
    if request.method == 'POST':

        user_form = LawyerProfileForm(
            request.POST or None, request.FILES or None, instance=request.user)
        lawyer_form = LawyerForm(request.POST or None, instance=lawyer)

        if user_form.is_valid() and lawyer_form.is_valid():
            user = user_form.save(commit=False)

            lawyer_form.instance.user = request.user

            user.save()
            lawyer_form.save()
            messages.success(request, "profile has been updated")
            print("success")

            return HttpResponseRedirect(reverse('accounts:lawyer_profile', args=[user.pk]))

        else:
            print("failed")
            return HttpResponseRedirect(reverse('accounts:lawyer_profile', args=[user.pk]))

    else:

        user_form = LawyerProfileForm(
            request.POST or None, instance=request.user)
        lawyer_form = LawyerForm(request.POST or None, instance=lawyer)

    return render(request, "accounts/lawyer-profile.html", {'lawyer_form': lawyer_form, 'user_form': user_form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('logout')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


def add_staff(request):

    if request.method == "POST":
        staff_form = OtherStaffForm(request.POST or None)
        user_form = UserForm(request.POST or None)

        if user_form.is_valid() and staff_form.is_valid():

            user = user_form.save(commit=False)

            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password1')
            email = user_form.cleaned_data.get('email')
            user.set_password(password)

            new_user = User.objects.create(first_name=user_form.instance.first_name, last_name=user_form.instance.last_name,
                                           username=user_form.instance.username, email=email, password=user.password)
            new_user.save(0)

            staff_form.instance.user = new_user
            staff_form.save()
            print('success')
            return redirect('accounts:staff_list')
        else:
            print('failed to add user')
            return redirect('accounts:staff_list')

    else:
        staff_form = OtherStaffForm()
        user_form = UserForm()

    return render(request, "accounts/add_staff.html", {'staff_form': staff_form, 'user_form': user_form})


def staff_details(request, pk):
    staff = get_object_or_404(OtherStaff, pk=pk)
    user_form = StaffUpdateForm(instance=staff.user)
    staff_form = OtherStaffForm(instance=staff)

    doc = Document.objects.filter(added_by=staff.user)
    rec = DocumentRecord.objects.filter(approved_by=staff)
    print(rec)
    not_available = Document.objects.select_related(
        'status').filter(status__title='Not Available')

    context = {
        'staff': staff,
        'user_form': user_form,
        'staff_form': staff_form,
        'rec': rec,
        'doc': doc,
    }

    return render(request, 'accounts/staff_detail.html', context)


def update_staff(request, pk):
    staff = get_object_or_404(OtherStaff, pk=pk)

    if request.method == "POST":
        user_form = StaffUpdateForm(
            request.POST, request.FILES, instance=staff.user)
        staff_form = OtherStaffForm(request.POST or None, instance=staff)

        if user_form.is_valid() and staff_form.is_valid():

            user_form.save()
            staff_form.instance.user = staff.user
            staff.save()

            messages.success(request, 'User has been Updated')

            return HttpResponseRedirect(reverse('accounts:staff_detail', args=[staff.pk]))
        else:
            print(user_form.errors)
            print(staff_form.errors)
            messages.error(request, 'Failed to update user')
            return HttpResponseRedirect(reverse('accounts:staff_detail', args=[staff.pk]))
    else:
        user_form = StaffUpdateForm
        staff_form = OtherStaffForm()

    return renser(request, "accounts/staff_detail.html", {'user_form': user_form, 'staff_form': staff_form})


def staff_detail_view(request, pk):
    staff = get_object_or_404(OtherStaff, pk=pk)
    user_form = StafUpdateForm(request.POST or None, instance=request.user)
    staff_form = OtherStaffForm(request.POST or None, instance=staff)
    doc = Document.objects.filter(added_by=request.user)
    rec = DocumentRecord.objects.select_related(
        'approved_by').filter(approved_by__user=request.user)
    print(rec)
    not_available = Document.objects.select_related(
        'status').filter(status__title='Not Available')

    context = {
        'staff': staff,
        'rec': rec,
        'doc': doc,
        'not_status': not_available,
        'user_form': user_form,
        'staff_form': staff_form
    }

    return render(request, "accounts/staff_profile.html", context)


def update_staff_profile(request, pk):
    staff = get_object_or_404(OtherStaff, pk=pk)

    if request.method == 'POST':

        user_form = StaffProfileForm(
            request.POST or None, instance=request.user)
        staff_form = OtherStaffForm(request.POST or None, instance=staff)

        if user_form.is_valid() and staff_form.is_valid():
            user = user_form.save(commit=False)

            staff_form.instance.user = request.user

            user.save()
            staff_form.save()
            messages.success(request, "profile has been updated")
            print("success")

            return HttpResponseRedirect(reverse('accounts:staff_profile', args=[staff.pk]))

        else:
            print("failed")
            return HttpResponseRedirect(reverse('accounts:staff_profile', args=[staff.staff]))

    else:

        user_form = StaffProfileForm(
            request.POST or None, instance=request.user)
        staff_form = OtherStaffForm(request.POST or None, instance=staff)

    return render(request, "accounts/lawyer-profile.html", {'staff_form': lawyer_form, 'staff_form': user_form})


def update_lawyers_profile(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)

    if request.method == 'POST':

        user_form = StaffUpdateForm(
            request.POST or None, request.FILES or None, instance=lawyer.user)
        lawyer_form = LawyerForm(request.POST or None, instance=lawyer)

        if user_form.is_valid() and lawyer_form.is_valid():

            user_form.save()
            print(user_form.errors)
            # lawyer_form.instance.user=request.user

            lawyer_form.save()
            messages.success(request, "profile has been updated")

            return HttpResponseRedirect(reverse('accounts:lawyer_detail', args=[lawyer.pk]))

        else:
            print("failed")

            print(lawyer_form.errors)
            print(user_form.errors)

            return HttpResponseRedirect(reverse('accounts:lawyer_detail', args=[lawyer.pk]))

    else:

        user_form = StaffUpdateForm(
            request.POST or None, instance=request.user)
        staff_form = OtherStaffForm(request.POST or None, instance=staff)

    return render(request, "accounts/lawyer-profile.html", {'lawyer_form': lawyer_form, 'user_form': user_form})


def get_lawyer(user):
    lawyer = Lawyer.objects.get(user=user)
    if lawyer:
        return lawyer
    else:
        return None


def delete_lawyer(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)
    if request.method == "POST":
        lawyer.delete()
        messages.success(request, "Lawyer has been deleted")

        return redirect("accounts:lawyer_list")

    return render(redirect, "accounts/lawyer.html")


def delete_staff(request, pk):
    staff = get_object_or_404(staff, pk=pk)
    if request.method == "POST":
        lawyer.delete()
        messages.success(request, "Staff has been deleted")

        return redirect("accounts:staff_list")

    return render(redirect, "accounts/staff_list.html")
