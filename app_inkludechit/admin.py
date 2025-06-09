from django.contrib import admin
from .models import User,SalePunchModel,NomineeModel,ProductModel,PaymentModel,ShareMyInterestModel,CustomerProfileModel,LiabilitiesModel
from .models import AgentProfileModel,BankListModel,PaidModel,UnpaidModel,OtherModel,CollectionModel
# Register your models here.

class productsetup(admin.ModelAdmin):
    list_display=["kuri_type","product_code","document_type","collection_mode","joining_date"]
    list_display_links = list_display

class salepunchmodel(admin.ModelAdmin):
    list_display=["id","get_customer_prof","place","adhar_no","current_address"]
    list_display_links = list_display

    def get_customer_prof(self,obj):
        return  obj.customer.first_name
    get_customer_prof.short_description = ""

class shareinterestsetup(admin.ModelAdmin):
    list_display=["id","get_customer_name","customer_email","custoemr_comment","customer_country_code","customer_phone"]
    list_display_links = list_display

    def get_customer_name(self,obj):
        return obj.customer_name.title() if obj.customer_name else ""
    get_customer_name.short_description = "first name"

class customerprofileclass(admin.ModelAdmin):
    list_display = ["id","mobile_no","email","amount","reciept_no","agent","agent_id"]
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

class liabilitysetup(admin.ModelAdmin):
    list_display = ["id","get_bank_name","amount","emi_amount","salepunch_id"]
    list_display_links = list_display

    def get_bank_name(self,obj):
        return obj.bank_name.upper()
    get_bank_name.short_description = "BANK NAME"

class bankmodel_setup(admin.ModelAdmin):
    list_display = ["id","bank_name"]
    list_display_link = list_display
    
class PaidModelSetup(admin.ModelAdmin):
    list_display = ["id","paid_amount","paid_trans_type"]
    list_display_links = list_display

class UnpaidModelSetup(admin.ModelAdmin):
    list_display = ["id","unpaid_reason_choices","unpaid_pos_next_pend_pay_choices"]
    list_display_links = list_display

class OtherModelSetup(admin.ModelAdmin):
    list_display = ["id","other_remarks","other_res_date"]
    list_display_links = list_display

class CollectionModelSetup(admin.ModelAdmin):
    list_display = ["id","cm_full_name","cm_next_date_and_time"]
    list_display_links = list_display


admin.site.register(User,Usersetup)
admin.site.register(SalePunchModel,salepunchmodel)
admin.site.register(NomineeModel)
admin.site.register(ProductModel,productsetup)
admin.site.register(ShareMyInterestModel,shareinterestsetup)
admin.site.register(CustomerProfileModel,customerprofileclass)
admin.site.register(AgentProfileModel,AgentSetup)
admin.site.register(LiabilitiesModel,liabilitysetup)
admin.site.register(BankListModel,bankmodel_setup)
admin.site.register(PaidModel,PaidModelSetup)
admin.site.register(UnpaidModel,UnpaidModelSetup)
admin.site.register(OtherModel,OtherModelSetup)
admin.site.register(CollectionModel,CollectionModelSetup)