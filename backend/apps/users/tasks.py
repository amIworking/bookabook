
from django.core.cache import cache

from django.core.mail import send_mail

from celery_tasks import app

from bookabook import settings

from secrets import token_urlsafe

from apps.users.logic.email_messages import email_messages


@app.task
def send_email_to_user(email: str,
                       message_key: str = "verify_email") -> None:
    domain = settings.DOMAIN_SITE
    token = token_urlsafe(16)
    cache_life_time = settings.CACHE_LIFE_TIME
    cache.set(token, email, cache_life_time)
    email_info = email_messages[message_key]
    uri = eval(email_info['uri'])
    subject = eval(email_info['subject'])
    message = eval(email_info['message'])
    send_mail(subject=subject, message=message,
              recipient_list=[email],
              from_email=settings.SERVER_EMAIL)
