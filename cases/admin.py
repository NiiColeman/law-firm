from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib import admin

# Register your models here.
from .models import Case, Status, Category, PriorityLevel, CaseTask, CaseFile,  LegalArgument, Representative


admin.site.header = 'Law Firm'


admin.site.register(Representative)

admin.site.register(CaseTask)
admin.site.register(PriorityLevel)
admin.site.register(CaseFile)
# admin.site.register(CaseArchive)
admin.site.register(LegalArgument)


@admin.register(Case)
class CaseAdmin(ImportExportModelAdmin):
    '''Admin View for Case'''

    list_display = ('name', 'category', 'court',
                    'date_added', 'added_by', 'closed')
    list_filter = ('category', 'court', 'closed', 'date_updated')
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    search_fields = ('name', 'description', 'category__name',
                     'lawyer__user__username', 'lawyer__user__first_name', 'lawyer__user__last_name')
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
