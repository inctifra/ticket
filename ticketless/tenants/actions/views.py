from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from ticketless.tenants.tasks import create_ticket_order
from ticketless.tickets.forms import ProcessTicketCheckoutForm
from ticketless.tickets.models import Event, Order
from ticketless.tickets.serializer import OrderSerializer


@require_POST
def initialize_ticket_purchase_view(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    form = ProcessTicketCheckoutForm(request.POST, event=event)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400, safe=False)
    email = form.cleaned_data.get("email")
    phone = form.cleaned_data.get("phone_number")
    amount = int(form.cleaned_data.get("total_price"))
    order = create_ticket_order(
        {
            "email": email,
            "phone": phone,
            "total_amount": amount,
        },
        event_slug=str(event.slug),
    )
    serializer = OrderSerializer(instance=order)
    return JsonResponse(serializer.data, status=201, safe=False)


@require_POST
def delete_order_payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    print(order)
    order.delete()
    return JsonResponse({}, status=204, safe=False)
