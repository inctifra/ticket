from django.core.mail import EmailMessage


def send_ticket_email(item, pdf_data, ticket, filename):
    subject = f"Your Ticket for {item.ticket_type.event.title}"
    message = f"Hello {ticket.holder_name},\n\nPlease find your ticket attached."
    email = EmailMessage(
        subject=subject,
        body=message,
        to=[item.meta.get("paid_by")],
    )
    email.attach(filename, pdf_data, "application/pdf")
    email.send()
    ticket.sent_mail = True
    ticket.save()
