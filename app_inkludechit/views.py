from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User,SalePunchModel,ShareMyInterestModel,AgentProfileModel,BankListModel
from .serializers import SalePunchCreationSerializer,CustomTokenObtainPairSerializer,CustomUserLoginSerializer,SendOtpSerializer,ShareMyInterestModelSerializer,BankModelSerializer,UserProfileGetSerailzer
from rest_framework import status
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from twilio.rest import Client
from django.conf import settings
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.views.generic import TemplateView
from rest_framework.permissions import BasePermission


# Create your views here.
# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
        
class IsAdminOrIsStaff(BasePermission):
    def has_permission(self,request,view):
        return request.user and request.user.is_authenticated and (request.user.user_type in ["admin","super admin"] or request.user.user_type in ["sales agent","sales and collection agent"])

class IsAgent(BasePermission):
    def has_permission(self,request,view):
        return request.user and request.user.is_authenticated and request.user.user_type in ["sales agent","collection agent","sales and collection agent"]

# BANK VIEW FUNCTION START

class GetAllBankView(APIView):

    permission_classes = [IsAdminOrIsStaff]

    def get(self,request):
        bank_list = BankListModel.objects.all().order_by("bank_name")
        print(bank_list)
        serializer = BankModelSerializer(bank_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

# BANK VIEW FUNCTION END

def OtpSendFunction(phone,message):
    client = Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
    response = client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone
    )
    return response.sid

class SendOtp(APIView):
    def post(self,request):
        serializer = SendOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        ph = '+91'+ result['email_or_mobile']
        msg = f'Your OTP is [ {result["otp"]} ]'
        print(f"\n{ph}\n{msg}")
        try:
            # OtpSendFunction(ph,msg)
            return Response({"success":"OTP has been send to your Registered mobile number"},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        # return Response({"success":"OTP has been send to your Registered mobile number"},status=status.HTTP_201_CREATED)
    
class CustomLoginView(APIView):
    # print("login here")
    def post(self, request):
        serializer = CustomUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        agent_prof_code = None
        if user.user_type in ["sales agent","collection agent","sales and collection agent"]:
            agent_prof_code = AgentProfileModel.objects.get(agent = user).agent_code


        refresh = RefreshToken.for_user(user)

        user_type = 0 if user.user_type=="super admin" else 1 if user.user_type=="admin" else 2 if user.user_type=="sales agent" else 3 if user.user_type=="collection agent" else 4 if user.user_type=="sales and collection agent" else 5 if user.user_type=="customer" else None

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_type":str(user_type),
            "name": str(user.first_name) + " "+ str(user.last_name) or user.username.split('@')[0],
            "position": user.user_type,
            "agent_code": str(agent_prof_code)
        }, status=status.HTTP_200_OK)
    
class ShareMyInterestView(APIView):
    
    def post(self,request):
        serializer = ShareMyInterestModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        return Response({"success":"Your request has been sent successfully"})
    
class GetShareMyInterest(APIView):
    
    permission_classes = [IsAdminUser,IsAuthenticated]

    def get(self,request):
        all_interest = ShareMyInterestModel.objects.all()
        if all_interest:
            serializer = ShareMyInterestModelSerializer(all_interest,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"error":"Data doesn't exist"},status=status.HTTP_400_BAD_REQUEST)
    
class CustomerFetch(TemplateView):

    permission_classes= [IsAuthenticated,IsAdminUser]
    template_name = "style.html"

class UserProfileView(APIView):

    permission_classes = [IsAgent]

    def get(self,request):
        try:
            user_data = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response({"error":"Agent doesn't exist"},status=status.HTTP_400_BAD_REQUEST)
        serializer = UserProfileGetSerailzer(user_data,many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)