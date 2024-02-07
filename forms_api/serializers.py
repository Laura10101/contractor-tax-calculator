"""Define serialisers for Form model."""

from rest_framework import serializers
from .models import Form


class FormSerializer(serializers.ModelSerializer):
    """Serialiser for Form model."""

    class Meta:
        """Metadata for Form serialiser."""

        model = Form
        fields = '__all__'
