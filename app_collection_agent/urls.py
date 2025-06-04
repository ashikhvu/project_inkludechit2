from django.urls import path
from . import views

urlpatterns = [
    path("get_ecreated_customers",views.GetEformCompletedCustomer.as_view(),name="get_ecreated_customers"),
]