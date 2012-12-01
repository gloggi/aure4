from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from .signals import password_set
from .utils import (InvalidCode, decode, send_registration_mail)
from .forms import RegistrationForm


def account(request):
    user = request.user

    if not user.is_authenticated():
        return render(request, 'account/home.html')

    return render(request, 'account/profile.html', {
        'user': user
    })


def register(request):
    return render(request, 'account/register.html')


def registration(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            send_registration_mail(email, request)

            return render(request, 'registration/email_registration_sent.html', {
                'email': email,
            })

    else:
        form = RegistrationForm()

    return render(request, 'registration/email_registration_form.html', {
        'form': form,
    })


def registration_confirm(request, code, max_age=1800):
    try:
        email, user = decode(code, max_age=max_age)
    except InvalidCode as exc:
        messages.error(request, exc[0])
        return redirect('/')

    if not user:
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Diese Email Adresse besteht bereits')
            return redirect('/')

        user = User(
            username=email if len(email) <= 30 else get_random_string(25),
            email=email)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()

            password_set.send(
                sender=user.__class__,
                request=request,
                user=user,
                password=form.cleaned_data.get('new_password1'),
                )

            messages.success(request, 'Dein Passwort wurde erfolgreich gesetzt.'
                'Du kannst dich nun anmelden.')

            return redirect('login')

    else:
        messages.success(request, 'Bitte setze ein Passwort.')
        form = SetPasswordForm(user)

    return render(request, 'registration/password_set_form.html', {
        'form': form,
        })
