from django.urls import path
from . import views

app_name = "actions"

urlpatterns = [
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
]
