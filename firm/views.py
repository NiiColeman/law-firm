from django.shortcuts import render
from cases.models import Case
from documents.models import Document
from lawyers.models import Lawyer,User
from cases.models import Case
from documents.models import Document
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.decorators import group_required, groups_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def index(request):
    lawyer = Lawyer.objects.all()
    case = Case.objects.all()
    document = Document.objects.all()

    context = {
        'lawyer': lawyer,
        'case': case,
        'document': document
    }

    return render(request, 'firm/index.html', context)





class FirmChart(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        doc=Document.objects.all()
        case=Case.objects.all()
        available=Document.objects.select_related(
        'status').filter(status__title='Available')
        not_available= Document.objects.select_related(
        'status').filter(status__title='Not Available')
        complete=Case.objects.select_related('status').filter(status__title="Complete")
        pending=Case.objects.select_related('status').filter(status__title="Pending")


        case_count=case.count()
        comp_count=complete.count()
        pend_count=pending.count()
        doc_count=doc.count()
        default=[case_count,comp_count,pend_count]
        avail_count=available.count()

        labels=[
            'Cases','Completed Cases','Pending Cases'
        ]

        data2=[doc_count,available.count(),not_available.count()]
        label1=['All Documents','Available Documents','Unavailable Documents']
        data={
            'labels':labels,
            'default':default,
            'label1':label1,
            'data2':data2



        }


        return Response(data)




