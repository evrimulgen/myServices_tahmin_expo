from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_verification_email(key, email):
    send_mail(
        "Tahmin.io'ya hoşgeldiniz! Emailinizi onaylayın",
        "Emailinizi onaylamak için tıklayın: http://tahmin.io/api/v1/users/activate/?key=" + key,
        "info@tahmin.io",
        [email]
    )


@shared_task
def send_password_change_email(email):
    send_mail(
        "Şifreniz değişti",
        "Hesabınızın şifresi değişti. Eğer bu değişikliği siz yapmadıysanız, info@tahmin.io'ya probleminizle birlikte bir mail gönderin.",
        "info@tahmin.io",
        [email],
    )


@shared_task
def send_passwordreset_email(key, email):
    send_mail(
        "Tahmin.io Şifre Değişikliği",
        "Şifrenizi değiştirmek için http://tahmin.io/change-password/?key=" + key,
        "info@tahmin.io",
        [email]
    )
