
from django.shortcuts import render, get_object_or_404

from .models import Kurs

from .forms import AnmeldungForm


def kurse(request):
    kurse = Kurs.objects.open()

    return render(request, 'anmeldung/kurse.html', {
        'kurse': kurse,
    })


def anmeldung(request, kurs):

    kurs = get_object_or_404(Kurs, url=kurs)

    form = AnmeldungForm()

    return render(request, 'anmeldung/form.html', {
        'form': form
    })
