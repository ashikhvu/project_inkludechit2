from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('userlogin',views.CustomLoginView.as_view(),name="userlogin"),
    path('sendotp',views.SendOtp.as_view(),name="sendotp"),
    path('share_interest',views.ShareMyInterestView.as_view(),name="share_interest"),
    path('getshare_interest',views.GetShareMyInterest.as_view(),name="getshare_interest"),
    path('customerfetch',views.CustomerFetch.as_view(),name="customerfetch"),

    # bank
    path('get_all_bank',views.GetAllBankView.as_view(),name="get_all_bank"),

    #agent
    path("get_user_profile",views.UserProfileView.as_view(),name="get_user_profile"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
