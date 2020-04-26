from django.shortcuts import render, reverse, redirect, get_object_or_404
from .models import Authority, Principles
from django.views.generic import CreateView, ListView, CreateView, DeleteView, UpdateView
# Create your views here.
from .forms import AuthorityForm, PrinciplesForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required



@login_required
def auth_list(request):
    print(Authority.objects.all())
    context = {
        'auth_list': Authority.objects.all(),
        'form': AuthorityForm(request.POST or None)
    }

    return render(request, "authorities/authority_list.html", context)

@login_required
def add_auth(request):

    if request.method == "POST":
        form = AuthorityForm(request.POST or None)
        if form.is_valid():
            form.instance.user = request.user
            form.save()

            messages.success(request, "authority has been added")
            return redirect('principles:authority_list')
        else:
            pass

    else:
        form = AuthorityForm()

    return render(request, "authorities/create_authority.html", {'form': form})

@login_required
def authority_update(request, pk):
    auth = get_object_or_404(Authority, pk=pk)
    form = AuthorityForm(request.POST or None, instance=auth)

    if request.method == "POST":
        form = AuthorityForm(request.POST or None, instance=auth)

        if form.is_valid():
            form.save()
            messages.success(request, "authority has been added")
            return redirect('principles:authority_list')
        else:

            messages.error(request, "failed to add authority")
            return redirect('principles:authority_list')
    else:
        form = AuthorityForm()

    return render(request, "authorities/update.html", {'form': form})

@login_required
def authority_detail(request, pk):
    auth = get_object_or_404(Authority, pk=pk)
    form = AuthorityForm(request.POST or None, instance=auth)

    context = {
        'form': form,
        'auth': auth

    }

    return render(request, "authorities/detail.html", context)

@login_required
def authority_delete(request, pk):
    auth = get_object_or_404(Authority, pk=pk)

    if request.method == "POST":
        auth.delete()
        messages.success(request, "authority has been deleted")
        return redirect('principles:authority_list')

    else:
        messages.error(request, "Failed to delete authority")
        return redirect('principles:authority_list')
    return render(request, "authorities/delete.html")

@login_required
def principle_list(request):
    prin = Principles.objects.all()
    paginator = Paginator(prin, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        # 'principles': prin,
        'page_obj': page_obj
    }

    return render(request, "principles/list.html", context)

@login_required
def principle_detail(request, pk):
    prin = get_object_or_404(Principles, pk=pk)
    form = PrinciplesForm(request.POST or None, instance=prin)

    context = {
        'prin': prin,
        'form': form
    }

    return render(request, "principles/detail.html", context)

@login_required
def principle_update(request, pk):
    prin = get_object_or_404(Principles, pk=pk)

    if request.method == "POST":
        form = PrinciplesForm(request.POST or None, instance=prin)
        if form.is_valid():
            form.instance.added_by = request.user
            form.save()
            messages.success(request, "Principle has been added")
            return HttpResponseRedirect(reverse('principles:principle_detail', args=[prin.pk]))

        else:
            messages.error(request, "Principle could not be added")
            return HttpResponseRedirect(reverse('principles:principle_detail', args=[prin.pk]))

    else:
        form = PrinciplesForm()

    return render(request, "principles/detail.html", {'form': form})

@login_required
def principle_delete(request, pk):
    prin = get_object_or_404(Principles, pk=pk)

    if request.method == "POST":
        prin.delete()
        messages.success(request, "principle has been deleted")
        return HttpResponseRedirect(reverse('principles:principle_detail', args=[prin.pk]))

    else:
        messages.error(request, "Failed to delete principle")
        return HttpResponseRedirect(reverse('principles:principle_detail', args=[prin.pk]))

    return render(request, "principles/detail")

@login_required
def tag_list(request, pk):
    tag = get_object_or_404(Authority, pk=pk)

    principle_list = Principles.objects.filter(authority=tag)
    paginator = Paginator(principle_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }

    return render(request, "principles/list.html", context)

@login_required
def add_principle(request):

    if request.method == 'POST':
        p_form = PrinciplesForm(request.POST or None)

        if p_form.is_valid():
            p_form.instance.added_by = request.user
            print("hi")
            p_form.save()

            messages.success(request, "principle has ben added")
            return redirect('principles:principle_list')

            # Principle.objects.create(principle=p_form.instance.principle,authority=p_form.instance.authority)

        else:
            messages.error(request, "Failed to add principle")
            return redirect('principles:principle_list')

    else:
        p_form = PrinciplesForm()
    return render(request, "accounts/lawyer-profile.hmtl", {"p_form": p_form})
