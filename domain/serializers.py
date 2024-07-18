from rest_framework import serializers
from .models import DomainDetails

class DomainDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainDetails
        fields = '__all__'
