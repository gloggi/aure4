# encoding: utf-8

from django.db import models

from .fields import RequiredCharField, OptionalCharField


class Kurs(models.Model):
    # Just some Comment

    CONST = 'HUU'

    name = RequiredCharField('Name')
    nummer = OptionalCharField('Kursnummer', help_text='z.Bsp PBS ZH 123-12')

    von = models.DateField('Von')
    bis = models.DateField('Bis')

    hauptleiter = OptionalCharField('Hauptleiter')
    email = models.EmailField('Email', blank=True, null=True)

    erfasst = models.DateTimeField('Erfasst', auto_now_add=True)
    aktualisiert = models.DateTimeField('Aktualisiert', auto_now=True)

    class Meta:
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurse'

    def __unicode__(self):
        return self.name

    @property
    def foo(self, erwin):
        pass


class Abteilung(models.Model):

    name = RequiredCharField('Name')
    region = OptionalCharField('Region / Korps',
        help_text='Z.Bsp. Gloggi, Flamberg oder Züri Oberland')
    verband = OptionalCharField('Kantonalverband', default='ZH')

    class Meta:
        verbose_name = 'Abteilung'
        verbose_name_plural = 'Abteilungen'

    def __unicode__(self):
        return self.name


class Anmeldung(models.Model):

    GESCHLECHT_CHOICES = (
        (1, u'männlich'),
        (2, u'weiblich'),
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

    kurs = models.ForeignKey(Kurs)

    # Personendaten
    geschlecht = RequiredCharField('Geschlecht', choices=GESCHLECHT_CHOICES)

    pfadiname = RequiredCharField('Pfadiname')
    vorname = RequiredCharField('Vorname')
    nachname = RequiredCharField('Nachname')
    geburtsdatum = models.DateField('Geburtsdatum')

    strasse = RequiredCharField('Strasse')
    plz = models.IntegerField('PLZ')
    ort = RequiredCharField('Ort')
    land = RequiredCharField('Land', choices=LAND_CHOICES, default='CH')

    nationalitaet = RequiredCharField(u'Nationalität', default='CH')
    erstsprache = RequiredCharField('Erstsprache', choices=ERSTSPRACHE_CHOICES,
        default='')
    bahnabo = RequiredCharField('Bahnabo', choices=BAHNABO_CHOICES,
        default='Keines')

    abteilung = models.ForeignKey(Abteilung, verbose_name='Abteilung',
        blank=True, null=True)

    einheit = RequiredCharField('Einheit')
    stufe = RequiredCharField('Stufe', choices=STUFE_CHOICES)

    js = models.IntegerField('JS-Nummer', blank=True, null=True)
    ahv = OptionalCharField('AHV-Nr.')

    email = models.EmailField('Email')
    telefon = OptionalCharField('Telefon')
    mobiltelefon = OptionalCharField('Mobiltelefon')

    essen = OptionalCharField('Essgewohnheiten', max_length=1000,
        help_text='Vegetarier, kein Schweinefleich, Allergien etc.')
    gesundheit = OptionalCharField('Gesunheitszustand', max_length=1000,
        help_text='Gesundheitliche Beschwerden, benötigte Medikamente etc.')

    bestaetigung = models.BooleanField('Bestätigung',
        help_text=u'Ich benötige eine Bestätigung für den Arbeitsgeber')

    class Meta:
        verbose_name = 'Ammeldung'
        verbose_name_plural = 'Anmeldungen'

    def __unicode__(self):
        return u'%s %s v/o %s' % (self.vorname, self.nachname, self.pfadiname)