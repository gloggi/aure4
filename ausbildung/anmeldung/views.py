
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Kurs, Notfallblatt

from .forms import AbteilungForm, AnmeldungForm, NotfallblattForm


def requires_anmeldung(view):
    def wrap(request, kurs, *args, **kwargs):
        try:
            anmeldung = request.user.anmeldungen.get(kurs__url=kurs)
        except:
            return redirect('anmeldung_form', kurs=kurs)
        return view(request, anmeldung, *args, **kwargs)
    return wrap


def index(request):
    return redirect('kurse_list')


def kurse_list(request):
    kurse = Kurs.objects.open()

    if request.user.is_authenticated():
        angemeldete_kurse = request.user.angemeldete_kurse.all()
    else:
        angemeldete_kurse = ()

    return render(request, 'kurse/list.html', {
        'kurse': kurse,
        'angemeldete_kurse': angemeldete_kurse,
    })


@login_required
def anmeldung_form(request, kurs):
    kurs = get_object_or_404(Kurs, url=kurs)

    if request.user in kurs.teilnehmer.all():
        return redirect('anmeldung_view', kurs=kurs.url)

    if kurs.kursplaetze and kurs.freie_plaetze <= 0:
        return render(request, 'anmeldung/fully_booked.html', {
            'kurs': kurs
        })

    initial = {'email': request.user.email}

    if request.method == 'POST':
        data = request.POST.copy()
        if data.get('abteilung', '') == 'andere':
            abtform = AbteilungForm(data)
            if abtform.is_valid():
                abteilung = abtform.save()
                data['abteilung'] = abteilung.id
        else:
            abtform = AbteilungForm()

        form = AnmeldungForm(data, request.FILES, initial=initial)
        if form.is_valid():
            anmeldung = form.save(commit=False)
            anmeldung.kurs = kurs
            anmeldung.user = request.user
            anmeldung.save()
            return redirect('anmeldung_view', kurs=kurs.url)
    else:
        form = AnmeldungForm(initial=initial)
        abtform = AbteilungForm()

    return render(request, 'anmeldung/form.html', {
        'kurs': kurs,
        'form': form,
        'abtform': abtform
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


@login_required
@requires_anmeldung
def notfallblatt_form(request, anmeldung):
    kurs = anmeldung.kurs

    try:
        notfallblatt = anmeldung.notfallblatt
        return redirect('notfallblatt_edit', kurs=kurs.url)
    except Notfallblatt.DoesNotExist:
        pass

    if request.method == 'POST':
        form = NotfallblattForm(request.POST)
        if form.is_valid():
            notfallblatt = form.save(commit=False)
            notfallblatt.anmeldung = anmeldung
            notfallblatt.save()
            return redirect('anmeldung_view', kurs=kurs.url)
    else:
        form = NotfallblattForm()

    return render(request, 'notfallblatt/form.html', {
        'form': form,
        'kurs': kurs
    })


@login_required
@requires_anmeldung
def notfallblatt_edit(request, anmeldung):
    kurs = anmeldung.kurs
    try:
        notfallblatt = anmeldung.notfallblatt
    except Notfallblatt.DoesNotExist:
        return redirect('anmeldung_view', kurs=kurs.url)

    if request.method == 'POST':
        form = NotfallblattForm(request.POST, instance=notfallblatt)
        if form.is_valid():
            form.save()
            return redirect('anmeldung_view', kurs=kurs.url)
    else:
        form = NotfallblattForm(instance=notfallblatt)

    return render(request, 'notfallblatt/form.html', {
        'form': form,
        'kurs': kurs
    })
