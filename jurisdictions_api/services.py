from .models import Jurisdiction
from django.db.models import Case, When, Value, IntegerField


# Create service method to retrieve all jurisdictions 
def get_all_jurisdictions():
    # Order with the default jurisdiction at the top, and then alphabetically
    # Solution taken from: https://stackoverflow.com/questions/2176346/can-django-orm-do-an-order-by-on-a-specific-value-of-a-column
    jurisdictions = Jurisdiction.objects.annotate(
        order=Case(
            When(id=1, then=1),
            default=Value(2),
            output_field=IntegerField()
        )
    ).order_by('order', 'name').all()
    print(str(jurisdictions))
    return jurisdictions

# Return jurisdictions by a list of IDs
def get_jurisdictions_by_ids(ids):
    return Jurisdiction.objects.filter(id__in=ids)

# Create service method to add new jurisdiction
def create_jurisdiction(name):
    # Create new jurisdiction in the database 
    new_jurisdiction = Jurisdiction()
    new_jurisdiction.name = name
    new_jurisdiction.full_clean()
    new_jurisdiction.save()
    # Return ID of newly created jurisdiction
    return new_jurisdiction.id

# Create new method to delete jurisdictions 
def delete_jurisdictions_by_id(ids):
    # Delete each id in the database 
    Jurisdiction.objects.filter(pk__in=ids).delete()




