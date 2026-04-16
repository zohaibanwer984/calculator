from rest_framework import serializers
from .models import Histroy

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Histroy
        fields = '__all__'