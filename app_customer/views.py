from django.shortcuts import render
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from app_inkludechit.models import SalePunchModel
from app_inkludechit.serializers import SalePunchCreationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    def has_permission(self,request,view):
        return request.user and request.user.user_type == "customer"

# Create your views here.
class SalepunchSingleGet(APIView):

    permission_classes = [IsCustomer]

    def get(self,request):
        id = request.data("id")
        if not id:
            return Response({"error":"please provide an id"},status=status.HTTP_400_BAD_REQUEST)
        try:
            salepunch_data = SalePunchModel.objects.get()
        except SalePunchModel.DoesNotExist:
            return Response({"error":"SalePunch data doesn't exist"},status=status.HTTP_400_BAD_REQUEST)    
        serializer = SalePunchCreationSerializer(salepunch_data,many=False)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors)