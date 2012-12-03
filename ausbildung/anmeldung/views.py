
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Kurs

from .forms import AnmeldungForm


def kurse(request):
    kurse = Kurs.objects.open()

    return render(request, 'anmeldung/kurse.html', {
        'kurse': kurse,
    })


@login_required
def anmeldung(request, kurs):
    kurs = get_object_or_404(Kurs, url=kurs)

    ready_to_save = request.REQUEST.get('ready_to_save', False)

    initial = {'email': request.user.email}

    if request.method == 'POST':
        form = AnmeldungForm(request.POST, initial=initial)
        if form.is_valid() and not 'change' in request.POST:
            form.make_immutable()
            ready_to_save = True
            if 'save' in request.POST:
                anmeldung = form.save(commit=False)
                anmeldung.kurs = kurs
                anmeldung.save()
                request.session['anmeldung'] = anmeldung
                return redirect('anmeldung_done')
    else:
        form = AnmeldungForm(initial=initial)

    return render(request, 'anmeldung/form.html', {
        'kurs': kurs,
        'ready_to_save': ready_to_save,
        'form': form
    })


def anmeldung_done(request):
    return render(request, 'anmeldung/done.html', {
        'anmeldung': request.session.get('anmeldung', None)
    })
