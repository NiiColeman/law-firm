"""firm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index, FirmChart
# from ajax_select import urls
# from ajax_select import urls as ajax_select_url
from ajax_select import urls as ajax_select_urls

admin.autodiscover()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("api/chart/data", FirmChart.as_view(), name="api-data"),

    path("", index, name="index"),
    path("", include('accounts.urls')),
    path("", include('cases.urls')),
    path("", include('documents.urls')),
    path("", include('principles.urls')),
    path("", include('clients.urls')),
    path("", include('schedules.urls')),
    path("", include('visitors.urls')),
    path("", include('wills.urls')),









    # path('ajax_select/', include('ajax_select.urls'))
    path('ajax_select/', include(ajax_select_urls)),



]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
