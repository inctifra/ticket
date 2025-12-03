from ticketless.tickets.models import Order
from ticketless.tickets.models import OrderItem


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


