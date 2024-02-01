from django.db.models.signals import post_save, post_delete

from jurisdictions_api.models import Jurisdiction
from .services import create_form, delete_form_for_jurisdiction

def trigger_form_creation(sender, instance, created, **kwargs):
    if created:
        create_form(instance.id)

def trigger_form_deletion(sender, instance, *args, **kwargs):
    delete_form_for_jurisdiction(instance.id)

post_save.connect(trigger_form_creation, sender=Jurisdiction)
post_delete.connect(trigger_form_deletion, sender=Jurisdiction)