from rest_framework import serializers
from .models import Unit

class UnitSerializer(serializers.ModelSerializer):
  access_code = serializers.CharField(style = {'type': 'password'})
  class Meta:
    model = Unit
    fields = ('id', 'width', 'height','length', 'size', 'occupied', 'daily_charge', 'weekly_charge', 'monthly_charge', 'access_code')
    write_fields = ('password')