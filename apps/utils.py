from django.core.mail import send_mail

from root.settings import EMAIL_HOST_USER


def send_email(subject, message, to_email: list):
    send_mail(subject, message, EMAIL_HOST_USER, to_email, False)
    return {"status": "success", "message": f"{', '.join(to_email)} pochtaga yuborildi"}
