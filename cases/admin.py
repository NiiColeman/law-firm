from django.contrib import admin

# Register your models here.
from .models import Case, Status, Category, PriorityLevel, CaseTask, CaseFile, CaseArchive, LegalArgument


admin.site.header = 'Law Firm'

admin.site.register(CaseTask)
admin.site.register(PriorityLevel)
admin.site.register(CaseFile)
admin.site.register(CaseArchive)
admin.site.register(LegalArgument)


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    '''Admin View for Case'''

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


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    '''Admin View for Status'''

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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Status'''
