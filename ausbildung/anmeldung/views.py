
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

    if request.method == 'POST':
    	form = AnmedlungForm(request.POST)

    	if form.is_valid():
    		anmeldung = form.save()
    else:
    	form = AnmeldungForm()

    return render(request, 'anmeldung/form.html', {
        'form': form
    })
