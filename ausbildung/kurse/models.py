# encoding: utf-8

from django.db import models

from django_countries import CountryField

from .fields import Required, Optional

class Kurs(models.Model):
    
    name = Required('Name')
    nummer = Optional('Kursnummer', help_text='z.Bsp PBS ZH 123-12')
    
    von = models.DateField('Von')
    bis = models.DateField('Bis')
    
    hauptleiter = Optional('Hauptleiter')
    email = models.EmailField('Email', blank=True, null=True)
    
    erfasst = models.DateTimeField('Erfasst', auto_now_add=True)
    aktualisiert = models.DateTimeField('Aktualisiert', auto_now=True)
    
    class Meta:
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurse'
        
    def __unicode__(self):
        return self.name
        
class Anmeldung(models.Model):

    GESCHLECHT_CHOICES = (
        ('m', u'männlich'),
        ('f', u'weiblich'),
    )

    BAHNABO_CHOICES = (
        ('Keines', u'Keines'),
        ('GA', u'GA'),
        ('1/2', u'Halbtax'),
        ('G7', u'Gleis 7'),
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
    geschlecht = Required('Geschlecht', choices=GESCHLECHT_CHOICES)
    
    pfadiname = Required('Pfadiname')
    vorname = Required('Vorname')
    nachname = Required('Nachname')
    
    strasse = Required('Strasse')
    plz = models.IntegerField('PLZ')
    ort = Required('Ort')
    
    telefon = Optional('Telefon')
    mobiltelefon = Required('Mobiltelefon')
    
    nationalitaet = CountryField(u'Nationalität', default='CH')
    bahnabo = Required('Bahnabo', choices=BAHNABO_CHOICES, default=u'Keines')
    
    abteilung = Required('Abteilung')
    einheit = Required('Einheit')
    stufe = Required('Stufe', choices=STUFE_CHOICES)
    
    geburtsdatum = models.DateField('Geburtsdatum')
    ahv = Optional('AHV-Nr.')
    
    email = models.EmailField('Email')
    
    vegetarier = models.BooleanField('Vegetarier')
    schweinefleisch = models.BooleanField('Kein Schweinefleich')
    
    bestaetigung = models.BooleanField('Bestätigung', 
        help_text=u'Isch benötige eine Bestätigung für den Arbeitsgeber')
    
    class Meta:
        verbose_name = 'Ammeldung'
        verbose_name_plural = 'Anmeldungen'
        
    def __unicode__(self):
        return u'%s %s v/o %s' % (self.vorname, self.nachname, self.pfadiname)
    
