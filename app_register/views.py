from django.shortcuts import render
from app_inkludechit.serializers import CustomerProfileCreationModelsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission

class IsAdminOrIsStaff(BasePermission):
    def has_permission(self,request,view):
        return request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser) 

# Create your views here.
class CustomerCreationSerializer(APIView):
    
    permission_classes = [IsAdminOrIsStaff]
    
    def post(self,request):
        serializer = CustomerProfileCreationModelsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"success":"Customer created successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)