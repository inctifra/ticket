from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.tenants.api.permissions import TenantHeaderPermission

class EventSearchAPIView(APIView):
    permission_classes = [IsAuthenticated, TenantHeaderPermission]
    def get(self, request, *args, **kwargs):
        print(request.tenant)
        return Response({}, status=200)



