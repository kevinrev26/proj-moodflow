from rest_framework import serializers

class SearchSerializer(serializers.Serializer):
    term = serializers.CharField(required=True)
    