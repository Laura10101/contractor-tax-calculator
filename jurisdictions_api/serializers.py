"""Define serialisers for Jurisdiction model."""

from rest_framework import serializers
from .models import Jurisdiction


class JurisdictionSerializer(serializers.ModelSerializer):
    """Serialiser for Jurisdiction model."""

    class Meta:
        """Metadata for Jurisdiction serialiser."""

        model = Jurisdiction
        fields = '__all__'
