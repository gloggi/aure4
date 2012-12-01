
from django.shortcuts import render


def account(request):
    user = request.user

    if not user.is_authenticated():
        return render(request, 'account/home.html', {})

    return render(request, 'account/profile.html', {
        'user': user
    })


def signup(request):
    return render(request, 'account/signup.html', {})
