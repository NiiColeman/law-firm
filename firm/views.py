from django.shortcuts import render
from cases.models import Case
from documents.models import Document,DocumentRecord
from lawyers.models import Lawyer, User, OtherStaff
from cases.models import Case, CaseTask
from documents.models import Document
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.decorators import group_required, groups_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from cases.models import
from datetime import datetime, date
from datetime import datetime, timedelta
from cases.tasks import notify_user
from clients.models import Client


@login_required
def index(request):
    lawyer = Lawyer.objects.all()
    case = Case.objects.all()
    document = Document.objects.all()
    user = request.user
    recs = DocumentRecord.objects.filter(approved=False)
    request.session['recs'] = recs.count()
    pending = Case.objects.filter(closed=False)
    request.session['pending'] = pending.count()

    completed = Case.objects.filter(closed=True)
    request.session['completed'] = completed.count()
    # request.session['other_staff']=Otherstaff.objects.get(user=request.user)
    date_me = datetime.now()+timedelta(15)
    close = CaseTask.objects.filter(
        deadline__lte=date_me)
    # for c in close:
    #     print(close)

    c = CaseTask.objects.all()
    # for f in c:
    #     print(f.case)

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
        doc = Document.objects.all()
        case = Case.objects.all()
        available = Document.objects.select_related(
            'status').filter(status__title='Available')
        not_available = Document.objects.select_related(
            'status').filter(status__title='Not Available')
        complete = Case.objects.filter(closed=True)
        pending = Case.objects.filter(closed=False)

        clients = Client.objects.all()
        client_count = clients.count()

        case_count = case.count()
        comp_count = complete.count()
        pend_count = pending.count()
        doc_count = doc.count()
        default = [client_count, case_count, comp_count, pend_count]
        avail_count = available.count()

        labels = [
            'Clients', 'Cases', 'Closed/Archived Cases', 'Active Cases'
        ]

        data2 = [doc_count, available.count(), not_available.count()]
        label1 = ['All Documents', 'Available Documents',
                  'Unavailable Documents']
        data = {
            'labels': labels,
            'default': default,
            'label1': label1,
            'data2': data2



        }

        return Response(data)
