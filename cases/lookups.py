from lawyers.models import Lawyer

from ajax_select import register, LookupChannel


@register('lawyers')
class LawyerLookup(LookupChannel):

    model = Lawyer

    def get_query(self, q, request):
        return self.model.objects.filter(user__first_name__icontains=q)

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name
