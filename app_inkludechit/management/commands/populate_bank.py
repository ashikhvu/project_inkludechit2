from app_inkludechit.models import BankListModel
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    help="populate the bank model with predefined bank name"

    def handle(self,*args,**kwargs):
        BANK_NAMES = [
            # Public Sector Banks
            "State Bank of India", "Bank of Baroda", "Bank of India", "Bank of Maharashtra",
            "Canara Bank", "Central Bank of India", "Indian Bank", "Indian Overseas Bank",
            "Punjab National Bank", "Punjab & Sind Bank", "UCO Bank", "Union Bank of India",

            # Private Sector Banks
            "HDFC Bank", "ICICI Bank", "Axis Bank", "Kotak Mahindra Bank", "IndusInd Bank",
            "IDFC FIRST Bank", "Bandhan Bank", "CSB Bank", "City Union Bank", "DCB Bank",
            "Dhanlaxmi Bank", "Federal Bank", "Jammu & Kashmir Bank", "Karnataka Bank",
            "Karur Vysya Bank", "Nainital Bank", "South Indian Bank", "Tamilnad Mercantile Bank",
            "Yes Bank", "RBL Bank", "Lakshmi Vilas Bank",

            # Foreign Banks
            "Citibank", "HSBC", "Standard Chartered", "Deutsche Bank", "Barclays",
            "BNP Paribas", "Bank of America", "DBS Bank", "Societe Generale",

            # Payments Banks
            "Airtel Payments Bank", "Fino Payments Bank", "India Post Payments Bank",
            "NSDL Payments Bank", "Paytm Payments Bank",

            # Small Finance Banks
            "AU Small Finance Bank", "Equitas Small Finance Bank", "Fincare Small Finance Bank",
            "ESAF Small Finance Bank", "Ujjivan Small Finance Bank", "Utkarsh Small Finance Bank",
            "Suryoday Small Finance Bank", "Jana Small Finance Bank", "North East Small Finance Bank",
            "Shivalik Small Finance Bank", "Capital Small Finance Bank",

            # Local Area Banks
            "Coastal Local Area Bank Ltd", "Krishna Bhima Samruddhi LAB Ltd"
        ]
        for i in BANK_NAMES:
            obj,created = BankListModel.objects.get_or_create(
                bank_name = i
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Bank {i} created successfully"))
            else:
                self.stdout.write(self.style.ERROR(f"Bank {i} creation failed"))