from rest_framework import serializers
from .models import Jurisdiction

class JurisdictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jurisdiction
        fields = '__all__'