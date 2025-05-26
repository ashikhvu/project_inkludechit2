from django.urls import path
from . import views

urlpatterns = [
    path('salepunch',views.SalePunchView.as_view(),name="salepunch"),
    path("get_registered_cust",views.GetAllRegisteredCustomerView.as_view(),name="get_registered_cust"),
]