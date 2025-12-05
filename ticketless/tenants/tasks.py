from decimal import Decimal

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from ticketless.management.models import EventPermission
from ticketless.tickets.models import Event
from ticketless.tickets.models import Order
from ticketless.tickets.models import OrderItem
from ticketless.tickets.models import Ticket
from ticketless.tickets.models import TicketType
from ticketless.users.models import Profile


def create_ticket_order(data: dict, event_slug: str):
    order = Order(
        email=data.get("email"),
        phone=data.get("phone"),
        total_amount=data.get("total_amount"),
        currency=data.get("KES", "KES"),
        meta={"provider": "PAYSTACK", "event_slug": str(event_slug)},
    )
    order.save()
    return order


def create_ticket_order_item(data: dict, order_id: str, event_slug: str):
    order = get_object_or_404(Order, id=order_id)
    event = get_object_or_404(Event, slug=event_slug)
    ticket_type = get_object_or_404(TicketType, id=data.get("ticket_type_id"))
    quantity = data.get("quantity")
    order.status = "paid"
    order.save()
    event.capacity -= 1
    event.save()
    amount = Decimal(str(data.get("amount")))
    quantity = Decimal(str(data.get("quantity")))
    unit_price = amount / quantity

    item = OrderItem(
        order=order,
        ticket_type=ticket_type,
        quantity=quantity,
        unit_price=unit_price,
        meta={
            "order_status": str(order.get_status_display()),
            "event_slug": str(event.slug),
            "trans_reference": data.get("trxref"),
            "transaction": data.get("transaction"),
            "paid_by": data.get("email", "phone"),
            "status": data.get("status"),
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
        },
    )
    item.save()
    return item


def create_or_retrieve_ticket_for_order(order_item_id: int):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    cleaned_name = (
        f"{order_item.meta.get('first_name')} {order_item.meta.get('last_name')}"
    )
    try:
        ticket = Ticket.objects.get(
            order_item=order_item,
            holder_name=cleaned_name,
            holder_email=f"{order_item.meta.get('paid_by')}",
        )
    except Ticket.DoesNotExist:
        ticket = Ticket(
            order_item=order_item,
            holder_name=cleaned_name,
            holder_email=f"{order_item.meta.get('paid_by')}",
            seats=order_item.quantity,
            event_title=order_item.ticket_type.event.title,
            event_start=order_item.ticket_type.event.start_at,
        )
        ticket.save()
    return ticket


def _normalize_profiles(profiles: Profile | QuerySet) -> list[Profile]:
    """Normalize profiles to a list."""
    if isinstance(profiles, Profile):
        return [profiles]
    if isinstance(profiles, QuerySet):
        return list(profiles)
    msg = "profiles must be a Profile instance or a QuerySet of Profile instances."
    raise TypeError(msg)


def _normalize_permissions(permissions: str | list[str]) -> list[str]:
    """Normalize permissions to a list."""
    if isinstance(permissions, str):
        return [permissions]
    if isinstance(permissions, list):
        if not all(isinstance(p, str) for p in permissions):
            msg = "All items in the permission list must be strings."
            raise TypeError(msg)
        return permissions
    msg = "permissions must be a string or a list of strings."
    raise TypeError(msg)


def _validate_permissions(permissions: list[str]) -> None:
    """Validate that all permissions are allowed."""
    allowed_perms = dict(EventPermission.PERMISSION_CHOICES).keys()
    for perm in permissions:
        if perm not in allowed_perms:
            msg = f"Invalid permission: {perm}"
            raise ValueError(msg)


def assign_event_scanning_permission(
    event,
    profiles: Profile | QuerySet,
    permissions: str | list[str]
):
    """
    Assign event-specific permission(s) to one or multiple Profile instances
    (single instance or QuerySet) and update their role to 'S'.

    Args:
        event: The Event instance to assign permissions for.
        profiles: A Profile instance or a Django QuerySet of Profile instances.
        permissions: A permission codename string or a list of strings.

    Raises:
        TypeError: If input types are invalid.
        ValueError: If a permission codename is invalid.
    """
    profiles = _normalize_profiles(profiles)
    permissions = _normalize_permissions(permissions)
    _validate_permissions(permissions)

    # Assign permissions and update roles
    for profile in profiles:
        for perm in permissions:
            EventPermission.objects.get_or_create(
                user=profile.user,
                event=event,
                permission=perm
            )

        # Update role if not already 'S'
        if profile.role != "S":
            profile.role = "S"
            profile.save(update_fields=["role"])

    return True
