from django.core.mail import send_mail


def send(user_email):
    send_mail(
        'Здратвуйте! Вы подписались на рассылку.',
        'Будет много спама, но не долго=)',
        'fff@yandex.ru',
        [user_email],
        fail_silently=False,
    )
