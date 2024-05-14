from django.core.cache import cache

from django.core.mail import send_mail

from celery_tasks import app

from bookabook import settings

from secrets import token_urlsafe


@app.task
def send_verify_email(email: str) -> None:
    domain = settings.DOMAIN_SITE
    token = token_urlsafe(16)
    uri = f'/me/verify_email/{token}/'
    cache_life_time = settings.CACHE_LIFE_TIME
    cache.set(token, email, cache_life_time)
    message = \
        (
            f"""
                You're receiving this email because you need to finish activation 
                process on {domain}.

                Please go to the following page to activate account:
                http://{domain}{uri}

             """
        )
    send_mail(subject=f"Verify your email on {domain}",
              message=message, recipient_list=[email],
              from_email=settings.SERVER_EMAIL)

