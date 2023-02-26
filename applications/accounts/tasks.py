from config.celery import app
from django.core.mail import send_mail
from decouple import config


@app.task
def send_confirmation_email(email, code):
    full_link = f"http://127.0.0.1:8000/api/v1/account/confirm/{code}"
    send_mail(
        "User activation",
        f"Пожалуйста подтвердите аккаунт перейдя по ссылке:  {full_link}",
        config('EMAIL_HOST_USER'),
        [email]
    )


@app.task
def send_password_recovery(email, code):
    full_link = f"http://127.0.0.1:8000/api/v1/account/recovery/{code}"
    send_mail(
        "Password recovery",
        f"Перейдите по ссылке чтобы сбросить пароль:  {full_link}",
        config('EMAIL_HOST_USER'),
        [email]
    )


@app.task
def send_confirmation_email_mentor(email, code):
    full_link = f"http://127.0.0.1:8000/api/v1/account/confirm-mentor/{code}"
    send_mail(
        "User activation",
        f"Пожалуйста подтвердите аккаунт перейдя по ссылке:  {full_link}",
        config('EMAIL_HOST_USER'),
        [email]
    )
