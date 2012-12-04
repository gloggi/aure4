
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Kurs, Anmeldung

from .forms import AnmeldungForm


def requires_anmeldung(view):
    def wrap(request, kurs, *args, **kwargs):
        anmeldung = get_object_or_404(request.user.anmeldungen, kurs__url=kurs)
        return view(request, anmeldung, *args, **kwargs)
    return wrap


def kurse(request):
    kurse = Kurs.objects.open()

    return render(request, 'anmeldung/kurse.html', {
        'kurse': kurse,
    })


@login_required
def anmeldung(request, kurs):
    kurs = get_object_or_404(Kurs, url=kurs)

    if request.user in kurs.teilnehmer.all():
        return redirect('anmeldung_view', kurs=kurs.url)

    ready_to_save = request.REQUEST.get('ready_to_save', False)

    initial = {'email': request.user.email}

    if request.method == 'POST':
        form = AnmeldungForm(request.POST, request.FILES, initial=initial)
        if form.is_valid() and not 'change' in request.POST:
            form.make_immutable()
            ready_to_save = True
            if 'save' in request.POST:
                anmeldung = form.save(commit=False)
                anmeldung.kurs = kurs
                anmeldung.user = request.user
                anmeldung.save()
                return redirect('anmeldung_view', kurs=kurs.url)
    else:
        form = AnmeldungForm(initial=initial)

    return render(request, 'anmeldung/form.html', {
        'kurs': kurs,
        'ready_to_save': ready_to_save,
        'form': form
    })


@login_required
@requires_anmeldung
def anmeldung_edit(request, anmeldung):
    kurs = anmeldung.kurs
    if request.method == 'POST':
        form = AnmeldungForm(request.POST, request.FILES, instance=anmeldung)
        if form.is_valid():
            anmeldung = form.save()
            return redirect('anmeldung_view', kurs=kurs.url)
    else:
        form = AnmeldungForm(instance=anmeldung)

    return render(request, 'anmeldung/form.html', {
        'edit': True,
        'kurs': kurs,
        'form': form
    })


@login_required
@requires_anmeldung
def anmeldung_view(request, anmeldung):
    return render(request, 'anmeldung/view.html', {
        'kurs': anmeldung.kurs,
        'anmeldung': anmeldung
    })


@login_required
@requires_anmeldung
def anmeldung_print(request, anmeldung):
    return render(request, 'anmeldung/print.html', {
        'a': anmeldung,
    })
