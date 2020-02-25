from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import DocumentRecord, DocumentRecord, DocumentStatus, Document, DocumentArchive, DocumentRecord, RequestArchive
# Create your views here.
from django.contrib import messages
from .forms import DocumentForm, RequestDocumentForm, DocumentRecordForm
from lawyers.models import User, Lawyer, OtherStaff
from accounts.decorators import group_required, groups_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from datetime import datetime, timedelta, timezone
from django.utils import timezone
from cases.tasks import notify_staff, notify_approve


@login_required
def document_list(request):
    documents = Document.objects.all().order_by('date_modified')
    available_documents = Document.objects.select_related(
        'status').filter(status__title='Available')
    form = DocumentForm()
    context = {
        'docs': documents,
        'available': available_documents,
        'form': form,
    }

    return render(request, 'documents/doc_list.html', context)


@login_required
def document_detail(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    form = DocumentForm(request.POST or None, instance=doc)

    context = {
        'doc': doc,
        'form': form
    }
    return render(request, 'documents/doc_detail.html', context)


@login_required
def add_document(request):

    if request.method == "POST":
        form = DocumentForm(request.POST or None)

        if form.is_valid():

            person = "{} {}".format(
                request.user.first_name, request.user.last_name)
            form.instance.added_by = request.user
            doc = Document()
            doc.title = form.instance.title
            doc.added_by = request.user
            doc.status = form.instance.status
            doc.storage_location = form.instance.storage_location
            doc.category = form.instance.category
            doc.date_added = form.instance.date_added
            archive = DocumentArchive.objects.create(document=doc.title, location=doc.storage_location, status=doc.status,
                                                     date_added=doc.date_added, description=doc.description, added_by=person, category=doc.category)
            print(archive)
            doc.save()

            messages.success(request, 'Document has been added!')
            return HttpResponseRedirect(reverse('documents:document_detail', args=[doc.id]))

        else:
            messages.error(
                request, "Failed to create new document. please check your form")
    else:
        form = DocumentForm()

    return render(request, "documents/add_doc.html", {'form': form})


@login_required
def update_document(request, pk):
    doc = get_object_or_404(Document, pk=pk)

    if request.method == "POST":
        form = DocumentForm(request.POST or None, instance=doc)
        if form.is_valid():
            # form.instance.added_by=request.user
            form.save()

            # archive=DocumentArchive.objects.create(document=form.instance.title,location=form.instance.storage_location,status=form.instance.status,date_added=form.instance.date_added,description=form.instance.description)
            # print(archive)
            try:
                req_archive = get_request_archive(doc.title)
                req_archive.document = form.instance.title
                print(req_archive)
                # req_archive
                # req_archive

                archive = get_document_archive(doc.title)
                print(archive)
                archive.document = form.instance.title
                archive.description = form.instance.description
                archive.location = form.instance.storage_location
                # archive.added_by=doc.added_by
                archive.date_added = form.instance.date_added
                archive.category = form.instance.category
                archive.save()
            except:
                print('document doesnt exist')

            try:
                req_archive = get_request_archive(doc.title)
                req_archive.document = form.instance.title
                print(req_archive)
            except:
                print('document doesnt exist')

            messages.success(
                request, "{} has been updated".format(form.instance.title))
            return HttpResponseRedirect(reverse('documents:document_detail', args=[doc.id]))
        else:
            messages.error(request, "failed to update Document")

    else:
        form = DocumentForm()

    return render(request, 'documents/doc_detail.html', {'form': form})


@login_required
def record_list(request):
    recs = DocumentRecord.objects.all().order_by('date_approved')
    apps = DocumentRecord.objects.filter(approved=True)
    reqs = DocumentRecord.objects.filter(approved_by=None)
    form = DocumentRecordForm()

    context = {
        'recs': recs,
        'form': form,
        'apps': apps,
        'reqs': reqs
    }

    return render(request, 'records/records_list.html', context)


@login_required
def record_detail(request, pk):
    rec = get_object_or_404(DocumentRecord, pk=pk)
    form = DocumentRecordForm(request.POST or None, instance=rec)

    context = {
        'rec': rec,
        'form': form
    }

    return render(request, 'records/records_detail.html', context)


@login_required
def record_update(request, pk):
    rec = get_object_or_404(DocumentRecord, pk=pk)

    if request.method == "POST":
        form = DocumentRecordForm(request.POST or None, instance=rec)

        if form.is_valid():
            form.save()

            messages.success(
                request, "{} has been updated".format(rec.document.title))
            return HttpResponseRedirect(reverse('documents:record_detail', args=[rec.pk]))
        else:
            messages.error(
                request, "failed to update {} ".format(rec.document.title))
            return HttpResponseRedirect(reverse('documents:record_detail', args=[rec.pk]))

    else:
        form = DocumentRecordForm()

    return render(request, 'records/record_detail.html', {'form': form})


@login_required
def record_delete(request, pk):
    rec = get_object_or_404(DocumentRecord, pk=pk)

    if request.method == "POST":
        rec.delete()
        messages.success(
            request, '{} has been deleted'.format(rec.document.title))
        return redirect('documents:record_list')
    else:
        messages.error(
            request, '{} could not be deleted'.format(rec.document.title))

    return render(request, 'records/record_detail.html')


@login_required
def request_doc(request, pk):
    doc = get_object_or_404(Document, pk=pk)

    if request.method == "POST":
        DocumentRecord.objects.create(
            document=doc, requested_by=get_lawyer(request.user))
        # doc.status=get_status(2)
        # doc.save()
        messages.success(
            request, "You request for {} has been made".format(doc.title))
        msg1 = "New Document Request"
        msg2 = "{} has mad a request for {}, this request needs approval".format(
            request.user, doc.title)
        notify_staff(23, msg1, msg2)

        return redirect('documents:doc_list')

    else:
        messages.error(
            request, "You request for {} could not be made".format(doc.title))
        return redirect('documents:doc_list')

    return render(request, "documents/doc_list.html")


# def document_delete(request,pk):

#     if request.method=="POST":
#         doc=get_object_or_404(Document,pk=pk)
#         doc.delete()

#         messages.success(request,"{} Has Been Deleted".format(doc.title))
#         return redirect('documents:doc_list')
#     else:
#         doc=get_object_or_404(Document,pk=pk)
#         messages.error(request,"{} could not be deleted".format(doc.title))
#         return HttpResponseRedirect(reverse('documents:document_detail', args=[doc.pk]))


#     return render(request,'documents/delete.html')


def get_lawyer(user):

    qs = Lawyer.objects.filter(user=user)

    if qs:
        return qs[0]
    else:
        return None


@login_required
def document_request(request):
    form = RequestDocumentForm()
    recs = DocumentRecord.objects.all()
    apps = DocumentRecord.objects.filter(approved=True)
    reqs = DocumentRecord.objects.filter(approved_by=None)

    if request.method == "POST":

        form = RequestDocumentForm(request.POST or None)

        try:
            form.instance.requested_by = get_lawyer(request.user)
            form.save()
            messages.success(request, "Request has been made successfully")
            # return redirect()
        except:
            messages.error(
                request, "Failed to request document, user is either not authenticated or not a lawyer")
            # return redirect()
    else:
        form = RequestDocumentForm()

    return render(request, 'records/records_list.html', {'form': form, 'recs': recs, 'apps': apps, 'reqs': reqs})


@login_required
def document_request_list(request):

    recs = Document.objects.filter(approved=False)

    context = {
        'recs': recs,

    }

    return render(request, "documents/records.html")


@login_required
def document_delete_view(request, pk):

    doc = get_object_or_404(Document, pk=pk)

    if request.method == "POST":

        doc.delete()
        messages.success(request, "document has been deleted")
        return redirect('documents:doc_list')

    else:

        messages.warning(
            request, 'document was not deleted,you are not uathorized to delete this file')
        return HttpResponseRedirect(reverse('documents:document_detail', args=[doc.pk]))

    return render(request, 'documents/doc_detail.html')


def get_status(id):
    status = DocumentStatus.objects.get(id=id)
    if status:
        return status
    else:
        return None


@login_required
def approve_request(request, pk):
    rec = get_object_or_404(DocumentRecord, pk=pk)
    rec.approved_by = get_otherstaff(request.user)
    rec.approved = True
    rec.save()
    messages.success(
        request, '{} has been approved'.format(rec.document.title))

    archive = RequestArchive.objects.create(document=rec.document.title, description=rec.document.description, date_added=rec.document.date_added,
                                            date_requested=rec.date_requested, approved_by=request.user, date_approved=timezone.now(), requested_by=rec.requeted_by)
    print(archive)
    return redirect('documents:record_list')


def get_otherstaff(user):
    qs = OtherStaff.objects.get(user=user)

    if qs:
        return qs
    else:
        return None


def get_document_archive(doc):

    rec = DocumentArchive.objects.filter(document=doc)
    if rec[0]:
        return rec
    else:
        return None


def document_archive_list(request):
    archives = DocumentArchive.objects.all()

    context = {
        'archives': archives
    }

    return render(request, 'documents/archive_list.html', context)


def record_archive_list(request):
    records = RequestArchive.objects.all()

    context = {
        'records': records
    }

    return render(request, "documents/request_list.html", context)


def get_request_archive(doc):
    qs = RequestArchive.objects.filter(doc)
    if qs[0]:
        return qs
    else:
        return None
