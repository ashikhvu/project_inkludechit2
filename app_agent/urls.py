from django.urls import path
from . import views

urlpatterns = [
    path('salepunch',views.SalePunchView.as_view(),name="salepunch"),
]