"""Define signals to delete rulesets and rules when jurisdiction deleted."""
from django.db.models.signals import post_delete

from jurisdictions_api.models import Jurisdiction
from .services import delete_rulesets_for_jurisdiction


def trigger_rulesets_deletion(sender, instance, *args, **kwargs):
    """Delete all rulesets for a jurisdiction when jurisdiction deleted."""
    delete_rulesets_for_jurisdiction(instance.id)


post_delete.connect(trigger_rulesets_deletion, sender=Jurisdiction)
