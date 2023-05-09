from rest_framework import serializers
from .model import *

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jurisdiction
        fields = '__all__'