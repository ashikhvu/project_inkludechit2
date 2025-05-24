from django.shortcuts import render
from rest_framework.views import APIView
from app_inkludechit.models import SalePunchModel,CustomerProfileModel,User
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework import status
from app_inkludechit.serializers import SalePunchCreationSerializer,CustomerUserCreationModelsSerializer
from rest_framework.response import Response
from rest_framework.permissions import BasePermission

class IsAdminOrIsStaff(BasePermission):
    def has_permission(self,request,view):
        return request.user and request.user.is_authenticated and (request.user.user_type in ["admin","super admin"] or request.user.user_type in ["sales agent","sales and collection agent"])

# Create your views here.
class SalePunchView(APIView):

    permission_classes = [IsAdminUser,IsAuthenticated]

    def get(self, request):
        profile = SalePunchModel.objects.all()
        if profile:
            serializer = SalePunchCreationSerializer(profile, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"error":"Data unavailable"},status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SalePunchCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetAllRegisteredCustomer(APIView):

    permission_classes = [IsAdminOrIsStaff]

    def get(self,request):
        user_type = request.user.user_type
        print(user_type)
        if user_type in ["admin","super admin"]:
            cust = CustomerProfileModel.objects.all()
            serializer = CustomerUserCreationModelsSerializer(cust,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif user_type in ["sales agent","sales and collection agent"]:
            try:
                user = User.objects.get(id=request.user.id)
            except User.DoesNotExist:
                return Response({"error","User doesn't exist"})
            cust = CustomerProfileModel.objects.filter(customer=user)
            serializer = CustomerUserCreationModelsSerializer(cust,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"error":"Data unavailable"},status=status.HTTP_400_BAD_REQUEST)