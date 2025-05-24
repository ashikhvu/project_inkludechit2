from django.urls import path
from . import views

urlpatterns = [
    path('salepunch',views.SalePunchView.as_view(),name="salepunch"),
    path("get_registered_cust",views.GetAllRegisteredCustomer.as_view(),name="get_registered_cust"),
]