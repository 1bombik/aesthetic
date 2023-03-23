from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class UserRegisterForm(forms.ModelForm):
    """Регистрация юзера"""
    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=_("Пароль должен быть не менее 8 символов")
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=_("Повтори пароль")
    )

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'telegram', 'phone_number', 'notification')

    def clean_password2(self):
        # Проверка на совпадение паролей
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Пароли не совпадают"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Изменение данных юзера"""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'telegram', 'phone_number', 'notification', 'password')

    def clean_password(self):
        return self.initial["password"]


class UserLoginForm(forms.Form):
    """Вход для юзера"""
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError(_("Неверно указана почта или пароль"))
            if not user.check_password(password):
                raise forms.ValidationError(_("Неверно указана почта или пароль"))
            cleaned_data['user'] = user
        return cleaned_data
