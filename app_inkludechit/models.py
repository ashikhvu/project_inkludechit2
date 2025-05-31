from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.core.validators import RegexValidator,MinValueValidator,MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from shortuuid.django_fields import ShortUUIDField
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta

class UserManager(BaseUserManager):
    def create_user(self,email=None,mobile=None,password=None,**extra_fields):
        if not email and not mobile:
            raise ValueError("The Email or Mobile must be set")

        if email:
            extra_fields['email']=self.normalize_email(email)

        # to avoid duplicate email or mobile attributevalue
        extra_fields.pop('email',None)
        extra_fields.pop('mobile',None)

        email = self.normalize_email(email) if email else None

        user = self.model(email=email,mobile=mobile,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_superuser(self,email=None,mobile=None,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        # to avoid duplicate email or mobile attributevalue
        extra_fields.pop('email',None)
        extra_fields.pop('mobile',None)
        return self.create_user(email=email,mobile=mobile,password=password,**extra_fields)

# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=255,blank=True,null=True)
    user_type_choices = (
        ('admin','admin'),
        ('super admin','super admin'),
        ('sales agent','sales agent'),
        ('collection agent','collection agent'),
        ('sales and collection agent','sales and collection agent'),
        ('customer','customer'),
    )
    user_type = models.CharField(max_length=255,choices=user_type_choices,default='customer',blank=True,null=True)
    first_name = models.CharField(max_length=255,blank=True,null=True)
    last_name = models.CharField(max_length=255,blank=True,null=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10,unique=True,validators=[RegexValidator(
        regex=r"^\d{10}",
        message="Please Provide a 10 digit number"
    )])

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects= UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile']

    def __str__(self):
        return str(self.username or self.email or "User")
    
    def save(self,*args,**kwargs):
        if self.email:
            user_name,mob_name = self.email.split('@')
            if self.first_name == '' or self.first_name == None:
                self.first_name = user_name
            if self.username == '' or self.username == None:
                self.username = user_name
        super(User,self).save(*args,**kwargs)
    

# AGENT MODELS START*****************************************************************************************

class AgentProfileModel(models.Model):
    agent = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    agent_code = ShortUUIDField(max_length=6,length=4,alphabet="0123456789",unique=True,blank=True,null=True)

    def __str__(self):
        return "AgentProfile "+str(self.id)

@receiver(post_save,sender=User)
def create_agent_profile(sender,instance,created,**kwargs):
    if created: 
        if instance.user_type in ["sales agent","sales and collection agent"]:
            AgentProfileModel.objects.create(agent=instance)
        elif instance.user_type in ["sales agent","sales and collection agent"]:
            try: 
                agent_instance = AgentProfileModel.objects.get(agent=instance)
            except AgentProfileModel.DoesNotExist():
                AgentProfileModel.objects.create(agent=instance)

@receiver(post_save,sender=User)
def save_agent_profile(sender,instance,**kwargs):
    if hasattr(instance,"agentprofilemodel"):
        instance.agentprofilemodel.save()

# AGENT MODELS END*******************************************************************************************



# CUSTOMER MODELS START****************************************************************************************

class CustomerProfileModel(models.Model):
    agent = models.ForeignKey(AgentProfileModel,on_delete=models.CASCADE,blank=True,null=True)
    customer = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    customer_name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=10,validators=[
        RegexValidator(
            regex=r"\d{10}$",
            message="Enter a 10 digit valid number"
        )]
    )
    whatsapp_no = models.CharField(max_length=10,validators=[
        RegexValidator(
            regex=r"\d{10}$",
            message="Enter a 10 digit valid number"
        )]
    )
    email = models.EmailField()
    amount = models.FloatField(default=0.00)
    reciept_no = models.CharField(max_length=12,unique=True)
    customer_otp = models.CharField(max_length=4,blank=True,null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_name or self.email.split('@')[0]

class OtpRecordModel(models.Model):
    mobile_no = models.CharField(max_length=10,validators=[
        RegexValidator(
            regex=r"^\d{10}",
            message="Enter a 10 digit number"
        )
    ])
    otp = models.CharField(max_length=4,blank=True,null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return (timezone.now() - self.create_at )< timedelta(minutes=3)

# CUSTOMER MODELS END****************************************************************************************

class NomineeModel(models.Model):
    nominee_name = models.CharField(max_length=255,blank=True,null=True)
    nominee_relation = models.CharField(max_length=255,blank=True,null=True)    
    nominee_address = models.TextField(blank=True,null=True)
    nominee_contact = models.CharField(max_length=10,blank=True,null=True,validators=[
        RegexValidator(
            regex=r'^\d{10}$',
            message='Enter a valid 10-digit phone number.'
        )
    ])
    def __str__(self):
        return str(self.nominee_name)

class ProductModel(models.Model):
    kuri_type_choices = (
        ('auction','auction'),
        ('draw','draw'),
        ('offer','offer'),
        ('multi division','multi division'),
    )
    kuri_type = models.CharField(max_length=50,choices=kuri_type_choices,default="auction",blank=True,null=True)
    product_code_choices = (
        ('301','301'),
        ('801','801'),

        ('201','201'),
        ('202','202'),

        ('901','901'),
        ('902','902'),
        ('903','903'),
        ('904','904'),
        ('951','951'),
        ('952','952'),

        ('502','502'),
    )
    product_code = models.PositiveIntegerField(validators=[MinValueValidator(111),MaxValueValidator(999)],blank=True,null=True)
    document_type_choices = (
        ('collateral','collateral'),
        ('noncollateral','noncollateral'),
    )
    document_type = models.CharField(max_length=100,choices=document_type_choices,default='collateral',blank=True,null=True)
    collection_mode_choices = (
        ('daily','daily'),
        ('weekly','weekly'),
        ('monthly','monthly'),
    )
    collection_mode = models.CharField(max_length=50,choices=collection_mode_choices,default='daily',blank=True,null=True)
    joining_date = models.DateField(blank=True,null=True)
    first_emi_completion_date = models.DateField(blank=True,null=True)
    chit_duration = models.CharField(max_length=50,blank=True,null=True)
    last_emi_date = models.DateField(blank=True,null=True)
    auction_eligibility = models.CharField(max_length=255, blank=True,null=True)
    auction_date = models.PositiveIntegerField(blank=True,null=True)
    divident_date= models.PositiveIntegerField(blank=True,null=True)
    
    draw_date = models.PositiveIntegerField(blank=True,null=True)
    dispatching_committed_date = models.DateField(blank=True,null=True)

    multi_division_auction_eligibility = models.DateField(blank=True,null=True)
    multi_division_auction_date = models.CharField(max_length=100,blank=True,null=True)
    multi_division_divident_date = models.CharField(max_length=100,blank=True,null=True)

class PaymentModel(models.Model):
    payment_mode_choices = (
        ('online','online'),
        ('direct','direct'),
    )
    payment_mode = models.CharField(max_length=255,choices=payment_mode_choices,default='online',blank=True,null=True)
    collection_area = models.CharField(max_length=255,blank=True,null=True)
    collection_point = models.PositiveIntegerField(blank=True,null=True)
    collection_start_date = models.DateField(blank=True,null=True)
    customer_committed_day = models.PositiveIntegerField(blank=True,null=True,validators=[
        MinValueValidator(1),
        MaxValueValidator(30)
    ])
    forman_commision = models.CharField(max_length=50,blank=True,null=True)
    upi_number = models.CharField(max_length=50,blank=True,null=True)

class SalePunchModel(models.Model):
    # basic info
    agent = models.ForeignKey(User,on_delete=models.CASCADE,related_name="agent",blank=True,null=True)
    customer = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    customer_prof = models.ForeignKey(CustomerProfileModel,on_delete=models.CASCADE,blank=True,null=True)
    # uid = ShortUUIDField(unique=True,length=10,max_length=12,alphabet='0123456789',blank=True,null=True)
    uid = models.CharField(unique=True,max_length=12,blank=True,null=True,validators=[
        RegexValidator(
            regex=r"^\d{12}",
            message="UID should be 12 digit"
        )
    ])
    kyc = models.CharField(unique=True,max_length=12,blank=True,null=True,validators=[
        RegexValidator(
            regex=r"^\d{12}",
            message="KYC number should be 12 digit"
        )
    ])
    # kyc = ShortUUIDField(unique=True,length=10,max_length=12,alphabet='0123456789',blank=True,null=True)
    agent_code = models.CharField(max_length=4,blank=True,null=True)
    full_name = models.CharField(max_length=255,blank=True,null=True)
    # last_name = models.CharField(max_length=255,blank=True,null=True)
    family_name = models.CharField(max_length=255,blank=True,null=True)
    # email = models.EmailField(blank=True,null=True)
    # mobile = models.CharField(max_length=10,blank=True,null=True,validators=[
    #     RegexValidator(
    #         regex=r'^\d{10}$',
    #         message='Enter a valid 10-digit phone number.'
    #     )
    # ])
    # whatsapp = models.CharField(max_length=10,blank=True,null=True,validators=[
    #     RegexValidator(
    #         regex=r'^\d{10}$',
    #         message='Enter a valid 10-digit phone number.'
    #     )
    # ])
    place = models.CharField(max_length=255,blank=True,null=True)
    # dob = models.DateField(blank=True,null=True)
    pancard_no = models.CharField(max_length=10,validators=[
        RegexValidator(regex=r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$",
                       message="Invalid Pancard Number")
    ],blank=True)
    adhar_no = models.CharField(max_length=12,validators=[
        RegexValidator(regex=r"^\d{12}$",
                       message="Adhar card number must be 12 digits")
    ],blank=True)

    # address info
    current_address = models.TextField(blank=True,null=True)
    permenent_address = models.TextField(blank=True,null=True)
    postal_address = models.TextField(blank=True,null=True)

    maritial_status_choices = (
        ("married","married"),
        ("single","single"),
        ("divorced","divorced"),
    )
    marital_status = models.CharField(max_length=255,default="single",choices=maritial_status_choices,blank=True,null=True)
    
    # proffesional_details
    company_address = models.TextField(blank=True,null=True)
    company_pincode = models.CharField(max_length=50,blank=True,null=True)
    designation = models.CharField(max_length=50,blank=True,null=True)
    period_of_work = models.PositiveIntegerField(blank=True,null=True)
    working_time = models.PositiveIntegerField(blank=True,null=True,validators=[
        MinValueValidator(1),
        MaxValueValidator(12)
    ])
    
    # salary details
    salary_date = models.DateField(blank=True,null=True)
    salary_mode_choices = (
        ('through bank account','through bank account'),
        ('cash in hands','cash in hands'),
    )
    company_salary_mode = models.CharField(max_length=255,blank=True,null=True,default='through bank account',choices=salary_mode_choices)
    company_contact_no = models.CharField(max_length=10,blank=True,null=True,validators=[
        RegexValidator(regex=r"^\d{10}$",
                       message='Enter a valid 10-digit phone number.')
    ])
    company_reference_mobile_no = models.CharField(max_length=10,blank=True,null=True,validators=[
        RegexValidator(regex=r"^\d{10}$",
                       message='Enter a valid 10-digit phone number.')
    ])
    company_partner_detail = models.CharField(max_length=255,blank=True,null=True)

    signature_field = models.FileField(upload_to="signature/",blank=True,null=True)
    video_field = models.FileField(upload_to="video/",blank=True,null=True)

    nominee_model_data = models.ForeignKey(NomineeModel,on_delete=models.CASCADE,blank=True,null=True)
    product_model_data = models.ForeignKey(ProductModel,on_delete=models.CASCADE,blank=True,null=True)
    payment_model_data = models.ForeignKey(PaymentModel,on_delete=models.CASCADE,blank=True,null=True)

class LiabilitiesModel(models.Model):
    salepunch = models.ForeignKey(SalePunchModel,on_delete=models.CASCADE,blank=True,null=True)
    # current liabilities
    bank_name = models.CharField(max_length=255,blank=True,null=True)
    amount = models.FloatField(default=0.0)
    emi_amount = models.FloatField(default=0.0)

    def __str__(self):
        return self.bank_name

class ShareMyInterestModel(models.Model):
    customer_name = models.CharField(max_length=255,blank=True,null=True)
    customer_email = models.EmailField(unique=True,blank=True,null=True)
    custoemr_comment = models.TextField(default='',blank=True,null=True)
    customer_country_code = models.CharField(max_length=50,blank=True,null=True,default='+91')
    customer_phone = models.CharField(max_length=10,unique=True,validators=[RegexValidator(
        regex=r"^\d{10}$",
        message="Enter a valid 10 digit phone number"
    )])

    def __str__(self):
        return self.customer_name or self.customer_email


    






# @receiver(post_save,sender=User)
# def create_customer_profile(sender,instance,created,**kwargs):
#     if created:
#         print(instance.customer_type)

# @receiver(post_save,sender=User)
# def create_profile_details(sender,instance,created,**kwargs):
#     if created:
#         SalePunchModel.objects.create(
#             user=instance,
#         )

# @receiver(post_save,sender=User)
# def save_user_profile(sender,instance,**kwargs):
#     if hasattr(instance,'salepunchmodel'):
#         instance.salepunchmodel.save()

# otp send 
# view function , serializer and url creation completed
# authenticate otp
# view function , serializer and url creation completed
# create customer
# view function , serializer and url creation completed
# combined otp authentication and customer temp creation view function,serailizer and url

