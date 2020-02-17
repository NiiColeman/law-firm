from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import DocumentRecord, DocumentRecord, DocumentStatus, Document
# Create your views here.
from django.contrib import messages
from .forms import DocumentForm,RequestDocumentForm,DocumentRecordForm
from lawyers.models import User,Lawyer,OtherStaff
from accounts.decorators import group_required, groups_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



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
        'form':form
    }
    return render(request, 'documents/doc_detail.html', context)

@login_required
def add_document(request):

    if request.method == "POST":
        form = DocumentForm(request.POST or None)

        if form.is_valid():
            form.instance.added_by = request.user
            doc = Document()
            doc.title = form.instance.title
            doc.added_by = request.user
            doc.status = form.instance.status
            doc.storage_location = form.instance.storage_location
            doc.category = form.instance.category
            doc.date_added = form.instance.date_added
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
    doc =get_object_or_404(Document, pk=pk)

    if request.method == "POST":
        form = DocumentForm(request.POST or None, instance=doc)
        if form.is_valid():
            form.save()

            messages.success(
                request, "{} has been updated".format(form.instance.title))
            return HttpResponseRedirect(reverse('documents:document_detail', args=[doc.id]))
        else:
            messages.error(request, "failed to update case")

    else:
        form = DocumentForm()

    return render(request, 'documents/doc_detail.html', {'form': form})

@login_required
def record_list(request):
    recs = DocumentRecord.objects.all().order_by('date_approved')
    apps=DocumentRecord.objects.filter(approved=True)
    reqs=DocumentRecord.objects.filter(approved_by=None)
    form=DocumentRecordForm()

    context = {
        'recs': recs,
        'form':form,
        'apps':apps,
        'reqs':reqs
    }

    return render(request, 'records/records_list.html', context)

@login_required
def record_detail(request, pk):
    rec = get_object_or_404(DocumentRecord, pk=pk)
    form = DocumentRecordForm(request.POST or None, instance=rec)

    context = {
        'rec': rec,
        'form':form
    }

    return render(request, 'records/records_detail.html',context)

@login_required
def record_update(request,pk):
    rec = get_object_or_404(DocumentRecord, pk=pk)

    if request.method=="POST":
        form=DocumentRecordForm(request.POST or None, instance=rec)

        if form.is_valid():
            form.save()

            messages.success(request,"{} has been updated".format(rec.document.title))
            return HttpResponseRedirect(reverse('documents:record_detail' , args=[rec.pk]))
        else:
            messages.error(request,"failed to update {} ".format(rec.document.title))
            return HttpResponseRedirect(reverse('documents:record_detail' , args=[rec.pk]))

    else:
        form=DocumentRecordForm()

    return render(request,'records/record_detail.html',{'form':form})


@login_required
def record_delete(request,pk):
    rec = get_object_or_404(DocumentRecord, pk=pk)

    if request.method=="POST":
        rec.delete()
        messages.success(request,'{} has been deleted'.format(rec.document.title))
        return redirect('documents:record_list')
    else:
        messages.error(request,'{} could not be deleted'.format(rec.document.title))

    return render(request,'records/record_detail.html')





@login_required
def request_doc(request,pk):
    doc=get_object_or_404(Document,pk=pk)

    if request.method=="POST":
        DocumentRecord.objects.create(document=doc,requested_by=get_lawyer(request.user))
        # doc.status=get_status(2)
        # doc.save()
        messages.success(request,"You request for {} has been made".format(doc.title))
        return redirect('documents:doc_list')

    else:
        messages.error(request,"You request for {} could not be made".format(doc.title))
        return redirect('documents:doc_list')
    

    return render(request,"documents/doc_list.html")






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

    qs=Lawyer.objects.filter(user=user)

    if qs:
        return qs[0]
    else:
        return None
    


@login_required
def document_request(request):
    form=RequestDocumentForm()
    recs=DocumentRecord.objects.all()
    apps=DocumentRecord.objects.filter(approved=True)
    reqs=DocumentRecord.objects.filter(approved_by=None)

    if request.method=="POST": 

        form=RequestDocumentForm(request.POST or None)

        try:
            form.instance.requested_by=get_lawyer(request.user)
            form.save()
            messages.success(request,"Request has been made successfully")
            # return redirect()
        except:
            messages.error(request, "Failed to request document, user is either not authenticated or not a lawyer")
            # return redirect()
    else:
        form=RequestDocumentForm()

    
    return render(request,'records/records_list.html',{'form':form,'recs':recs,'apps':apps,'reqs':reqs})



@login_required
def document_request_list(request):
    
    recs= Document.objects.filter(approved=False)


    context={
        'recs':recs,

    }


    return render(request,"documents/records.html")


    
@login_required
def document_delete_view(request,pk):

    doc=get_object_or_404(Document,pk=pk)

    if request.method=="POST":

        
        doc.delete()
        messages.success(request,"document has been deleted")
        return redirect('documents:doc_list')
              
    else:


        messages.warning(request,'document was not deleted,you are not uathorized to delete this file')
        return HttpResponseRedirect(reverse('documents:document_detail', args=[doc.pk]))


    


    return render(request,'documents/doc_detail.html')



def get_status(id):
    status=DocumentStatus.objects.get(id=id)
    if status:
        return status
    else:
        return None
        



@login_required
def approve_request(request,pk):
    rec=get_object_or_404(DocumentRecord,pk=pk)
    rec.approved_by=get_otherstaff(request.user)
    rec.approved=True
    rec.save()
    messages.success(request,'{} has been approved'.format(rec.document.title))
    return redirect('documents:record_list')


    



def get_otherstaff(user):
    qs=OtherStaff.objects.get(user=user)


    if qs:
        return qs
    else:
        return None
