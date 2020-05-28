from django.contrib import admin

# Register your models here.
from .models import Book, Branch, Category, BookHistory


admin.site.register(Branch)
admin.site.register(Category)
admin.site.register(BookHistory)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    '''Admin View for Book'''

    list_display = ('title', 'added_by', 'branch', 'category')
    list_filter = ('category',)

    search_fields = ('title',)
    # date_hierarchy = ''
    # ordering = ('',)
