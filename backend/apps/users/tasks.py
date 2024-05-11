from django.core.cache import cache

from django.core.mail import send_mail

from celery_tasks import app

from apps.users.models import User

from bookabook.settings import SERVER_EMAIL, env

import secrets


def generate_token_urlsafe(length: int = 16):
    return secrets.token_urlsafe(length)


@app.task
def send_verify_email(data):
    email = data.get('email')
    domain = env.str('DOMAIN_SITE', '127.0.0.1:8000')
    uri = 'verify_email'
    token = generate_token_urlsafe()
    cache.set(token, email, 300)
    message = \
        (
            f"""
                You're receiving this email because you need to finish activation 
                process on {domain}.

                Please go to the following page to activate account:
                http://{domain}/{uri}/{token}/

             """
        )
    send_mail(subject=f"Verify your email on {domain}",
              message=message, recipient_list=[email],
              from_email=SERVER_EMAIL)


def check_verify_email(token):
    email = cache.get(token)
    user = User.objects.filter(email=email).first()
    if user:
        if user.is_active:
            response_data = \
                {
                    "message": "Your account already has been activated",
                    "status": 400
                }
        else:
            user.is_active = True
            user.save()
            response_data = \
                {
                    "message": "Congrats, you successfully verified your email",
                    "status": 200
                }
    else:
        response_data = \
            {
                "message":
                    "Your verify token got inspired "
                    "or you're trying to send an invalid one",
                "status": 400
            }
    return response_data
