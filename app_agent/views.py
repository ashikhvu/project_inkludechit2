from django.shortcuts import render
from rest_framework.views import APIView
from app_inkludechit.models import SalePunchModel,CustomerProfileModel,User
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework import status
from app_inkludechit.serializers import SalePunchCreationSerializer,GetAllRegisteredCustomerSerializer
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
    
class GetAllRegisteredCustomerView(APIView):

    permission_classes = [IsAdminOrIsStaff]

    def get(self,request):
        user_type = request.user.user_type
        print(user_type)
        if user_type in ["admin","super admin"]:
            cust = CustomerProfileModel.objects.all()
            serializer = GetAllRegisteredCustomerSerializer(cust,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif user_type in ["sales agent","sales and collection agent"]:
            try:
                user = User.objects.get(id=request.user.id)
            except User.DoesNotExist:
                return Response({"error","User doesn't exist"})
            cust = CustomerProfileModel.objects.filter(agent=user)
            serializer = GetAllRegisteredCustomerSerializer(cust,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"error":"Data unavailable"},status=status.HTTP_400_BAD_REQUEST)
    
class RemoveRegisteredCustomer(APIView):
    
    permission_classes = [IsAdminOrIsStaff]

    def post(self,request):
        id = request.data.get("id") or None
        print(request.user)
        if not id:
            return Response({"error":"Please provide an id"},status=status.HTTP_400_BAD_REQUEST)
        try:
            cust_prof = CustomerProfileModel.objects.get(id=id)
            cust = User.objects.get(id=cust_prof.customer.id)
            if request.user.user_type not in ["admin","super admin"]:
                if cust_prof.agent!=request.user:
                    return Response({"error":"User has no permission to delete this data"},status=status.HTTP_400_BAD_REQUEST)
            cust.delete()
            return Response({"success":"Customer deleted seccesfully"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)

class ClickOnRegisterBtn(APIView):

    permission_classes = [IsAdminOrIsStaff]

    def get(self,request):
        id = request.data.get("id") or None
        if not id:
            return Response({"error":"Please provide an id"},status=status.HTTP_200_OK)
        try:
            cust_prof = CustomerProfileModel.objects.get(id=id)
            serializer = GetAllRegisteredCustomerSerializer(cust_prof,many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except CustomerProfileModel.DoesNotExist:
            return Response({"error":"Customer details doesn't exist"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error",str(e)},status=status.HTTP_400_BAD_REQUEST)

