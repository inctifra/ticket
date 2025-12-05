from rest_framework import permissions

from ticketless.management.models import EventPermission


class IsAllowedToScanTickets(permissions.BasePermission):
    message = "You do not have permission to scan tickets for this event."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        event_id = view.kwargs.get("event_slug")
        if not event_id:
            return False
        return EventPermission.objects.filter(
            user=user, event__slug=event_id, permission="scan_tickets"
        ).exists()
