from django.shortcuts import render
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from app_inkludechit.models import SalePunchModel
from app_inkludechit.serializers import SalePunchCreationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.

class SalePunchViewListGet(APIView):

    permission_classes = [IsAdminUser,IsAuthenticated]

    def get(self, request):
        profile = SalePunchModel.objects.all()
        print(profile)
        if profile:
            serializer = SalePunchCreationSerializer(profile, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"error":"Data unavailable"},status=status.HTTP_200_OK)
