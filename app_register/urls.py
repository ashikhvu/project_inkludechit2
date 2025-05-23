from django.urls import path
from . import views

urlpatterns = [
    path("customer_create",views.CustomerCreationSerializer.as_view(),name="customer_create"),
    path("customer_otp_auth",views.CustomerOtpAuthenticateView.as_view(),name="customer_otp_auth"),
]