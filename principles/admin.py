from django.contrib import admin

from .models import Authority, Principles

# Register your models here.


admin.site.register(Principles)
admin.site.register(Authority)
