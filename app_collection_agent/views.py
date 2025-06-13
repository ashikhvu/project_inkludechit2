from django.shortcuts import render
from rest_framework.views import APIView
from app_inkludechit.serializers import GetAllRegisteredCustomerSerializer,GetAllRegisteredCustomersNameandPhSerializer
from app_inkludechit.models import CustomerProfileModel,AgentProfileModel
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission,IsAdminUser,IsAuthenticated

class IsCollectionAgent(BasePermission):
    def has_permission(self,request,view):
        return request.user and request.user.is_authenticated and request.user.user_type == "collection agent"

# Create your views here.
class GetEformCompletedCustomer(APIView):

    permission_classes = [IsCollectionAgent]

    def get(self,request):
        try:
            cust_prof = CustomerProfileModel.objects.filter(is_salepunch_created=True)
        except CustomerProfileModel.DoesNotExist:
            return Response({"error":"Customer Details doesn't exist"},status=status.HTTP_400_BAD_REQUEST)
        serialzer = GetAllRegisteredCustomerSerializer(cust_prof,many=True)
        return Response(serialzer.data,status=status.HTTP_200_OK)
    
class GetAllEformCompletedCustomersNameandPh(APIView):

    permission_classes = [IsCollectionAgent]

    def get(self,request):
        try:
            cust_prof = CustomerProfileModel.objects.filter(is_salepunch_created=True)
        except CustomerProfileModel.DoesNotExist:
            return Response({"error":"Customer Details doesn't exist"},status=status.HTTP_400_BAD_REQUEST)
        serialzer = GetAllRegisteredCustomersNameandPhSerializer(cust_prof,many=True)
        return Response(serialzer.data,status=status.HTTP_200_OK)