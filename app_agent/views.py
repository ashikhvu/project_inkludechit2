from django.shortcuts import render
from rest_framework.views import APIView
from app_inkludechit.models import SalePunchModel
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework import status
from app_inkludechit.serializers import SalePunchCreationSerializer
from rest_framework.response import Response

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