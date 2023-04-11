from .models import Jurisdiction


# Create service method to retrieve all jurisdictions 
def get_all_jurisdictions():
    jurisdictions = Jurisdiction.objects.all()
    return jurisdictions

