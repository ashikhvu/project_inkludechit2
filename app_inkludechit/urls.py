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
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
