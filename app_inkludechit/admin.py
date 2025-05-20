from django.contrib import admin
from .models import User,UserProfileModel,NomineeModel,ProductModel,PaymentModel,ShareMyInterestModel

# Register your models here.

class productsetup(admin.ModelAdmin):
    list_display=["kuri_type","product_code","document_type","collection_mode","joining_date"]

class userprof(admin.ModelAdmin):
    list_display=["first_name","email","mobile","current_address"]

class shareinterestsetup(admin.ModelAdmin):
    list_display=["get_customer_name","customer_email","custoemr_comment","customer_country_code","customer_phone"]

    def get_customer_name(self,obj):
        return obj.customer_name.title() if obj.customer_name else ""
    get_customer_name.short_description = "first name"

admin.site.register(User)
admin.site.register(UserProfileModel,userprof)
admin.site.register(NomineeModel)
admin.site.register(ProductModel,productsetup)
admin.site.register(ShareMyInterestModel,shareinterestsetup)