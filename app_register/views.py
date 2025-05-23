from django.shortcuts import render
from app_inkludechit.serializers import CustomerProfileCreationModelsSerializer,CustomerOtpAuthenticateSerializer
# from app_inkludechit.serializers import CustomerRegisterSendOtp
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission
from twilio.rest import Client
from django.conf import settings
import random

def SendOTPFunction(ph,msg):
    client = Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
    response = client.messages.create(
        body=msg,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=ph
    )
    return response.sid

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
            customer_random_otp = random.randint(1111,9999)
            serializer.validated_data["customer_otp"] = customer_random_otp
            serializer.save()
            customer_otp = str(customer_random_otp)
            phone = "+91"+ str(customer_random_otp)
            msg = f"Your OTP is [ {customer_random_otp} ]"
            print(f"Your OTP is [ {customer_random_otp} ]")
            # SendOTPFunction(phone,msg)
            return Response({"success":"OTP Sent Successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# class CustomerSendOtp(APIView):
    
#     permission_classes = [IsAdminOrIsStaff]
    
#     def post(self,request):
#         serializer = CustomerRegisterSendOtp(data=request.data)
#         if serializer.is_valid():
#             customer_otp = str(serializer.validated_data["customer_otp"])
#             phone = "+91"+ str(serializer.validated_data["mobile_no"])
#             msg = f"Your OTP is [ {customer_otp} ]"
#             print(f"Your OTP is [ {customer_otp} ]")
#             # SendOTPFunction(phone,msg)
#             return Response({"success":"OTP Sent Successfully"},status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#         # return Response({"error":"OTP Sending Failed"},status=status.HTTP_400_BAD_REQUEST)

class CustomerOtpAuthenticateView(APIView):
    
    permission_classes = [IsAdminOrIsStaff]

    def post(self,request):
        serializer = CustomerOtpAuthenticateSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"success":"Validation success"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
