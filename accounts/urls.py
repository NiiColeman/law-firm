from django.urls import path
from .views import accounts, update_lawyers_profile, staff_detail_view, lawyer_profile_view, lawyer_detail, lawyer_list, lawyer_profile, other_staff, update_lawyer_profile, change_password, add_staff, staff_details, update_staff, update_staff_profile


app_name = "accounts"


urlpatterns = [




    path("accounts/signup", accounts, name="signup"),
    path("accounts/lawyer/signup", lawyer_profile_view, name='lawyer-signup'),
    path("accounts/lawyers/lawyer-list", lawyer_list, name="lawyer_list"),
    path("accounts/lawyers/<int:pk>/lawyer-detail",
         lawyer_detail, name="lawyer_detail"),
    path("accounts/lawyers/<int:pk>/lawyer-profile",
         lawyer_profile, name="lawyer_profile"),

    path("accounts/front-desk/staff-list", other_staff, name="staff_list"),
    path("accounts/password", change_password, name="change_password"),
    path("accounts/users/add-staff", add_staff, name="add_staff"),
    path("accounts/users/<int:pk>/staff-detail",
         staff_details, name='staff_detail'),
    path("accounts/users/<int:pk>/update-staff",
         update_staff, name='update_staff'),

    path("accounts/lawyers/<int:pk>/lawyers-profile",
         update_lawyers_profile, name="lawyers_profile"),







    path("accounts/profile/<int:pk>/update-profile",
         update_lawyer_profile, name="update_profile"),
    path("accounts/profile/staff-profile",
         staff_detail_view, name="staff_profile"),


    path("accounts/profile/<int:pk>/update-staff-profile",
         update_staff_profile, name="staff_profileupdate"),




]
