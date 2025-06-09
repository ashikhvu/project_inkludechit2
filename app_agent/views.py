from django.shortcuts import render
from rest_framework.views import APIView
from app_inkludechit.models import SalePunchModel,CustomerProfileModel,User,AgentProfileModel,CollectionModel
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework import status
from app_inkludechit.serializers import SalePunchCreationSerializer,GetAllRegisteredCustomerSerializer,PartialFetchSelectedRegisteredCustomerSerializer
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from dateutil.relativedelta import relativedelta
import datetime

class IsAdminOrIsStaff(BasePermission):
    def has_permission(self,request,view):
        return request.user and request.user.is_authenticated and (request.user.user_type in ["admin","super admin"] or request.user.user_type in ["sales agent","sales and collection agent"])

class IsSalesAgent(BasePermission):
    def has_permission(self,request,view):
        return request.user and request.user.is_authenticated and request.user.user_type =="sales agent"

class SalePunchViewPost(APIView):

    permission_classes = [IsAdminOrIsStaff]

    def post(self, request):
        serializer = SalePunchCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["agent"] = request.user
            serializer.save()

            val_data = serializer.validated_data

            if val_data:
                kuri_type=val_data["product_model_data"]["kuri_type"]
                product_code=val_data["product_model_data"]["product_code"]
                document_type=val_data["product_model_data"]["document_type"]
                chit_duration=val_data["product_model_data"]["chit_duration"]
                first_emi_completion_date=val_data["product_model_data"]["first_emi_completion_date"]
                last_emi_date=val_data["product_model_data"]["last_emi_date"]
                auction_eligibility=val_data["product_model_data"]["auction_eligibility"]
                auction_date=val_data["product_model_data"]["auction_date"]
                divident_date=val_data["product_model_data"]["divident_date"]

                # print(f"{kuri_type}\n{product_code}\n{document_type}\n{chit_duration}\n{first_emi_completion_date}\n{last_emi_date}\n{auction_eligibility}\n{auction_date}\n{divident_date}")


                if kuri_type=="auction":
                    print(f"inside auction")
                    if document_type == "collateral":

                        first_emi_completion_date
                        for i in range(40):
                            # print(f"\n{i}")
                            future_emi_date = first_emi_completion_date+relativedelta(months=i+1)
                            next_emi_date = first_emi_completion_date+relativedelta(months=i+2)
                            CollectionModel.objects.get_or_create(
                                # cm_agent_data=
                                cm_full_name=f"name {i}",
                                cm_next_date_and_time=next_emi_date
                            )

            return Response({"success":"SalePunch submitted successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class GetAllRegisteredCustomerView(APIView):

    permission_classes = [IsAdminOrIsStaff]

    def get(self,request):
        user_type = request.user.user_type
        print(user_type)
        if user_type in ["admin","super admin"]:
            cust = CustomerProfileModel.objects.filter(is_salepunch_created=False)
            serializer = GetAllRegisteredCustomerSerializer(cust,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif user_type in ["sales agent","sales and collection agent"]:
            try:
                print("trying")
                user = User.objects.get(id=request.user.id)
                agent_prof = AgentProfileModel.objects.get(agent=user)
                print(f"agent id : {agent_prof.id}")
            except User.DoesNotExist:
                return Response({"error","User doesn't exist"})
            except AgentProfileModel.DoesNotExist:
                return Response({"error","Agent Profile doesn't exist"})

            cust = CustomerProfileModel.objects.filter(agent=agent_prof,is_salepunch_created=False)
            print(cust)
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
            agent_prof = AgentProfileModel.objects.get(agent = request.user)
            if request.user.user_type not in ["admin","super admin"]:
                if cust_prof.agent!=agent_prof:
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
            print(cust_prof)
            serializer = PartialFetchSelectedRegisteredCustomerSerializer(cust_prof,many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except CustomerProfileModel.DoesNotExist:
            return Response({"error":"Customer details doesn't exist"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error",str(e)},status=status.HTTP_400_BAD_REQUEST)
