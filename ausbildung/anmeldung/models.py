# encoding: utf-8

from django import forms
from django.db import models
from django.utils.timezone import now

from sorl.thumbnail import ImageField

from .fields import RequiredCharField, OptionalCharField


class KursManager(models.Manager):
    def open(self):
        return self.get_query_set().filter(anmeldeschluss__gte=now())


class Kurs(models.Model):
    name = RequiredCharField('Name')
    url = models.SlugField('url')

    nummer = OptionalCharField('Kursnummer', help_text='z.Bsp PBS ZH 123-12')

    von = models.DateField('Von')
    bis = models.DateField('Bis')
    anmeldeschluss = models.DateField('Anmeldeschluss')

    hauptleiter = OptionalCharField('Hauptleiter')
    email = models.EmailField('Email', blank=True, null=True)

    erfasst = models.DateTimeField('Erfasst', auto_now_add=True)
    aktualisiert = models.DateTimeField('Aktualisiert', auto_now=True)

    kursplaetze = models.IntegerField(u'Kursplätze', blank=True, null=True,
        help_text='Maximale Anzahl Teilnehmer')

    teilnehmer = models.ManyToManyField('auth.User', through='Anmeldung',
        related_name="angemeldete_kurse")

    objects = KursManager()

    class Meta:
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurse'

    def __unicode__(self):
        return self.name

    @property
    def freie_plaetze(self):
        if self.kursplaetze:
            return self.kursplaetze - self.teilnehmer.count()
        else:
            return u'Unbeschränkt'

    def zusatzform(self):
        felder = {}
        for feld in self.zusatzfelder.all():
            felder[feld.name] = feld.form_field()

        return type('ZusatzForm', (forms.Form,), felder)


class Zusatzfeld(models.Model):
    TYP_CHOICES = (
        ('char', 'Textfeld'),
        ('checkbox', 'Checkbox'),
        ('integer', 'Zahl'),
        ('textarea', 'Langer Text'),
    )

    kurs = models.ForeignKey(Kurs, related_name='zusatzfelder')
    typ = RequiredCharField('Typ', choices=TYP_CHOICES)
    label = RequiredCharField('Bezeichnung')
    help_text = OptionalCharField('Hilfstext')

    @property
    def name(self):
        return self.label.lower()

    def form_field(self):
        kwargs = {
            'label': self.label,
            'help_text': self.help_text,
            'required': False,
        }

        if self.typ == 'char':
            return forms.CharField(**kwargs)
        elif self.typ == 'checkbox':
            return forms.BooleanField(**kwargs)
        if self.typ == 'integer':
            return forms.IntegerField(**kwargs)
        if self.typ == 'textarea':
            return forms.CharField(widget=forms.TextInput, **kwargs)

    class Meta:
        verbose_name = 'Zusatzfeld'
        verbose_name_plural = 'Zusatzfelder'

    def __unicode__(self):
        return self.label


class Abteilung(models.Model):

    verband = RequiredCharField('Kantonalverband', default='ZH')
    region = RequiredCharField('Region / Korps')
    name = RequiredCharField('Abteilungsname')

    class Meta:
        verbose_name = 'Abteilung'
        verbose_name_plural = 'Abteilungen'

    def __unicode__(self):
        return u'%s - %s' % (self.region, self.name)


class Zusatzwert(models.Model):
    anmeldung = models.ForeignKey('Anmeldung', related_name='zusatz')
    name = RequiredCharField('name', unique=True)
    wert = RequiredCharField('wert')

    class Meta:
        verbose_name = 'Zusatzwert'
        verbose_name_plural = 'Zusatzwerte'

    def __unicode__(self):
        return u'%s : %s' % (self.name, self.wert)


class Anmeldung(models.Model):

    GESCHLECHT_CHOICES = (
        ('1', u'männlich'),
        ('2', u'weiblich'),
    )

    LAND_CHOICES = (
        ('CH', 'Schweiz'),
        ('FL', 'Fürstentum Lichtenstein'),
        ('D', 'Deutschland'),
        ('F', 'Frankreich'),
        ('I', 'Italien'),
        ('A', 'Österreich'),
    )

    ERSTSPRACHE_CHOICES = (
        ('D', u'Deutsch'),
        ('F', u'Französisch'),
        ('I', u'Italienisch'),
        ('E', u'Englisch'),
    )

    BAHNABO_CHOICES = (
        ('Keines', u'Keines'),
        ('GA', u'GA'),
        ('Halbtax', u'Halbtax'),
        ('Regenbogen', u'Regenbogen'),
        ('Gleis 7', u'Gleis 7'),
    )

    STUFE_CHOICES = (
        ('biber', u'Biberstufe'),
        ('wolf', u'Wolfsstufe'),
        ('pfadi', u'Pfadistufe'),
        ('pio', u'Piostufe'),
        ('rover', u'Roverstufe'),
    )

    kurs = models.ForeignKey(Kurs, related_name='anmeldungen')
    user = models.ForeignKey('auth.User', related_name='anmeldungen')

    # Adminfelder
    erstellt = models.DateTimeField(auto_now=True)
    aktualisiert = models.DateTimeField('Zuletzt aktualisiert', auto_now_add=True)

    anmeldung_erhalten = models.DateTimeField('Unterschriebene Anmeldung erhalten',
        blank=True, null=True)
    notfallblatt_erhalten = models.DateTimeField('Notfallblatt erhalten', blank=True,
        null=True)
    bezahlt = models.DateTimeField('Zahlung eingegangen', blank=True, null=True)

    # Personendaten
    pfadiname = RequiredCharField('Pfadiname')
    vorname = RequiredCharField('Vorname')
    nachname = RequiredCharField('Nachname')
    geschlecht = RequiredCharField('Geschlecht', choices=GESCHLECHT_CHOICES)
    geburtsdatum = models.DateField('Geburtsdatum')

    foto = ImageField('Foto', upload_to="tnfotos", blank=True, null=True)

    strasse = RequiredCharField('Strasse')
    plz = models.IntegerField('PLZ')
    ort = RequiredCharField('Ort')
    land = RequiredCharField('Land', choices=LAND_CHOICES, default='CH')

    email = models.EmailField('Email')
    telefon = OptionalCharField('Telefon')
    mobiltelefon = OptionalCharField('Natel')

    # Pfadizugehörigkeit
    abteilung = models.ForeignKey(Abteilung, verbose_name='Abteilung')
    einheit = RequiredCharField('Einheit')
    stufe = RequiredCharField('Stufe', choices=STUFE_CHOICES)

    nationalitaet = RequiredCharField(u'Nationalität', default='CH')
    erstsprache = RequiredCharField('Erstsprache', choices=ERSTSPRACHE_CHOICES,
        default='')
    bahnabo = RequiredCharField('Bahnabo', choices=BAHNABO_CHOICES,
        default='Keines')

    js = models.IntegerField('JS-Nummer', blank=True, null=True)
    ahv = OptionalCharField('AHV-Nr.')

    vegetarier = models.BooleanField('Vegetarier',
        help_text="Ich bin Vegetarier"
    )
    schweinefleisch = models.BooleanField('Kein Schweinefleich',
        help_text="Ich esse kein Schweinefleich"
    )

    bestaetigung = models.BooleanField('Bestätigung',
        help_text=u'Ich benötige eine Bestätigung für meinen Arbeitsgeber')

    #zusatz = JSONField('Zusatzdaten', blank=True, null=True)

    @property
    def zusatz_initial(self):
        result = {}
        for wert in self.zusatz.all():
            result[wert.name] = wert.wert
        return result

    def update_zusatzwerte(self, zusatzdaten):
        aktualisiert = []
        for name, wert in zusatzdaten.items():
            try:
                zusatzwert = self.zusatz.get(name=name)
            except Zusatzwert.DoesNotExist:
                zusatzwert = Zusatzwert(anmeldung=self, name=name)
            zusatzwert.wert = unicode(zusatzdaten[zusatzwert.name])
            zusatzwert.save()
            aktualisiert.append(zusatzwert.id)

        for zusatzwert in self.zusatz.exclude(id__in=aktualisiert):
            zusatzwert.delete()

    class Meta:
        verbose_name = 'Ammeldung'
        verbose_name_plural = 'Anmeldungen'
        unique_together = (('kurs', 'user'),)

    def __unicode__(self):
        return u'%s %s v/o %s' % (self.vorname, self.nachname, self.pfadiname)


class Notfallblatt(models.Model):
    anmeldung = models.OneToOneField(Anmeldung)

    # Kontaktperson während dem Lager
    kontakt = RequiredCharField('Voller Name',
        help_text="z.Bsp Beide Elternteile mit Vor- und Nachnamen")
    strasse = RequiredCharField('Strasse')
    plz = models.IntegerField('PLZ')
    ort = RequiredCharField('Ort')
    land = RequiredCharField('Land')
    email = OptionalCharField('Email')
    telefon = OptionalCharField('Telefon')
    mobiltelefon = OptionalCharField('Natel')

    # Versicherung
    krankenkasse = RequiredCharField('Krankenkasse')
    rega = models.BooleanField('Rega-Gönner',
        help_text='Gönner der Schweizerischen Rettungsflugwacht (Rega)')

    # Hausarzt
    arzt_name = RequiredCharField('Voller Name',
        help_text="z.Bsp Dr. med. Christian und Ursula Koeppel | Allgemeine Medizin FMH")
    arzt_strasse = RequiredCharField('Strasse')
    arzt_plz = models.IntegerField('PLZ')
    arzt_ort = RequiredCharField('Ort')
    arzt_telefon = RequiredCharField('Telefon Praxis')

    # Gesundheitszustand
    starrkrampf = RequiredCharField('Datum der letzten Starrkrampfimpfung')

    medikamente = models.TextField('Medikamente',  blank=True,
        help_text='Regelmässig einzunehmende Medikamente ' +
                  '(Bezeichnung, Dosierung, Einnamevorschrift)'
    )

    medis_ll = models.BooleanField('Verabreichung durch Lagerleitung',
        help_text='Sollen die Medikamente durch die Leiter ' +
                  'verabreicht werden?'
    )

    gesundheitszustand = models.TextField('Gesundheitszustand', blank=True,
        help_text='Bemerkungen zum Gesundheitszustand (z.B. nachwirkende ' +
                  'Krankheiten und Unfälle, Operationen, Allergien)'
    )

    weiteres = models.TextField('Weiteres', blank=True,
        help_text='Weitere Infos, welche die Lagerleitung haben sollte')

    class Meta:
        verbose_name = 'Notfallblatt'
        verbose_name_plural = 'Notfallblätter'

    def __unicode__(self):
        return 'Notfallblatt %s' % self.anmeldung.pfadiname
