from django.conf import settings
from django.db import models
from users.models import User

# варианты периодичности рассылки (раз в день, в неделю, в месяц)
MAILING_PERIODICITY = [(1, 'раз в день'), (2, 'раз в неделю'), (3, 'раз в месяц')]

# варианты статуса рассылки
MAILING_STATUS = [(1, 'завершена'), (2, 'создана'), (3, 'запущена')]

# необязательное поле
NULLABLE = {'blank': True, 'null': True}


class System(models.Model):
    name = models.CharField(max_length=350, unique=True, verbose_name='наименование')
    description = models.TextField(**NULLABLE, verbose_name='описание')

    def __str__(self):
        return f'{self.name} ({self.description})'

    class Meta:
        verbose_name = 'система'
        verbose_name_plural = 'системы'


class MailingMessage(models.Model):
    """Сообщение для рассылки"""

    title = models.CharField(max_length=150, verbose_name='Тема сообщения')
    message = models.TextField(verbose_name='Тело сообщения')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.title


class Mailing(models.Model):
    """Настройка для рассылки"""

    date_time = models.DateTimeField(verbose_name='время рассылки')
    periodicity = models.PositiveSmallIntegerField(choices=MAILING_PERIODICITY, default=1, verbose_name='периодичность')
    status = models.PositiveSmallIntegerField(choices=MAILING_STATUS, default=2, verbose_name='статус рассылки')
    client = models.ManyToManyField(User, related_name='client_mailings', verbose_name='клиент рассылки')
    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE, verbose_name='сообщение для рассылки')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner_mailings', on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return f'Рассылка на {self.date_time} с периодичностью {self.periodicity}. Статус {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [('can_view_mailings', 'can_view_mailings'),
                       ('can_disable_mailings', 'can_disable_mailings'),
                       ]


class MailingLog(models.Model):
    """Логи рассылки"""

    date_time = models.DateTimeField(auto_now_add=True, verbose_name='дата и время попытки')
    status = models.CharField(max_length=100, verbose_name='Статус попытки')
    answer = models.CharField(max_length=100, verbose_name='Ответ сервера', **NULLABLE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'


class Blog(models.Model):
    """Блог"""

    title = models.CharField(max_length=100, verbose_name='заголовок')
    description = models.TextField(verbose_name='содержимое статьи')
    image = models.ImageField(upload_to='image/', verbose_name='изображение', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')

    def __str__(self):
        return f'{self.title} ({self.description})'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блог'
