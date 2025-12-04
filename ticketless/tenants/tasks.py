from decimal import Decimal

from django.shortcuts import get_object_or_404

from ticketless.tickets.models import Event
from ticketless.tickets.models import Order
from ticketless.tickets.models import OrderItem
from ticketless.tickets.models import Ticket
from ticketless.tickets.models import TicketType


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
