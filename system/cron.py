from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import send_mail

from system import models


def send_mailing(recipients) -> None:
    print('отправка...')
    emails = recipients.client.values('email')
    title = recipients.message.title
    text = recipients.message.message

    for email in emails:
        try:
            send_mail(title,
                      text,
                      settings.EMAIL_HOST_USER,
                      recipient_list=[email['email']])
            status = 'success'
            answer = 'Письмо отправлено успешно!'


        except Exception as err:
            status = 'error'
            answer = str(err)
        models.MailingLog.objects.create(status=status, answer=answer, mailing=recipients)


def send_email_tasks():
    print('Функция для управления рассылками')
    now = datetime.now()  # текущая дата
    mailings = models.Mailing.objects.filter(status__in=[2, 3])

    to_send = False

    for mailing in mailings:
        if mailing.date_time.strftime('%H:%M') == now.strftime('%H:%M'):
            last_log = models.MailingLog.objects.filter(mailing=mailing.id).last()
            if not last_log:
                to_send = True
            else:
                from_last = now.date() - last_log.date_time.date()
                if mailing.periodicity == 1 and from_last == timedelta(days=1):
                    print('day')
                    to_send = True
                elif mailing.periodicity == 2 and from_last == timedelta(days=7):
                    print('week')
                    to_send = True
                elif mailing.periodicity == 3 and from_last == timedelta(days=30):
                    print('month')
                    to_send = True
        if to_send:
            send_mailing(mailing)
