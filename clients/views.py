from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
# from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse
from .forms import ClientForm, ClientCategoryForm,ClientCaseForm,ClientWillForm
# Create your views here.
from .models import Client, ClientCategory
from django.contrib import messages
from cases.models import Case
from django.contrib.auth.decorators import login_required



@login_required
def client_create_view(request):

    if request.method == "POST":
        form = ClientForm(request.POST or None)

        if form.is_valid():
            form.instance.added_by = request.user
            client = Client.objects.create(name=form.instance.name, phone=form.instance.phone,
                                           email=form.instance.email, added_by=request.user, category=form.instance.category, address=form.instance.address)
            messages.success(
                request, "{} has been added to your client list".format(client.name))
            return HttpResponseRedirect(reverse('clients:client_detail', args=[client.pk]))

        else:
            messages.error(
                request, "Failed to add Client, please check you form for errors")
            return redirect('clients:client_list')

    else:
        form = ClientForm()

    return render(request, 'clients/client_list.html', {'form': form})

@login_required
def client_list(request):
    client_list = Client.objects.all()
    form = ClientForm(request.POST or None)

    context = {
        'client_list': client_list,
        'form': form
    }

    return render(request, 'clients/client_list.html', context)

@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=client)
    client_cases = Case.objects.filter(client=client)
    print(client_cases)

    context = {
        'client': client,
        'form': form,
        'client_cases': client_cases,
        'case_form':ClientCaseForm(request.POST or None),
        'will_form':ClientWillForm(request.POST or None ),
    }

    return render(request, "clients/client_detail.html", context)

@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":

        form = ClientForm(request.POST or None, instance=client)
        form.instance.added_by = request.user
        form.save()

        messages.success(request, "client has been updated")

        return HttpResponseRedirect(reverse('clients:client_detail', args=[client.pk]))

    else:
        form = ClientForm()

    return render(request, 'clients/client_detail.html', {'form': form})

@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        client.delete()
        messages.success(request, "Client has been deleted")
        return redirect('clients:client_list')

    return render(request, 'clients/clients_detail.html')

@login_required
def category_list(request):
    cats = ClientCategory.objects.all()
    form = ClientCategoryForm

    context = {
        'cats': cats,
        'form': form
    }
    return render(request, 'clients/cat_list.html', context)

@login_required
def cat_detail(request, pk):
    cat = get_object_or_404(ClientCategory, pk=pk)

    context = {
        'cat': cat,
        'form': ClientCategoryForm(request.POST or None, instance=cat)
    }

    return render(request, 'clients/cat_detail.html', context)

@login_required
def add_cat(request):
    if request.method == "POST":
        form = ClientCategoryForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, "Category has been added")
            return redirect('clients:cat_list')
    else:
        form = ClientCategoryForm()

    return render(request, 'clients/cat_list.html', {'form': form})

@login_required
def update_cat(request, pk):
    cat = get_object_or_404(ClientCategory, pk=pk)

    if request.method == "POST":
        form = ClientCategoryForm(request.POST or None, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, "Category has been updated")
            return HttpResponseRedirect(reverse('clients:cat_detail', args=[cat.pk]))
        else:
            messages.error(request, "Category could not updated")
            return HttpResponseRedirect(reverse('clients:cat_detail', args=[cat.pk]))
    else:
        form = ClientCategoryForm()

    return render(request, "clients/cat_detail.html", {'form': form})

@login_required
def cat_delete(request, pk):
    cat = get_object_or_404(ClientCategory, pk=pk)
    if request.method == "POST":
        cat.delete()
        messages.success(request, "Category has been deleted")
        return redirect('clients:cat_list')
    else:
        messages.error(request, "Category could not deleted")
        return HttpResponseRedirect(reverse('clients:cat_detail', args=[cat.pk]))

    return render(request, 'clients/cat_detail.html')

@login_required
def client_cat(request, pk):
    cat = get_object_or_404(ClientCategory, pk=pk)
    client = Client.objects.filter(category=cat)

    context = {
        'client_list': client
    }

    return render(request, 'clients/client_list.html', context)





@login_required
def add_case(request,pk):
    client=get_object_or_404(Client,pk=pk)

    if request.method=="POST":

        form=ClientCaseForm(request.POST or None)
        if form.is_valid():

            form.instance.client=client
            form.instance.added_by=request.user
            form.save()

            messages.success(request, 'a new case hase been added for {}'.format(client.name))
            return HttpResponseRedirect(reverse('clients:client_detail', args=[client.pk] ))

        else:
            messages.error(request, 'Failed To Add A New Case For  {},Please Check Your Form'.format(client.name))
            return HttpResponseRedirect(reverse('clients:client_detail', args=[client.pk] ))
    else:
        form =ClientCaseForm()

    return render(request,'clients/client_detail',{'case_form':form})


def get_lawyer(user):
    qs=Lawyer.objects.get(user=user)

    return qs


@login_required
def add_will(request,pk):
    client=get_object_or_404(Client,pk=pk)

    if request.method=="POST":
        form = ClientWillForm(request.POST or None)
        if form.is_valid():
            form.instance.client=client
            form.save()

            messages.success(request, 'New will has been added for {}'.format(client.name))
            return redirect('wills:will_list')

        else:
            messages.error(request, 'failed to add new will for {}'.format(client.name))
            return HttpResponseRedirect(reverse('clients:client_detail', args=[client.pk]))

    else:
        form=ClientWillForm()



    return render(request,'clients/client_detail.html', {'will_form':form})








