from django.contrib import admin

# Register your models here.
from .models import ClientCategory, Client

admin.site.register(ClientCategory)
admin.site.register(Client)
