from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
# Create your views here.
from .models import Correspondent
from .forms import CorrespondentForm, CaseCorrespondentForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cases.models import Case


@login_required
def list_corrs(request):
    object_list = Correspondent.objects.all()
    form = CorrespondentForm(request.POST or None)
    context = {
        'form': form,
        'object_list': object_list
    }

    return render(request, 'correspondents/list.html', context)


@login_required
def add_corrs(request):

    if request.method == "POST":
        form = CorrespondentForm(request.POST or None)
        if form.is_valid():
            form.instance.lawyer = request.user
            form.save()
            messages.success(request, "Correspondent has been added")
            return redirect('correspondents:list')
        else:
            messages.error(
                request, "Correspondent could not be added, please check your form")
            return redirect('correspondents:list')
    else:
        form = CorrespondentForm()

    return render(request, 'correspondents/list.html', context)


@login_required
def update_corrs(request, pk):
    object = get_object_or_404(Correspondent, pk=pk)

    if request.method == "POST":
        form = CorrespondentForm(request.POST or None, instance=object)
        if form.is_valid():
            form.instance.lawyer = request.user
            form.save()
            messages.success(request, "Correspondent has been updated")
            return HttpResponseRedirect(reverse('correspondents:detail', args=[object.pk]))
        else:
            messages.error(request, "Correspondent could not be updated")
            return HttpResponseRedirect(reverse('correspondents:detail', args=[object.pk]))
    else:
        form = CorrespondentForm()

    return render(request, 'correspondents/detail.html', {'form': form})


@login_required
def detail_corrs(request, pk):
    object = get_object_or_404(Correspondent, pk=pk)
    form = CorrespondentForm(request.POST or None, instance=object)

    context = {
        'form': form,
        'object': object
    }

    return render(request, 'correspondents/detail.html', context)


@login_required
def delete_corrs(request, pk):
    object = get_object_or_404(Correspondent, pk=pk)

    if request.method == "POST":
        object.delete()
        messages.success(request, "Correspondent has been deleted")
        return redirect('correspondents:list')
    else:

        messages.error(request, "Correspondent could not be deleted")
        return HttpResponseRedirect(reverse('correspondents:detail', args=[object.pk]))

    return render(request, 'correspondents/detail.html', context)


@login_required
def case_corrs(request, pk):
    object = get_object_or_404(Case, pk=pk)
    form = CaseCorrespondentForm(request.POST or None)
    object_list = Correspondent.objects.filter(case=object)

    context = {
        'form': form,
        'object': object,
        'object_list': object_list
    }

    return render(request, 'correspondents/list2.html', context)


@login_required
def case_add_corrs(request, pk):
    object = get_object_or_404(Case, pk=pk)

    object_list = Correspondent.objects.filter(case=object)

    if request.method == "POST":
        form = CaseCorrespondentForm(request.POST or None)
        if form.is_valid():
            form.instance.case = object
            form.instance.client = object.client
            form.instance.lawyer = request.user
            form.save()
            messages.success(request, "Correspondent has been addded")
            return HttpResponseRedirect(reverse('cases:case_detail', args=[object.pk]))
        else:
            messages.error(request, "Correspondent could not be added")
            return HttpResponseRedirect(reverse('cases:case_detail', args=[object.pk]))

    context = {
        'form': form,
        'object': object,
        'object_list': object_list
    }

    return render(request, 'casess/case_detail.html', context)
