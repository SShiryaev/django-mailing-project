import random
from secrets import token_hex

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    """Представление регистрации пользователя """

    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Пожалуйста, перейдите по ссылке для подтверждения почты: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    # верификация пользователя по почте и флагу is_active

    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileView(UpdateView):
    """Представление редактирования профиля пользователя"""

    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def make_password():
    # генерация пароля

    dictionaries = ['abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', '0123456789', '!&?']
    generate_password = [random.choice(d) for d in dictionaries] + random.choices(''.join(dictionaries),
                                                                                  k=random.randint(8, 16) - 4)
    random.shuffle(generate_password)
    return ''.join(generate_password)


class UserPasswordResetView(PasswordResetView):
    """Представление восстановления пароля"""

    template_name = 'users/user_password_reset.html'
    email_template_name = 'users/email.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'
    model = User

    def form_valid(self, form):
        if self.request.method == 'POST':
            email = self.request.POST['email']
            user = User.objects.get(email=email)
            password = make_password()
            user.set_password(password)
            user.save()
            send_mail(
                subject='Восстановление пароля',
                message=f'Вы запросили восстановление пароля на сайте Магазин СЗР'
                        f'Ваш новый пароль: {password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            return HttpResponseRedirect(reverse('users:login'))
        return super().form_valid(form)


class UsersListView(PermissionRequiredMixin, ListView):
    """ Просмотр списка пользователей """

    model = User
    permission_required = "users.view_users"

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            return super().get_queryset(*args, **kwargs).exclude(pk=self.request.user.pk).exclude(is_superuser=True)
        return super().get_queryset(*args, **kwargs).exclude(pk=self.request.user.pk).exclude(
            is_superuser=True).exclude(is_staff=True)


@permission_required('users.block_user')
def toggle_deactivate(request, pk):
    """Контроллер блокировки пользователя"""

    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True

    user.save()

    return redirect(reverse('users:user_list'))
