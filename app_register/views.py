from django.shortcuts import render
# from app_inkludechit.serializers import CustomerRegisterSendOtp
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission
from twilio.rest import Client
from django.conf import settings
import random
from app_inkludechit.serializers import CustomerCreationAndSendOtpSerializer
from app_inkludechit.models import User

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
        return request.user and request.user.is_authenticated and (request.user.user_type in ["admin","super admin"] or request.user.user_type in ["sales agent","sales and collection agent"])

# Create your views here.
class CustomerCreationSerializer(APIView):
    
    permission_classes = [IsAdminOrIsStaff]

    def post(self,request):
        serializer = CustomerCreationAndSendOtpSerializer(data=request.data)
        if serializer.is_valid():
            cust_data = serializer.validated_data
            rand_otp = random.randint(1111,9999)
            cust_data["customer_otp"] =rand_otp
            request.session["customer_data"] = cust_data
            request.session.set_expiry(180)
            request.session.modified = True
            ph = "+91"+ serializer.validated_data["mobile_no"]
            msg = f"Your OTP is [ {rand_otp} ]"
            # SendOTPFunction(ph,msg)
            print(f"Your OTP is [ {rand_otp} ]")
            return Response({"success":"Otp send successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_200_OK)
    

class CustomerOtpAuthenticateView(APIView):
    

    permission_classes = [IsAdminOrIsStaff]

    def post(self,request):
        serializer = CustomerCreationAndSendOtpSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data["mobile_no"]
            customer_otp = serializer.validated_data["customer_otp"]
            email = serializer.validated_data["email"]
            customer_name = serializer.validated_data["customer_name"]
            
            cust_data = request.session.get("customer_data")
            if cust_data and cust_data["mobile_no"] == mobile:
                if int(cust_data["customer_otp"]) ==  int(customer_otp):
                    customer_user = User.objects.create(
                        first_name=customer_name,
                        mobile=mobile,
                        email=email,
                    )
                    serializer.validated_data["agent"]=request.user
                    serializer.validated_data["customer"]=customer_user
                    serializer.validated_data["is_verified"]=True
                    serializer.save()
                    return Response({"success":"OTP verfication success"},status=status.HTTP_200_OK)
                else: 
                    return Response({"error":"Invalid OTP"},status=status.HTTP_400_BAD_REQUEST) 
            else:
                return Response({"error":"mobile number not found"},status=status.HTTP_400_BAD_REQUEST) 

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

