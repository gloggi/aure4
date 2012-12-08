# encoding: utf-8

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from sorl.thumbnail import ImageField

from ausbildung.anmeldung.fields import OptionalCharField
from ausbildung.anmeldung.models import Abteilung, Anmeldung


class Profil(models.Model):

    user = models.OneToOneField(User)

    erstellt = models.DateTimeField(auto_now=True)
    aktualisiert = models.DateTimeField(auto_now_add=True)

    # Personendaten
    pfadiname = OptionalCharField('Pfadiname')

    geschlecht = OptionalCharField('Geschlecht',
        choices=Anmeldung.GESCHLECHT_CHOICES)
    geburtsdatum = models.DateField('Geburtsdatum', blank=True, null=True)

    foto = ImageField('Foto', upload_to="tnfotos", blank=True, null=True)

    strasse = OptionalCharField('Strasse')
    plz = models.IntegerField('PLZ', blank=True, null=True)
    ort = OptionalCharField('Ort')
    land = OptionalCharField('Land',
        choices=Anmeldung.LAND_CHOICES, default='CH')

    telefon = OptionalCharField('Telefon')
    mobiltelefon = OptionalCharField('Natel')

    # Pfadizugehörigkeit
    abteilung = models.ForeignKey(Abteilung, verbose_name='Abteilung',
        blank=True, null=True)
    einheit = OptionalCharField('Einheit')
    stufe = OptionalCharField('Stufe', choices=Anmeldung.STUFE_CHOICES)

    # Weiteres
    nationalitaet = OptionalCharField(u'Nationalität', default='CH')
    erstsprache = OptionalCharField('Erstsprache',
        choices=Anmeldung.ERSTSPRACHE_CHOICES, default='')
    bahnabo = OptionalCharField('Bahnabo', choices=Anmeldung.BAHNABO_CHOICES,
        default='Keines')

    vegetarier = models.BooleanField('Vegetarier',
        help_text="Ich bin Vegetarier"
    )
    schweinefleisch = models.BooleanField('Kein Schweinefleich',
        help_text="Ich esse kein Schweinefleich"
    )


@receiver(post_save, sender=Anmeldung)
def update_profile(sender, instance, *args, **kwargs):
    a = instance
    u = a.user
    p, created = Profil.objects.get_or_create(user=a.user)

    u.first_name = a.vorname
    u.last_name = a.nachname
    u.save()

    p.pfadiname = a.pfadiname
    p.geschlecht = a.geschlecht
    p.geburtsdatum = a.geburtsdatum

    p.foto = a.foto
    p.strasse = a.strasse
    p.plz = a.plz
    p.ort = a.ort
    p.land = a.land

    p.telefon = a.telefon
    p.mobiltelefon = a.mobiltelefon

    p.abteilung = a.abteilung
    p.einheit = a.einheit
    p.stufe = a.stufe

    p.nationalitaet = a.nationalitaet
    p.erstsprache = a.erstsprache
    p.bahnabo = a.bahnabo

    p.vegetarier = a.vegetarier
    p.schweinefleisch = a.schweinefleisch
    p.save()
