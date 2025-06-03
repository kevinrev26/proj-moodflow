from rest_framework import serializers
from .models import App, AppSnapshot

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = '__all__' 

class AppSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppSnapshot
        fields = '__all__' 