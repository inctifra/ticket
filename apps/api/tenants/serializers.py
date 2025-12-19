from rest_framework import serializers

class TenantSelectSerializer(serializers.Serializer):
    schema = serializers.CharField(max_length=255)
