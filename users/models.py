from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    name = models.CharField(max_length=15, null=False, blank=False, help_text='Как тебя зовут?')
    email = models.EmailField(_("Email address"), unique=True, help_text='Укажи свою почту')
    telegram = models.CharField(max_length=50, null=True, blank=True,
                                help_text='Укажи свой телеграм в формате: @your-telegram')
    phone_number = models.CharField(max_length=13, null=True, blank=True, help_text='Укажи свой номер телефона')

    to_email = 'На почту'
    to_telegram = 'В телеграм'
    statuses = (
        (to_email, 'На почту'),
        (to_telegram, 'В телеграм')
    )
    notification = models.TextField(choices=statuses, help_text='Куда присылать оповещения и новости?')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
