import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from system.cron import send_email_tasks
from system.forms import MailingForm
from system.models import Mailing, User, MailingMessage, Blog, MailingLog


@cache_page(60)
def home(request):
    """Домашняя страница"""
    posts = Blog.objects.all()
    posts_for_context = []
    if len(posts) > 3:
        for i in range(3):
            number = random.randint(0, len(posts))
            posts_for_context.append(posts[number])
            print(posts[number])
    else:
        posts_for_context = posts

    if request.user.has_perm('service.can_disable_mailings'):
        mailing_list = Mailing.objects.filter(status=2 or 3)
        mailing_all = Mailing.objects.all()

    else:
        mailing_list = Mailing.objects.filter(status=2 or 3,
                                              owner=request.user.pk)
        mailing_all = Mailing.objects.filter(owner=request.user.pk)

    count_clients = User.objects.all()
    context = {'object_list': mailing_list, 'title': 'Список активных рассылок',
               'count_active_mailings': len(mailing_list),
               'count_mailings': len(mailing_all),
               'posts': posts_for_context,
               'count_clients': len(count_clients)}
    return render(request, 'system/index.html', context)


class MailingListView(ListView):
    """Все имеющиеся рассылки"""
    model = Mailing
    template_name = 'system/mailings_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Список всех рассылок'
        return context

    def get_queryset(self):
        if self.request.user.has_perm('service.can_disable_mailings'):
            return super().get_queryset()

        else:
            return Mailing.objects.filter(owner=self.request.user.pk)


class MailingCreateView(CreateView, LoginRequiredMixin):
    """Создание рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('system:index')

    def form_valid(self, form):
        mailing = form.save()
        mailing.owner = self.request.user
        send_email_tasks()
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(UpdateView, LoginRequiredMixin):
    """Редактирования рассылок"""

    model = Mailing
    fields = ('date_time', 'periodicity', 'client', 'status', 'message')
    success_url = reverse_lazy('system:index')


class MailingDeleteView(DeleteView, LoginRequiredMixin):
    """Удаления рассылки"""

    model = Mailing
    success_url = reverse_lazy('system:index')


class ClientCreateView(CreateView, LoginRequiredMixin):
    """Создание клиента"""

    model = User
    success_url = reverse_lazy('system:create')
    fields = ('email', 'first_name', 'last_name', 'comment')


class MessageCreateView(CreateView, LoginRequiredMixin):
    """Создание сообщения"""

    model = MailingMessage
    fields = ('title', 'message')
    success_url = reverse_lazy('system:create')


def disable_mailing(pk):
    """Отключение рассылок"""

    mailing_for_disable = Mailing.objects.get(pk=pk)
    mailing_for_disable.status = 1
    mailing_for_disable.save()
    return redirect(reverse('system:mailings'))


class MailingLogList(ListView, LoginRequiredMixin):
    model = MailingLog

    def get_queryset(self):
        return MailingLog.objects.filter(mailing__owner=self.request.user)


class MailingMessagesList(ListView, LoginRequiredMixin):
    model = MailingMessage

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()

        return MailingMessage.objects.filter(owner=self.request.user)


class ClientListView(ListView, LoginRequiredMixin):
    model = User

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return User.objects.filter(owner=self.request.user)
