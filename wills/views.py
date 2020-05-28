from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Will, Agreement, AgreementCategory
from .forms import WillForm, AgreementForm, AgreementCategoryForm
from django.urls import reverse
# Create your views here.
from .models import models
from .forms import WillForm
from django.contrib.auth.decorators import login_required

@login_required()
def will_list(request):
    wills = Will.objects.filter(lawyer__user=request.user)
    form = WillForm(request.POST or None)

    context = {
        'wills': wills,
        'form': form
    }
    return render(request, 'wills/list.html', context)

@login_required
def will_detail(request, pk):
    will = get_object_or_404(Will, pk=pk)
    form = WillForm(request.POST or None, instance=will)
    lawyers=will.lawyer.all()
    context = {
        'will': will,
        'form': form,
        'lawyers':lawyers
    }

    return render(request, 'wills/detail.html', context)

@login_required
def will_update(request, pk):
    will = get_object_or_404(Will, pk=pk)

    if request.method == "POST":
        form = WillForm(request.POST or None, instance=will)
        if form.is_valid():

            form.save()
            messages.success(request, "Will Has been updated")

            return HttpResponseRedirect(reverse('wills:details', args=[will.id]))

        else:
            messages.error(
                request, "Failed to update will, please check the form")
            return HttpResponseRedirect(reverse('wills:details', args=[will.id]))

    else:
        form = WillForm()

    context = {
        'will': will,
        'form': form
    }

    return render(request, 'wills/detail.html', context)

@login_required
def add_will(request):

    if request.method == "POST":
        form = WillForm(request.POST or None)
        if form.is_valid():


            form.save()

            messages.success(request, "will has been added")
            return redirect('wills:will_list')
        else:
            messages.error(request, "failed to add will")
            return redirect('wills:will_list')

    else:
        form = WillForm()

    return render(request, 'wills/list.html', {'form': form})

@login_required
def delete_will(request, pk):
    will = get_object_or_404(Will, pk=pk)

    if request.method == "POST":
        will.delete()
        messages.success(request, "Will Has been deleted")
        return redirect('wills:will_list')
    else:
        messages.error(request, "Willcould not deleted")
        return HttpResponseRedirect(reverse('wills:detail', args=[will.pk]))

    return render(request, 'wills/detail.html')

@login_required
def agreement_list(request):
    object_list = Agreement.objects.filter(lawyer__user=request.user)
    form = AgreementForm(request.POST or None)

    context = {
        'object_list': object_list,
        'form': form
    }

    return render(request, 'wills/agreements/list.html', context)

@login_required
def add_agreement(request):
    if request.method == "POST":
        form = AgreementForm(request.POST or None)
        if form.is_valid():

            form.save()
            messages.success(request, "Agreement has been added")
            return redirect('wills:agreement_list')
        else:
            messages.error(
                request, "failed to add new agreement, please check the form")
            return redirect('wills:agreement_list')
    else:
        form = AgreementForm()

    return render(request, "wills/agreements/list.html", {'form': form})

@login_required
def agreement_detail(request, pk):
    object = get_object_or_404(Agreement, pk=pk)
    form = AgreementForm(request.POST or None, instance=object)
    lawyers=object.lawyer.all()

    context = {
        'agreement': object,
        'form': form,
        'lawyers':lawyers
    }

    return render(request, 'wills/agreements/detail.html', context)

@login_required
def agreement_update(request, pk):
    object = get_object_or_404(Agreement, pk=pk)
    if request.method == "POST":
        form = AgreementForm(request.POST or None, instance=object)
        if form.is_valid():

            form.save()
            messages.success(request, "Agreement has been updated")
            return HttpResponseRedirect(reverse('wills:agreement_detail', args=[object.pk]))
        else:
            messages.error(request, "Agreement could not be updated")
            return HttpResponseRedirect(reverse('wills:agreement_detail', args=[object.pk]))

    else:
        form = AgreementForm()

    return render(request, 'wills/agreements/detail.html', {'form': form})

@login_required
def delete_agreement(request, pk):
    object = get_object_or_404(Agreement, pk=pk)

    if request.method == "POST":
        object.delete()
        messages.success(request, "Agreement  Has been deleted")
        return redirect('wills:agreement_list')
    else:
        messages.error(request, "Agreement could not deleted")
        return HttpResponseRedirect(reverse('wills:agreement_detail', args=[object.pk]))

    return render(request, 'wills/detail.html')


@login_required
def cat_list(request):
    cats = AgreementCategory.objects.all()
    form = AgreementCategoryForm()

    context = {
        'cats': cats,
        'form': form
    }
    return render(request, 'wills/category/cat_list.html', context)


@login_required
def cat_detail(request, pk):
    cat = get_object_or_404(AgreementCategory, pk=pk)

    context = {
        'cat': cat,
        'form': AgreementCategoryForm(request.POST or None, instance=cat)
    }

    return render(request, 'wills/category/cat_detail.html', context)


@login_required
def add_cat(request):
    if request.method == "POST":
        form = AgreementCategoryForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, "Category has been added")
            return redirect('wills:cat_list')
    else:
        form = AgreementCategoryForm()

    return render(request, 'wills/category/cat_list.html', {'form': form})


@login_required
def update_cat(request, pk):
    cat = get_object_or_404(AgreementCategory, pk=pk)

    if request.method == "POST":
        form = AgreementCategoryForm(request.POST or None, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, "Category has been updated")
            return HttpResponseRedirect(reverse('wills:cat_detail', args=[cat.pk]))
        else:
            messages.error(request, "Category could not updated")
            return HttpResponseRedirect(reverse('wills:cat_detail', args=[cat.pk]))
    else:
        form = AgreementCategoryForm()

    return render(request, "wills/category/cat_detail.html", {'form': form})


@login_required
def cat_delete(request, pk):
    cat = get_object_or_404(AgreementCategory, pk=pk)
    if request.method == "POST":
        cat.delete()
        messages.success(request, "Category has been deleted")
        return redirect('wills:cat_list')
    else:
        messages.error(request, "Category could not deleted")
        return HttpResponseRedirect(reverse('wills:cat_detail', args=[cat.pk]))

    return render(request, 'wills/category/cat_detail.html')

# @login_required
# def client_cat(request, pk):
#     cat = get_object_or_404(AgreementCategory, pk=pk)
#     # client = Client.objects.filter(category=cat)

#     context = {
#         # 'client_list': client
#     }

#     return render(request, 'wills/category/client_list.html', context)
