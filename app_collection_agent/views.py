from django.shortcuts import render
from rest_framework.views import APIView
from app_inkludechit.serializers import GetAllRegisteredCustomerSerializer
from app_inkludechit.models import CustomerProfileModel 
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class GetEformCompletedCustomer(APIView):
    def get(self,request):
        try:
            cust_prof = CustomerProfileModel.objects.filter(is_salepunch_created=True)
        except CustomerProfileModel.DoesNotExist:
            return Response({"error":"Customer Details doesn't exist"},status=status.HTTP_400_BAD_REQUEST)
        serialzer = GetAllRegisteredCustomerSerializer(cust_prof,many=True)
        return Response(serialzer.data,status=status.HTTP_200_OK)
    
