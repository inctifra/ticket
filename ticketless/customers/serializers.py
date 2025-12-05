from rest_framework import serializers

from ticketless.users.api.serializers import UserSerializer

from .models import Client


class ClientModelSerializer(serializers.ModelSerializer):
    manager = UserSerializer(read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Client
        fields = [
            "name",
            "schema_name",
            "created_on",
            "description",
            "manager",
            "owner",
        ]
