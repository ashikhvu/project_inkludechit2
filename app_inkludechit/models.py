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
    

# BANK MODEL START
class BankListModel(models.Model):
    indian_banks_choices = (
        # Public Sector Banks (12)
        ("State Bank of India", "State Bank of India"),
        ("Bank of Baroda", "Bank of Baroda"),
        ("Bank of India", "Bank of India"),
        ("Bank of Maharashtra", "Bank of Maharashtra"),
        ("Canara Bank", "Canara Bank"),
        ("Central Bank of India", "Central Bank of India"),
        ("Indian Bank", "Indian Bank"),
        ("Indian Overseas Bank", "Indian Overseas Bank"),
        ("Punjab National Bank", "Punjab National Bank"),
        ("Punjab & Sind Bank", "Punjab & Sind Bank"),
        ("UCO Bank", "UCO Bank"),
        ("Union Bank of India", "Union Bank of India"),

        # Private Sector Banks (21)
        ("HDFC Bank", "HDFC Bank"),
        ("ICICI Bank", "ICICI Bank"),
        ("Axis Bank", "Axis Bank"),
        ("Kotak Mahindra Bank", "Kotak Mahindra Bank"),
        ("IndusInd Bank", "IndusInd Bank"),
        ("IDFC FIRST Bank", "IDFC FIRST Bank"),
        ("Bandhan Bank", "Bandhan Bank"),
        ("CSB Bank", "CSB Bank"),
        ("City Union Bank", "City Union Bank"),
        ("DCB Bank", "DCB Bank"),
        ("Dhanlaxmi Bank", "Dhanlaxmi Bank"),
        ("Federal Bank", "Federal Bank"),
        ("Jammu & Kashmir Bank", "Jammu & Kashmir Bank"),
        ("Karnataka Bank", "Karnataka Bank"),
        ("Karur Vysya Bank", "Karur Vysya Bank"),
        ("Nainital Bank", "Nainital Bank"),
        ("South Indian Bank", "South Indian Bank"),
        ("Tamilnad Mercantile Bank", "Tamilnad Mercantile Bank"),
        ("Yes Bank", "Yes Bank"),
        ("RBL Bank", "RBL Bank"),
        ("Lakshmi Vilas Bank", "Lakshmi Vilas Bank"),

        # Foreign Banks
        ("Citibank", "Citibank"),
        ("HSBC", "HSBC"),
        ("Standard Chartered", "Standard Chartered"),
        ("Deutsche Bank", "Deutsche Bank"),
        ("Barclays", "Barclays"),
        ("BNP Paribas", "BNP Paribas"),
        ("Bank of America", "Bank of America"),
        ("DBS Bank", "DBS Bank"),
        ("Societe Generale", "Societe Generale"),

        # Payments Banks
        ("Airtel Payments Bank", "Airtel Payments Bank"),
        ("Fino Payments Bank", "Fino Payments Bank"),
        ("India Post Payments Bank", "India Post Payments Bank"),
        ("NSDL Payments Bank", "NSDL Payments Bank"),
        ("Paytm Payments Bank", "Paytm Payments Bank"),

        # Small Finance Banks
        ("AU Small Finance Bank", "AU Small Finance Bank"),
        ("Equitas Small Finance Bank", "Equitas Small Finance Bank"),
        ("Fincare Small Finance Bank", "Fincare Small Finance Bank"),
        ("ESAF Small Finance Bank", "ESAF Small Finance Bank"),
        ("Ujjivan Small Finance Bank", "Ujjivan Small Finance Bank"),
        ("Utkarsh Small Finance Bank", "Utkarsh Small Finance Bank"),
        ("Suryoday Small Finance Bank", "Suryoday Small Finance Bank"),
        ("Jana Small Finance Bank", "Jana Small Finance Bank"),
        ("North East Small Finance Bank", "North East Small Finance Bank"),
        ("Shivalik Small Finance Bank", "Shivalik Small Finance Bank"),
        ("Capital Small Finance Bank", "Capital Small Finance Bank"),

        # Local Area Banks
        ("Coastal Local Area Bank Ltd", "Coastal Local Area Bank Ltd"),
        ("Krishna Bhima Samruddhi LAB Ltd", "Krishna Bhima Samruddhi LAB Ltd"),
    )
    bank_name = models.CharField(max_length=255,default="State Bank of India",choices=indian_banks_choices,blank=True,null=True)

    def __str__(self):
        return self.bank_name

# BANK MODEL END


# AGENT MODELS START*****************************************************************************************

class AgentProfileModel(models.Model):
    agent = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    agent_code = ShortUUIDField(max_length=6,length=4,alphabet="0123456789",unique=True,blank=True,null=True)

    def __str__(self):
        return "AgentProfile "+str(self.id)

@receiver(post_save,sender=User)
def create_agent_profile(sender,instance,created,**kwargs):
    if created: 
        if instance.user_type in ["sales agent","collection agent","sales and collection agent"]:
            AgentProfileModel.objects.create(agent=instance)
        elif instance.user_type in ["sales agent","collection agent","sales and collection agent"]:
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
    # customer_name = models.CharField(max_length=255)
    customer_first_name = models.CharField(max_length=255,blank=True,null=True)
    customer_last_name = models.CharField(max_length=255,blank=True,null=True)
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
    is_salepunch_created = models.BooleanField(default=False,blank=True,null=True)

    def __str__(self):
        return str(self.customer_first_name)+str(self.customer_last_name) or self.email.split('@')[0]

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
        ('non collateral','non collateral'),
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
    first_name = models.CharField(max_length=255,blank=True,null=True)
    last_name = models.CharField(max_length=255,blank=True,null=True)
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

# ==========================================================================================================
#                                        COLLECTION MODELS START  
# ==========================================================================================================

class PaidModel(models.Model):
    paid_agent_data = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="paid_agent_data")
    paid_customer_data = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    paid_customer_prof_data = models.ForeignKey(CustomerProfileModel,on_delete=models.CASCADE,blank=True,null=True)

    paid_amount = models.FloatField(default=0.0,blank=True,null=True)
    paid_trans_type_choices = (
        ("cash","cash"),
        ("bank","bank"),
        ("cheque","cheque")
    )
    paid_trans_type = models.CharField(max_length=100,default="cash",choices=paid_trans_type_choices,blank=True,null=True)
    paid_pay_type_choices = (
        ("fixed amount","fixed amount"),
        ("minimum required amount","minimum required amount")
    )
    paid_pay_type = models.CharField(max_length=100,choices=paid_pay_type_choices,blank=True,null=True)
    paid_next_pay_date = models.DateTimeField(blank=True,null=True)
    paid_created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return self.paid_amount
    
class UnpaidModel(models.Model):
    unpaid_agent_data = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="unpaid_agent_data")
    unpaid_customer_data = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    unpaid_customer_prof_data = models.ForeignKey(CustomerProfileModel,on_delete=models.CASCADE,blank=True,null=True)

    unpaid_reason_choices = (
        ("income date & collection date variation","income date & collection date variation"),
        ("rescentment of not getting kuri","rescentment of not getting kuri"),
        ("unexpected expenses","unexpected expenses"),
        ("payment unscheduled","payment unscheduled"),
        ("current over liability","current over liability"),
        ("unstructured financial behaviour","unstructured financial behaviour")
    )
    unpaid_reason = models.CharField(max_length=255,blank=True,null=True)
    unpaid_pos_next_pend_pay_choices = (
        ("salary/income","salary/income"),
        ("anticipating money","anticipating money"),
        ("borrowed","borrowed"),
        ("money rolling","money rolling"),
        ("better financial profile","better financial profile"),
    )
    unpaid_pos_next_pend_pay = models.CharField(max_length=100,choices=unpaid_pos_next_pend_pay_choices,blank=True,null=True)
    unpaid_res_date = models.DateTimeField(blank=True,null=True)
    unpaid_created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return self.unpaid_reason

class OtherModel(models.Model):
    other_agent_data = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="other_agent_data")
    other_customer_data = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    other_customer_prof_data = models.ForeignKey(CustomerProfileModel,on_delete=models.CASCADE,blank=True,null=True)

    other_remarks = models.TextField(blank=True,null=True)
    other_res_date = models
    other_created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return self.other_remarks

class CollectionModel(models.Model):
    cm_agent_data = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="cm_agent_data")
    cm_customer_data = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    cm_customer_prof_data = models.ForeignKey(CustomerProfileModel,on_delete=models.CASCADE,blank=True,null=True)
    cm_salepunch_data = models.ForeignKey(SalePunchModel,on_delete=models.CASCADE,blank=True,null=True)

    cm_kyc = models.CharField(unique=True,max_length=12,blank=True,null=True,validators=[
        RegexValidator(
            regex=r"^\d{12}",
            message="KYC number should be 12 digit"
        )
    ])
    cm_uid = models.CharField(unique=True,max_length=12,blank=True,null=True,validators=[
        RegexValidator(
            regex=r"^\d{12}",
            message="UID number should be 12 digit"
        )
    ])
    cm_first_name = models.CharField(max_length=255,blank=True,null=True)
    cm_last_name = models.CharField(max_length=255,blank=True,null=True)

    cm_group_choices = (
        ("301","301"),
        ("801","801"),
        
        ("201","201"),
        ("202","202"),

        ("901","901"),
        ("902","902"),
        ("903","903"),
        ("904","904"),
        ("951","951"),
        ("952","952"),

        ("502","502"),

    )
    cm_group = models.PositiveIntegerField(blank=True,null=True,choices=cm_group_choices,default="301")
    cm_batch_choices = (
        ('1st','1st'),
        ('2nd','2nd'),
        ('3rd','3rd'),
        ('4th','4th'),
        ('5th','5th')
    )
    cm_batch = models.CharField(max_length=10,blank=True,null=True,choices=cm_batch_choices)
    
    cm_reminder_date = models.DateField(blank=True,null=True)
    cm_current_date_and_time = models.DateField()
    cm_next_date_and_time = models.DateField()
    cm_collection_count = models.IntegerField()
    cm_unit_amount = models.PositiveBigIntegerField(blank=True,null=True)
    cm_unit_sum = models.PositiveBigIntegerField(blank=True,null=True)
    cm_emi_count = models.PositiveBigIntegerField(blank=True,null=True)
    # cm_emi_sum = models.PositiveBigIntegerField(blank=True,null=True)
    cm_payable_date_emi = models.PositiveBigIntegerField(blank=True,null=True)
    cm_emi_bounce_date = models.CharField(blank=True,null=True)
    cm_collection_mode_choices = (
        ('daily','daily'),
        ('weekly','weekly'),
        ('monthly','monthly')
    )
    cm_collection_mode = models.CharField(default='daily',choices=cm_collection_mode_choices,blank=True,null=True)
    cm_payment_mode_choice = (
        ("gpay","gpay"),
        ("direct","direct")
    )
    cm_payment_mode = models.CharField(default='gpay',choices=cm_payment_mode_choice,blank=True,null=True)
    cm_collection_aprouch_mode_choices = (
        ("by call","by call"),
        ("by visit","by visit")
    )

    cm_emi_tobe_paid = models.FloatField(default=0.0,choices=cm_collection_aprouch_mode_choices,blank=True,null=True)
    cm_visit_type_choices = (
        ("direct visit","direct visit"),
        ("phone","phone")
    )
    cm_visit_type = models.CharField(max_length=100,default="direct visit",choices=cm_visit_type_choices,blank=True,null=True)
    cm_visit_count = models.PositiveIntegerField(default=0,blank=True,null=True)

    cm_paid_data = models.ForeignKey(PaidModel,on_delete=models.CASCADE,blank=True,null=True)
    cm_unpaid_data = models.ForeignKey(UnpaidModel,on_delete=models.CASCADE,blank=True,null=True)
    cm_others_data = models.ForeignKey(OtherModel,on_delete=models.CASCADE,blank=True,null=True)

    cm_created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return str(self.cm_last_name)
    


# ==========================================================================================================
#                                         COLLECTION MODELS START END
# ==========================================================================================================













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

