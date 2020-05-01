from django.contrib import admin

# Register your models here.
from .models import Will, Agreement, AgreementCategory

admin.site.register(Will)
admin.site.register(Agreement)
admin.site.register(AgreementCategory)

