from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
# from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView

from .forms import ClientForm, ClientCategory
# Create your views here.
from .models import Client, ClientCategory
from django.contrib import messages


def client_create_view(request):

    if request.method == "POST":
        form = ClientForm(request.POST or None)

        if form.is_valid():
            form.instance.added_by = request.user
            client = Client.objects.create(name=form.instance.name, phone=form.instance.phone,
                                           email=form.instance.email, added_by=request.user, category=form.instance.category, address=form.instance.address)
            messages.success(
                request, "{} has been added to your client list".format(client.name))
            return HttpResponseRedirect(reverse('client:client_detail', args=[cliint.pk]))

        else:
            messages.error(
                request, "Failed to add Client, please check you form for errors")
            return redirect('clients:client_list')

    else:
        form = ClientForm()

    return render(request, 'clients/client_list.html', {'form': form})


def client_list(request):
    client_list = Client.objects.all()
    form = ClientForm(request.POST or None)

    context = {
        'client_list': client_list,
        'form': form
    }

    return render(request, 'clients/client_list.html', context)


def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=client)

    context = {
        'client': client,
        'form': form
    }

    return render(request, "clients/client_detail.html", context)


def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":

        form = ClientForm(request.POST or None, instance=client)
        form.instance.added_by = request.user
        form.save()

        messages.success(request, "client has been updated")

        return HttpResponseRedirect(reverse('clients:client_detail', arg=[client.pk]))

    else:
        form = ClientForm()

    return render(request, 'clients/client_detail.html', {'form': form})


def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        client.delete()
        messages.success(request, "Client has been deleted")
        return redirect('clients:client_list')

    return render(request, 'clients/clients_detail.html')
