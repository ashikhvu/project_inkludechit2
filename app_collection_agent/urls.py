from django.urls import path
from . import views

urlpatterns = [
    path("get_ecreated_customers",views.GetEformCompletedCustomer.as_view(),name="get_ecreated_customers"),
    path("get_ecreated_customers_name_and_ph",views.GetAllEformCompletedCustomersNameandPh.as_view(),name="get_ecreated_customers_name_and_ph"),
    path("get_customer_details",views.CustomerDetailsForCollectionAgent.as_view(),name="get_customer_details"),
]