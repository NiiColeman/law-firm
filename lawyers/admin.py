from django.contrib import admin
from .models import Lawyer, LawyerStatus, OtherStaff, User, Role
# Register your models here.


@admin.register(Lawyer)
class LawyerAdmin(admin.ModelAdmin):
    '''Admin View for Lawyer'''

    # list_display = ('user__username', 'user__email')

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


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    '''Admin View for Role'''

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


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    '''Admin View for User'''

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


@admin.register(OtherStaff)
class OtherStaffAdmin(admin.ModelAdmin):
    '''Admin View for OtherStaff'''

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


@admin.register(LawyerStatus)
class LawyerStatusAdmin(admin.ModelAdmin):
    '''Admin View for LawyerStatus'''

    # list_display = ('user__first_name',)
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
