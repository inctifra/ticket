from rest_framework import permissions


class IsOwnerOrManager(permissions.BasePermission):
    """
    Custom permission to only allow owners or managers of a
    tenant to access certain views.
    """

    def has_permission(self, request, view):
        u = request.user
        return (
            hasattr(u, "tenant")
            or (u.owned_tenants.exists() or u.managed_tenants.exists())
            or u.is_superuser
        )


class IsEventManager(permissions.BasePermission):
    """
    Custom permission to only allow users with 'manage_event' permission
    for the specific event.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.has_perm("tickets.manage_event", obj)


class CanScanTickets(permissions.BasePermission):
    """
    Custom permission to only allow users with 'scan_tickets' permission
    for the specific event.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.has_perm("tickets.scan_tickets", obj)



class CanViewEventReports(permissions.BasePermission):
    """
    Custom permission to only allow users with 'view_event_reports' permission
    for the specific event.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.has_perm("tickets.view_event_reports", obj)


