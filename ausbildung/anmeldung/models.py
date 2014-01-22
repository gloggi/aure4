# encoding: utf-8

from django import forms
from django.db import models
from django.utils.timezone import now
from django.template.defaultfilters import slugify

from autoslug import AutoSlugField

from sorl.thumbnail import ImageField

from .fields import RequiredCharField, OptionalCharField, JSONField


class KursManager(models.Manager):
    def open(self):
        return self.get_query_set().filter(anmeldeschluss__gte=now())

    def online(self):
        return self.filter(online=True)

class Kurs(models.Model):

    online = models.BooleanField('Online', help_text='Auf Webseite anzeigen',
        default=True)

    name = RequiredCharField('Name')
    url = models.SlugField('url')

    order = models.IntegerField('Reihenfolge', blank=True, null=True)

    nummer = OptionalCharField('Kursnummer', help_text='z.Bsp PBS ZH 123-12')

    lagerbeitrag = models.PositiveIntegerField('Lagerbeitrag', default=150,
        help_text='CHF')

    von = models.DateField('Von')
    bis = models.DateField('Bis')
    anmeldeschluss = models.DateField('Anmeldeschluss')

    jahrgang = models.SmallIntegerField(blank=True, null=True)

    hauptleiter = OptionalCharField('HauptleiterInn')
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
        ordering = ('order',)

    def __unicode__(self):
        return u'%s %d' % (self.name, self.von.year)

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
    required = models.BooleanField('Plichtfeld', default=True)
    label = RequiredCharField('Bezeichnung')
    help_text = OptionalCharField('Hilfstext')

    @property
    def name(self):
        return self.label.lower()

    def form_field(self):
        kwargs = {
            'label': self.label,
            'help_text': self.help_text,
            'required': self.required
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

    slug = AutoSlugField(populate_from='name', unique=True)

    abteilungsleitung = models.ManyToManyField('auth.User',
        through='Abteilungsleitung', related_name='abteilungen')

    class Meta:
        verbose_name = 'Abteilung'
        verbose_name_plural = 'Abteilungen'

    def __unicode__(self):
        return u'%s - %s' % (self.region, self.name)


class Abteilungsleitung(models.Model):

    abteilung = models.ForeignKey(Abteilung, related_name='leiter')
    user = models.ForeignKey('auth.User', related_name='al')

    seit = models.DateField(default=now)
    bis = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Abteilungsleiter'
        verbose_name_plural = 'Abteilungsleiter'

    def __unicode__(self):
        return u'AL %s von %s' % (self.abteilung, self.user)


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
    erstellt = models.DateTimeField('zuletzt aktualisiert', auto_now=True)
    aktualisiert = models.DateTimeField('eingegangen', auto_now_add=True)

    anmeldung_erhalten = models.DateField('Anmeldung im Seki',
        blank=True, null=True,
        help_text='Wann ist die unterschrieben Anmeldung im Seki angekommen')
    notfallblatt_erhalten = models.DateField('Notfallblatt im Seki',
        blank=True, null=True,
        help_text='Wann ist das Notfallblatt im Seki angekommen')
    bezahlt = models.DateField('Bezahlt am', blank=True, null=True,
        help_text='Wann ist die Zahlung eingegangen')

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

    vegetarier = models.BooleanField('Vegi',
        help_text="Ich bin Vegetarier"
    )
    schweinefleisch = models.BooleanField('Kein Schweinefleich',
        help_text="Ich esse kein Schweinefleich"
    )

    bestaetigung = models.BooleanField(u'Bestätigung',
        help_text=u'Ich benötige eine Bestätigung für meinen Arbeitsgeber')

    zusatz = JSONField('Zusatzdaten', blank=True, null=True)

    class Meta:
        verbose_name = 'Anmeldung'
        verbose_name_plural = 'Anmeldungen'
        unique_together = (('kurs', 'user'),)

    def __unicode__(self):
        return u'%s %s v/o %s' % (self.vorname, self.nachname, self.pfadiname)

    def tr_class(self):
        try:
            print self.alfeedback
            if self.alfeedback.ok:
                return 'success'
            else:
                return 'error'
        except:
            return 'warning'

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
    unfallversicherung = RequiredCharField('Unfallversicherung')
    rega = models.BooleanField('Rega-Gönner',
        help_text='Gönner der Schweizerischen Rettungsflugwacht (Rega)')

    # Hausarzt
    arzt_name = OptionalCharField('Voller Name',
        help_text="z.Bsp Dr. med. Christian und Ursula Koeppel | Allgemeine Medizin FMH")
    arzt_strasse = OptionalCharField('Strasse')
    arzt_plz = models.IntegerField('PLZ', blank=True, null=True)
    arzt_ort = OptionalCharField('Ort')
    arzt_telefon = OptionalCharField('Telefon Praxis')

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


class ALFeedback(models.Model):

    anmeldung = models.OneToOneField(Anmeldung)

    erstellt = models.DateTimeField(auto_now=True)
    aktualisiert = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey('auth.User', verbose_name='Erstellt von')

    ok = models.BooleanField('AL OK', default=True)

    mitteilung = models.TextField('Mitteilung',
        help_text='In welchen Bereichen soll die/der TN speziell '
            'gefördert werden, Bemerkungen, Begründung Ablehnung')

    kontaktperson = models.CharField('Kontaktperson', max_length=255,
        help_text='Kontaktperson der Abteilung / an wen kann sich die '
            'Kursleitung bei Fragen wenden')

    mobiltelefon = models.CharField('Natelnummer der Kontaktperson',
        max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'ALFeedback'
        verbose_name_plural = 'ALFeedbacks'

    def __unicode__(self):
        return u'Bestätgung für %s von %s' % (self.anmeldung, self.user)
