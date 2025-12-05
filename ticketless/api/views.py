from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from ticketless.api.snippets.authentication import TenantHeaderAuthentication
from ticketless.api.snippets.permission import IsAllowedToScanTickets
from ticketless.api.tasks import create_ticket_scan_log
from ticketless.customers.models import Client
from ticketless.customers.serializers import ClientModelSerializer
from ticketless.management.models import EventPermission
from ticketless.tickets.models import Event
from ticketless.tickets.models import Ticket
from ticketless.tickets.serializer import EventSerializer
from ticketless.users.api.serializers import UserSerializer


class TenantListView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [TenantHeaderAuthentication]
    queryset = Client.objects.all()
    serializer_class = ClientModelSerializer


@extend_schema(exclude=True)
class EventSearchView(APIView):
    authentication_classes = [
        TenantHeaderAuthentication,
        JWTAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.GET.get("query", "").strip()
        user = request.user

        if not query:
            return Response(
                {"detail": "Query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Filter events where user has any permission for that event
        allowed_event_ids = EventPermission.objects.filter(user=user).values_list(
            "event__id", flat=True
        )
        events = Event.objects.filter(
            id__in=allowed_event_ids, title__icontains=query
        ).order_by("title")
        serializer = EventSerializer(events, many=True)
        return Response({"events": serializer.data}, status=status.HTTP_200_OK)


@extend_schema(exclude=True)
class EventDetailView(RetrieveAPIView):
    """
    Tenant-aware Event Detail API.

    - Requires X-Tenant header to switch tenant (mobile app provides it)
    - JWT authentication
    - Only returns event if user has permissions
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [TenantHeaderAuthentication, JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    lookup_field = "slug"

    def get_queryset(self):
        """
        Restrict queryset to events the user has permission for.
        """
        user = self.request.user
        allowed_event_ids = EventPermission.objects.filter(user=user).values_list(
            "event__id", flat=True
        )
        return Event.objects.filter(id__in=allowed_event_ids)


@extend_schema(exclude=True)
class ScanTicketView(APIView):
    authentication_classes = [
        TenantHeaderAuthentication,
        JWTAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated, IsAllowedToScanTickets]

    def post(self, request, event_slug):
        qr_code_data = request.data.get("qr_code_data")
        if not qr_code_data:
            return Response(
                {"detail": "QR code is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            ticket = Ticket.objects.get(
                token=qr_code_data,
                order_item__ticket_type__event__slug=event_slug,
            )
        except Ticket.DoesNotExist:
            msg = "Invalid or mismatched ticket."
            return Response(
                {"detail": msg},
                status=status.HTTP_404_NOT_FOUND,
            )

        if ticket.status == "redeemed":
            msg = "Ticket has already been scanned."
            create_ticket_scan_log(
                ticket,
                request.user,
                {"success": False, "reason": msg},
            )
            return Response(
                {"detail": msg},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ticket.status = "redeemed"
        ticket.save()
        msg = "Ticket scanned successfully."
        scan = create_ticket_scan_log(
            ticket,
            request.user,
            {"success": True, "reason": msg},
        )
        return Response(
            {
                "detail": msg,
                "ticket_id": ticket.id,
                "event": EventSerializer(
                    instance=ticket.order_item.ticket_type.event
                ).data,
                "scanned_by": UserSerializer(instance=scan.scanned_by).data,
            },
            status=status.HTTP_200_OK,
        )
