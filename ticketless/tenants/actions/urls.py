from django.urls import path

from . import views

app_name = "actions"

urlpatterns = [
    path(
        "load-provider-payment-key/",
        views.load_paystack_payment_key,
        name="load_paystack_view",
    ),
    path(
        "initialize-ticket-purchase/<event_slug>/",
        views.initialize_ticket_purchase_view,
        name="initialize_ticket_purchase_view",
    ),
    path(
        "delete-order-view/<order_id>/",
        views.delete_order_payment_view,
        name="delete_order_view",
    ),
    path(
        "events/ticket-download-view/<order_item_id>/",
        views.download_ticket_view,
        name="ticket_download_view",
    ),
    path(
        "process-ticket-order-item-purchase/<order_id>/<event_slug>/",
        views.process_ticket_order_item_view,
        name="process_ticket_order_item_view",
    ),
]
