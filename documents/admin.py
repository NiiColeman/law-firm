from django.contrib import admin

# Register your models here.
from .models import Document, DocumentStatus, DocumentRecord, DocCategory, RequestArchive, DocumentArchive, DocFile


admin.site.register(DocCategory)

admin.site.register(DocumentArchive)
admin.site.register(RequestArchive)
admin.site.register(DocFile)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    '''Admin View for Document'''

    # list_display = ('',)
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)


@admin.register(DocumentRecord)
class DocumentRecordAdmin(admin.ModelAdmin):
    '''Admin View for DocumentRecords'''

    # list_display = ('',)
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)


@admin.register(DocumentStatus)
class DocumentStatusAdmin(admin.ModelAdmin):
    '''Admin View for DocumentStatus'''

    # list_display = ('',)
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
