from django.urls import path
from . import views

urlpatterns = [
    path('salepunch_post',views.SalePunchViewPost.as_view(),name="salepunch_post"),
    path("get_registered_cust",views.GetAllRegisteredCustomerView.as_view(),name="get_registered_cust"),
    path("delete_reg_customer",views.RemoveRegisteredCustomer.as_view(),name="delete_reg_customer"),
    path("clickon_register_btn",views.ClickOnRegisterBtn.as_view(),name="clickon_register_btn"),
    path("sales_agent_dashboard",views.SalesAgentDashBoard.as_view(),name="sales_agent_dashboard"),
]