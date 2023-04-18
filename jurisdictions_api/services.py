from .models import Jurisdiction


# Create service method to retrieve all jurisdictions 
def get_all_jurisdictions():
    jurisdictions = Jurisdiction.objects.all()
    return jurisdictions

# Create service method to add new jurisdiction
def create_jurisdiction(name):
    # Create new jurisdiction in the database 
    new_jurisdiction = Jurisdiction.objects.create(name=name)
    # Return ID of newly created jurisdiction
    return new_jurisdiction.id

# Create new method to delete jurisdictions 
def delete_jurisdictions_by_id(ids):
    # Delete each id in the database 
    Jurisdiction.objects.filter(pk__in=ids).delete()




