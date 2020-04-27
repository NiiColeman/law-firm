from django.urls import path
from .views import will_list, will_detail, will_update, add_will, delete_will

app_name = "wills"


urlpatterns = [
    path('wills/list', will_list, name="will_list"),
    path('will/add', add_will, name='add'),
    path('will/<int:pk>/detail', will_detail, name='details'),
    path('will/<int:pk>/update', will_update, name='update'),
    path('will/<int:pk>/deletee', delete_will, name='delete'),

]
