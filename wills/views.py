from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Will
from .forms import WillForm
from django.urls import reverse
# Create your views here.
from .models import models
from .forms import WillForm


def will_list(request):
    wills = Will.objects.filter(user=request.user)
    form = WillForm(request.POST or None)

    context = {
        'wills': wills,
        'form': form
    }
    return render(request, 'wills/list.html', context)


def will_detail(request, pk):
    will = get_object_or_404(Will, pk=pk)
    form = WillForm(request.POST or None, instance=will)
    context = {
        'will': will,
        'form': form
    }

    return render(request, 'wills/detail.html', context)


def will_update(request, pk):
    will = get_object_or_404(Will, pk=pk)

    if request.method == "POST":
        form = WillForm(request.POST or None, instance=will)
        if form.is_valid():
            form.instance.user = request.user
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


def add_will(request):

    if request.method == "POST":
        form = WillForm(request.POST or None)
        if form.is_valid():
            form.instance.user = request.user

            form.save()

            messages.success(request, "will has been added")
            return redirect('wills:will_list')
        else:
            messages.error(request, "failed to add will")
            return redirect('wills:will_list')

    else:
        form = WillForm()

    return render(request, 'wills/list.html', {'form': form})


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
