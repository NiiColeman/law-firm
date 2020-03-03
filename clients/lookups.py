from .models import Client, ClientCategory

from ajax_select import register, LookupChannel


@register('category')
class ClientCategoryLookup(LookupChannel):

    model = ClientCategory

    def get_query(self, q, request):
        return self.model.objects.filter(title__icontains=q).order_by('title')

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name
