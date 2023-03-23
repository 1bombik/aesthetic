from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Менеджер для кастомной модели юзера"""

    def create_user(self, email, password, **extra_fields):
        """Создание юзера"""
        if not email:
            raise ValueError(_("Не указана почта"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Создание суперюзера"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Для суперюзера обязательно is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Для суперюзера обязательно is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
