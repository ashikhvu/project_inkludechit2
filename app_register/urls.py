from django.urls import path
from . import views

urlpatterns = [
    path("customer_create",views.CustomerCreationSerializer.as_view(),name="customer_create"),
]