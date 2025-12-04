import base64
import json
from io import BytesIO

from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from weasyprint import HTML

from config.settings.base import env
from ticketless.tenants.mails import send_ticket_email
from ticketless.tenants.tasks import create_or_retrieve_ticket_for_order
from ticketless.tenants.tasks import create_ticket_order
from ticketless.tenants.tasks import create_ticket_order_item
from ticketless.tickets.forms import ProcessTicketCheckoutForm
from ticketless.tickets.models import Event
from ticketless.tickets.models import Order
from ticketless.tickets.models import OrderItem
from ticketless.tickets.serializer import OrderItemSerializer
from ticketless.tickets.serializer import OrderSerializer

paystack_public_key = env("PAYSTACK_PUBLIC_KEY")
paystack_private_key = env("PAYSTACK_PRIVATE_KEY")


@require_POST
def initialize_ticket_purchase_view(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    form = ProcessTicketCheckoutForm(request.POST, event=event)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400, safe=False)
    email = form.cleaned_data.get("email")
    phone = form.cleaned_data.get("phone_number")
    amount = int(form.cleaned_data.get("total_price"))
    with transaction.atomic():
        order = create_ticket_order(
            {
                "email": email,
                "phone": phone,
                "total_amount": amount,
            },
            event_slug=str(event.slug),
        )
        serializer = OrderSerializer(instance=order)

        item_url = reverse(
            "tenants:actions:process_ticket_order_item_view",
            kwargs={
                "order_id": serializer.data["id"],
                "event_slug": event.slug,
            },
        )
        response_data = serializer.data.copy()
        response_data["order_item_process_url"] = item_url
    return JsonResponse(response_data, status=201, safe=False)


@require_POST
def process_ticket_order_item_view(request, order_id, event_slug):
    try:
        data: dict = json.loads(request.body)
    except json.JSONDecodeError as e:
        return JsonResponse({"errors": json.dumps(e)}, status=400, safe=False)
    with transaction.atomic():
        item = create_ticket_order_item(
            {
                "quantity": data.get("quantity"),
                "ticket_type_id": int(data.get("ticket_type")),
                "amount": data.get("total_price"),
                "trxref": data.get("trxref"),
                "transaction": data.get("transaction"),
                "email": data.get("email"),
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name"),
                "phone": data.get("phone_number"),
                "status": data.get("status"),
            },
            order_id=order_id,
            event_slug=event_slug,
        )
        serializer = OrderItemSerializer(instance=item)
        response_data = serializer.data.copy()
        response_data["success_url"] = reverse(
            "tenants:download_ticket_view", kwargs={"order_item_id": int(item.id)}
        )
    return JsonResponse(response_data, status=200)


@require_POST
def delete_order_payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return JsonResponse({}, status=204, safe=False)


def load_paystack_payment_key(request):
    return JsonResponse({"key": str(paystack_public_key)}, status=200, safe=False)


def download_ticket_view(request, order_item_id):
    item = get_object_or_404(OrderItem, id=order_item_id)
    ticket = create_or_retrieve_ticket_for_order(order_item_id)
    qr_image_base64 = ""
    if ticket.qr_code:
        with ticket.qr_code.open("rb") as f:
            qr_image_base64 = base64.b64encode(f.read()).decode("utf-8")
    html_string = render_to_string(
        "tenants/tickets/ticket_template.html",
        {"order_item": item, "ticket": ticket, "qr_image_base64": qr_image_base64},
    )

    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)
    pdf_file.seek(0)
    pdf_data = pdf_file.read()

    filename = f"ticket-{slugify(item.ticket_type.event.title)}.pdf"
    if not ticket.sent_mail:
        send_ticket_email(item, pdf_data, ticket, filename)
    response = HttpResponse(pdf_data, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
