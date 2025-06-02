from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User,SalePunchModel,ShareMyInterestModel,AgentProfileModel
from .serializers import SalePunchCreationSerializer,CustomTokenObtainPairSerializer,CustomUserLoginSerializer,SendOtpSerializer,ShareMyInterestModelSerializer
from rest_framework import status
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from twilio.rest import Client
from django.conf import settings
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.views.generic import TemplateView


# Create your views here.
# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
        

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
            "agent_name": user.first_name or user.username.split('@')[0],
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

    
