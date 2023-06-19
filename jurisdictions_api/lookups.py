from selectable.base import ModelLookup
from selectable.registry import registry

from .models import Jurisdiction


class JurisdictionLookup(ModelLookup):
    model = Jurisdiction
    search_fields = ('name__icontains', )
    
registry.register(JurisdictionLookup)