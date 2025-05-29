from django.contrib import admin
from .models import User,SalePunchModel,NomineeModel,ProductModel,PaymentModel,ShareMyInterestModel,CustomerProfileModel
from .models import AgentProfileModel
# Register your models here.

class productsetup(admin.ModelAdmin):
    list_display=["kuri_type","product_code","document_type","collection_mode","joining_date"]
    list_display_links = list_display

class salepunchmodel(admin.ModelAdmin):
    list_display=["get_customer_prof","place","adhar_no","current_address"]
    list_display_links = list_display

    def get_customer_prof(self,obj):
        return  obj.full_name
    get_customer_prof.short_description = "FULL_NAME"

class shareinterestsetup(admin.ModelAdmin):
    list_display=["get_customer_name","customer_email","custoemr_comment","customer_country_code","customer_phone"]
    list_display_links = list_display

    def get_customer_name(self,obj):
        return obj.customer_name.title() if obj.customer_name else ""
    get_customer_name.short_description = "first name"

class customerprofileclass(admin.ModelAdmin):
    list_display = ["id","customer_name","mobile_no","email","amount","reciept_no","agent","agent_id"]
    list_display_links = list_display

    def agent_id(self,obj):
        return obj.agent.id
    agent_id.short_description = "Agent Id"


class Usersetup(admin.ModelAdmin):
    list_display = ["id","email","mobile","user_type"]
    list_display_links = list_display

class AgentSetup(admin.ModelAdmin):
    list_display = ["id","agent_code","agent_email"]
    list_display_links = list_display

    def agent_email(self,obj):
        return obj.agent.email
    agent_email.short_description = "Agent Email"

admin.site.register(User,Usersetup)
admin.site.register(SalePunchModel,salepunchmodel)
admin.site.register(NomineeModel)
admin.site.register(ProductModel,productsetup)
admin.site.register(ShareMyInterestModel,shareinterestsetup)
admin.site.register(CustomerProfileModel,customerprofileclass)
admin.site.register(AgentProfileModel,AgentSetup)