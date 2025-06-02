from django.urls import path
from . import views

urlpatterns = [
    path('all_salepunch_get',views.SalePunchViewListGet.as_view(),name="all_salepunch_get"),
]