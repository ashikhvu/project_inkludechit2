from django.urls import path
from . import views

urlpatterns = [
    path('salepunch',views.SalePunchView.as_view(),name="salepunch"),
    path("get_registered_cust",views.GetAllRegisteredCustomerView.as_view(),name="get_registered_cust"),
    path("delete_reg_customer",views.RemoveRegisteredCustomer.as_view(),name="delete_reg_customer"),
    path("clickon_register_btn",views.ClickOnRegisterBtn.as_view(),name="clickon_register_btn"),
]