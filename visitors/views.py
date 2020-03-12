from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

from .models import Visitor
from .forms import VisitorForm
from django.contrib import messages


def add_visitor(request):

    if request.method == "POST":
        form = VisitorForm(request.POST or None)

        if form.is_valid():
            form.save()

            messages.success(request, "Visitor has been added")
            return redirect('visitors:visitor_list')

        else:
            messages.error(request, "Failed to add visitor")
            return redirect('visitors:visitor_list')
    else:
        form = VisitorForm()

    return render(request, "visitors/visitor_list.html", {'form': form})


def visitor_list(request):
    visitor_list = Visitor.objects.all()
    form = VisitorForm(request.POST or None)
    print(visitor_list)

    context = {
        'visitor_list': visitor_list,
        'form': form
    }

    return render(request, "visitors/visitor_list.html", context)


def visitor_detail(request, pk):
    vis = get_object_or_404(Visitor, pk=pk)
    form = VisitorForm(request.POST or None, instance=vis)
    context = {
        'form': form,
        'vis': vis
    }

    return render(request, 'visitors/detail.html', context)


def update_visitor(request, pk):
    vis = get_object_or_404(Visitor, pk=pk)
    if request.method == "POST":
        form = VisitorForm(request.POST or None, instance=vis)
        if form.is_valid():
            form.save()
            messages.success(request, "Visitor has been updated ")
            return HttpResponseRedirect(reverse('visitors:visitor_detail',  args=[vis.pk]))
        else:
            messages.error(request, "failed to add visitor")
            return HttpResponseRedirect(reverse('visitors:visitor_detail', args=[vis.pk]))
    else:
        form = VisitorForm()

    return render(request, "visitors/detail.html", {'form': form})


def delete_visitor(request, pk):
    vis = get_object_or_404(Visitor, pk=pk)

    if vis:
        vis.delete()
        messages.success(request, "Visitor has been deleted ")
        return redirect('visitors:visitor_list')
    else:
        messages.error(request, "failed to delete visitor")
        return HttpResponseRedirect(reverse('visitors:visitor_detail', args=[vis.pk]))

    return render(request, "visitors/detail.html")
