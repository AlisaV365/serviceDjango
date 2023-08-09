from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView
from users.forms import UserProfileForm, UserRegisterForm

from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    # template_name = 'users/logout.html'
    pass


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    # def form_valid(self, form):
    #     self.object = form.save()
    #     send_mail(
    #         subject='Поздравляем с регистрацией',
    #         message='Вы зарегистрировались на нашей платформе',
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[self.object.email]
    #     )
    #
    #     return super().form_valid(form)

class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('service:home')
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user


class UsersListView(ListView):
    model = User

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Список зарегистрированных пользователей сервиса'
        return context


def activate_new_user(request, pk):
    user = get_user_model()
    user_for_activate = user.objects.get(id=pk)
    user_for_activate.is_active = True
    user_for_activate.save()
    return render(request, 'users/activate_user.html')


def block_user(request, pk):
    user_for_block = User.objects.get(id=pk)
    if user_for_block.is_active:
        user_for_block.is_active = False
    else:
        user_for_block.is_active = True

    user_for_block.save()

    return redirect(reverse('users:users_list'))
