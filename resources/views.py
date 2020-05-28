from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, BookHistory
from .forms import BookForm
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.
from django.contrib import messages
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from lawyers.models import Lawyer, OtherStaff
from cases.tasks import notify_staff, notify_approve



class BookListView(ListView, LoginRequiredMixin):
    model = Book
    template_name = "resources/book_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Book.objects.all()
        context["form"] = BookForm(self.request.method == "POST" or None)
        return context


# # detail view for books
# class BookDetail(DetailView, LoginRequiredMixin):
#     model = Book
#     template_name = 'resources/book_detail.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context variable for formto be rendered in template
#         context["form"] = BookForm(
#             self.request.method == "POST" or None, instance=self.object)
#         return context


@login_required
def detail_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)

    context = {
        'object': book,
        'form': form
    }
    return render(request, "resources/book_detail.html", context)


@login_required()
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST or None)

        if form.is_valid():
            form.instance.added_by = get_lawyer(request.user)
            form.save(commit=True)

            messages.success(request, "Book Has Been Added")
            return redirect('resources:book_list')

        else:
            messages.error(request, "Book could not be added")
            return redirect('resources:book_list')
    else:
        form = BookForm()

    return render(request, "resources/book_list.html", {'form': form})


# def update_book(request, pk):
#     object = get_object_or_404(Book, pk=pk)

#     if request.method == "POST":
#         form = BookForm(request.method == "POST", instance=object)
#         if form.is_valid():
#             # form.instance.added_by = get_lawyer(request.user)
#             form.save()
#             messages.success(request, "Book has been updated")
#             return HttpResponseRedirect(reverse('resources:book_detail', args=[object.pk]))
#         else:
#             messages.error(request, "Book has been deleted")
#             return HttpResponseRedirect(reverse('resources:book_detail', args=[object.pk]))
#     else:
#         form = BookForm()

#     return render(request, "resources/book_detail.html", {'form': form})

@login_required()
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        form = BookForm(request.POST or None, instance=book)
        if form.is_valid():
            form.instance.added_by = get_lawyer(request.user)
            form.save()
            messages.success(request, "Book has been updated")
            return HttpResponseRedirect(reverse('resources:book_detail', args=[book.pk]))
        else:
            messages.error(request, "Book has been deleted")
            return HttpResponseRedirect(reverse('resources:book_detail', args=[book.pk]))
    else:
        form = BookForm()

    return render(request, "resources/book_detail.html", {'form': form})


@login_required()
def delete_book(request, pk):
    object = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        object.delete()
        messages.success(request, "Book Has Been Added")
        return redirect('resources:book_list')

    else:
        messages.error(request, "Book could not be added")
        return redirect('resources:book_list')

    return render(request, 'resources/book_list.html')


def get_lawyer(user):

    qs = OtherStaff.objects.filter(user=user)

    if qs:
        return qs[0]
    else:
        return None


@login_required()
def request_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not book.requested:
        book.requested = True
        book.available = True
        book.save()
        lawyer = get_user(request.user)
        today = timezone.now()
        history = BookHistory.objects.create(book=book, lawyer=lawyer, date_requested=today)

        for user in staff:
            print("{} {}".format(user.user.id, user.user.username))
            msg1 = "New Document Request"
            msg2 = "{} has made a request for {}, this request needs approval".format(
                request.user, doc.title)
            notify_staff(user.user.id, msg1, msg2)

        messages.success(request, "Your requesthas been made")

        return redirect('resources:book_list')

    else:
        messages.error(request, "a request has already been made ")

        return redirect('resources:book_list')

    return render(request, 'resources/book_list.html')



def get_user(user):

    qs = Lawyer.objects.filter(user=user)

    if qs:
        return qs[0]
    else:
        return None


@login_required()
def approve_book(request, pk):
    hist = get_object_or_404(BookHistory, pk=pk)

    if hist:
        hist.approved_by = get_lawyer(request.user)
        hist.approved = True
        hist.date_approved = timezone.now()

        book = hist.book
        book.available = False
        book.save()
        hist.save()

        msg2 = "Dear {} , your request for {} has been approved.".format(
            hist.lawyer, book.title)
        msg1 = "Request Approved!"
        notify_approve(hist.lawyer.user.id, msg1, msg2)

        messages.success(request, "book has been approved")
        return redirect('resources:request_list')

    else:

        messsages.error(request, 'Oooops!! Something Went Wrong')

        return redirect('resources:request_list')

    return render(request, "resources/book_requests/req_list.html")


class BookHistoryListView(ListView, LoginRequiredMixin):
    model = BookHistory
    template_name = "resources/book_requests/req_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = BookHistory.objects.filter(approved=False).order_by(
            '-date_requested')
        return context


class BookHistoryDetailView(DetailView):
    model = BookHistory
    template_name = "resources/book_requests/req_detail.html"


class ApproveListView(ListView, LoginRequiredMixin):
    model = BookHistory
    template_name = "resources/approvals/approved.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["history"] = BookHistory.objects.filter(
            approved=True,returned=False).order_by('-date_approved')
        return context


class HistoryListView(ListView, LoginRequiredMixin):
    model = BookHistory
    template_name = "resources/approvals/history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["history"] = BookHistory.objects.filter(
            approved=True, returned=True).order_by('-date_returned')
        return context




@login_required()
def return_book(request, pk):
    hist = get_object_or_404(BookHistory, pk=pk)

    if hist:

        hist.returned = True
        hist.date_returned = timezone.now()

        book = hist.book
        book.available = True
        book.requested=False
        book.save()
        hist.save()

        messages.success(request, "book has been returned")
        return redirect('resources:approve_list')

    else:

        messsages.error(request, 'Oooops!! Something Went Wrong')

        return redirect('resources:request_list' )

    return render(request, "resources/approvals/approve.html")