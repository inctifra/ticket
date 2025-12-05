from django.utils import timezone

from ticketless.tickets.models import ScanLog
from ticketless.tickets.models import Ticket
from ticketless.users.models import User


def create_ticket_scan_log(
    ticket: Ticket, scanner: User, data: dict, payload: dict | None = None
):
    if payload is None:
        payload = {}
    scan = ScanLog(
        ticket=ticket,
        token=ticket.token,
        scanned_by=scanner,
        success=data.get("success"),
        reason=data.get("reason"),
        scanned_at=timezone.now,
        raw_payload=payload,
    )
    scan.save()
    return scan
