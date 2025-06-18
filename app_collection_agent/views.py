from django.shortcuts import render
from rest_framework.views import APIView
from app_inkludechit.serializers import GetAllRegisteredCustomerSerializer,GetAllRegisteredCustomersNameandPhSerializer
from app_inkludechit.models import CustomerProfileModel,AgentProfileModel,SalePunchModel,CollectionModel,LastVisitDetailsModel
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission,IsAdminUser,IsAuthenticated
from datetime import datetime
from django.http import JsonResponse

class IsCollectionAgent(BasePermission):
    def has_permission(self,request,view):
        return request.user and request.user.is_authenticated and request.user.user_type == "collection agent"

# Create your views here.
class GetEformCompletedCustomer(APIView):

    permission_classes = [IsCollectionAgent]

    def get(self,request):
        try:
            cust_prof = CustomerProfileModel.objects.filter(is_salepunch_created=True)
        except CustomerProfileModel.DoesNotExist:
            return Response({"error":"Customer Details doesn't exist"},status=status.HTTP_400_BAD_REQUEST)
        serialzer = GetAllRegisteredCustomerSerializer(cust_prof,many=True)
        return Response(serialzer.data,status=status.HTTP_200_OK)
    
class GetAllEformCompletedCustomersNameandPh(APIView):

    permission_classes = [IsCollectionAgent]

    def get(self,request):
        try:
            cust_prof = CustomerProfileModel.objects.filter(is_salepunch_created=True)
        except CustomerProfileModel.DoesNotExist:
            return Response({"error":"Customer Details doesn't exist"},status=status.HTTP_400_BAD_REQUEST)
        serialzer = GetAllRegisteredCustomersNameandPhSerializer(cust_prof,many=True)
        return Response(serialzer.data,status=status.HTTP_200_OK)
    
class CustomerDetailsForCollectionAgent(APIView):

    permission_classes = [IsCollectionAgent]
    
    def get(self,request):
        try:
            cust_prof_id = request.GET.get("id")
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        if not cust_prof_id:
            return Response({"error":"please provide an id"},status=status.HTTP_400_BAD_REQUEST)
        
        try:    
            cust_prof = CustomerProfileModel.objects.get(id=cust_prof_id)
        except CustomerProfileModel.DoesNotExist:
            return Response({"error":"customer profile doesn't exist"})
        
        try:
            sp=SalePunchModel.objects.get(customer_prof=cust_prof)
        except SalePunchModel.DoesNotExist:
            return Response({"error":"Salepunch detail not found for the specific customer"})
        

        # basic details---------------------------
        kyc = sp.kyc
        uid = sp.uid
        group = sp.product_model_data.product_code
        # batch = 

        current_date = datetime.today().date()
        print(current_date)
        print(f"-----------------\n\nmonth={current_date.month:02d}\n\n-----------------")
        current_month = f"{current_date.month:02d}"

        try:
            collection_data = CollectionModel.objects.filter(cm_customer_prof_data__id=cust_prof_id,cm_current_date_and_time__month=current_month).first()
        except CollectionModel.DoesNotExist:
            return Response({"error":"collection model data doesn't exist"},status=status.HTTP_400_BAD_REQUEST)    
        

        try:
            prev_collection_data = CollectionModel.objects.filter()
        except CollectionModel.DoesNotExist:
            return Response({"error":"Colection model data doesn't exist"})
            



        print(f"query : {collection_data}")

        # emi details--------------------------
        reminder_date = collection_data.cm_reminder_date
        fixed_date = collection_data.cm_current_date_and_time
        collection_count = collection_data.cm_collection_count
        unit_amount = collection_data.cm_unit_amount
        unit_sum = collection_data.cm_unit_sum
        emi_count = collection_data.cm_emi_count
        payable_date_emi = collection_data.cm_payable_date_emi
        emi_bounce_date = collection_data.cm_emi_bounce_date

        # prev details-----------------------------
        last_visited_data = None
        
        try:
            last_visited_data = LastVisitDetailsModel.objects.filter(ls_customer_prof_data=cust_prof).first()
        except LastVisitDetailsModel.DoesNotExist:
            return Response({"error":"Last visit details not found"},status=status.HTTP_400_BAD_REQUEST)
        
        print(f"============================\n{last_visited_data}\n==========================")


        last_visited_details_id=last_visit_count=last_visit_date=last_visit_status=last_unit_amount=None
        if last_visited_data:
            last_visited_details_id = last_visited_data.id
            last_visit_count = last_visited_data.ls_visit_count
            last_visit_date = last_visited_data.ls_visit_date
            last_visit_status = last_visited_data.ls_visit_status
            last_unit_amount = last_visited_data.ls_unit_amount

        customer_data = {
            "basic_details":{
                "kyc":str(kyc),
                "uid":str(uid),
            },
            "emi_details":{
                "remider_date":str(reminder_date),
                "fixed_date":str(fixed_date),
                "collection_count":str(collection_count),
                "unit_amount":str(unit_amount),
                "unit_sum":str(unit_sum),
                "emi_count":str(emi_count),
                "payable_date_emi":str(payable_date_emi),
                "emi_bounce_date":str(emi_bounce_date)
            },
            "previous_visit_details":{
                "last_visited_details_id": str(last_visited_details_id),
                "last_visit_count":str(last_visit_count),
                "last_visit_date":str(last_visit_date),
                "last_visit_status":str(last_visit_status),
                "last_unit_amount":str(last_unit_amount)
            }
        }

        print(f"\n{cust_prof_id}\n{cust_prof}\n{current_date}")
        
        return JsonResponse(customer_data,status=status.HTTP_200_OK)
    
class CollectionPost(APIView):
     
    permission_classes = [IsCollectionAgent]

    def post(self,request):

        try:
            id = request.data.get('id')
        except:
            return 

        cm = CollectionModel.objects.get(id=id)

        print(cm)
        return Response({"succes":"Collection model created"},status=status.HTTP_200_OK)
