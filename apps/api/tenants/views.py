from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.api.tenants.serializers import TenantSelectSerializer
from apps.tenants.models import Client
from apps.tenants.serializers import ClientSerializer
from rest_framework.response import Response


class TenantAPIListView(APIView):
    """
    GET: List all tenants user belongs to
    POST: Select a tenant by schema
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Optionally filter tenants the user belongs to
        tenants = Client.objects.all()
        serializer = ClientSerializer(tenants, many=True)
        return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        # Select a tenant via schema
        serializer = TenantSelectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        schema_name = serializer.validated_data.get("schema")

        # Fetch tenant safely
        tenant = get_object_or_404(Client, schema_name=schema_name)
        tenant_serializer = ClientSerializer(instance=tenant)
        return Response(tenant_serializer.data, status=200)

