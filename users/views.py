from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm, UserChangeForm
from .models import UserProfile, CustomUser


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)

            subject = 'Регистрация прошла успешно!'
            message = f'Спасибо за регистрацию! Желаем приятных покупок!'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            return redirect('home')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Неверно указана почта или пароль")
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def user_profile(request, pk):
    user = CustomUser.objects.get(pk=pk)
    profile = UserProfile.objects.get(user=pk)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = UserChangeForm(instance=user)
    context = {'user': user, 'profile': profile, 'form': form}
    return render(request, 'users/user_account.html', context)
