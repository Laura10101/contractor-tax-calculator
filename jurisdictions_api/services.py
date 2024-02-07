"""Define service methods for the Jurisdiction API."""

from .models import Jurisdiction
from django.db.models import Case, When, Value, IntegerField


def get_all_jurisdictions():
    """Return all jurisdictions."""

    # Order with the default jurisdiction at the top, and then alphabetically
    # https://stackoverflow.com/questions/2176346/can-django-orm-do-an-order-by-on-a-specific-value-of-a-column
    jurisdictions = Jurisdiction.objects.annotate(
        order=Case(
            When(id=1, then=1),
            default=Value(2),
            output_field=IntegerField()
        )
    ).order_by('order', 'name').all()
    print(str(jurisdictions))
    return jurisdictions


def get_jurisdictions_by_ids(ids):
    """Define jurisdictions based on a list of IDs."""

    return Jurisdiction.objects.filter(id__in=ids)


def create_jurisdiction(name):
    """Create a new jurisdiction."""

    # Create new jurisdiction in the database
    new_jurisdiction = Jurisdiction()
    new_jurisdiction.name = name
    new_jurisdiction.full_clean()
    new_jurisdiction.save()
    # Return ID of newly created jurisdiction
    return new_jurisdiction.id


def delete_jurisdictions_by_id(ids):
    """Delete jurisdictions based on a list of ids."""
    # Delete each id in the database
    Jurisdiction.objects.filter(pk__in=ids).delete()
