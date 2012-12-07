from django import forms

from .models import Abteilung, Anmeldung, Notfallblatt


class AbteilungForm(forms.ModelForm):
    class Meta:
        model = Abteilung

    def save(self, *args, **kwargs):
        # Dont' save if an exact copy already exist
        try:
            return Abteilung.objects.get(**self.cleaned_data)
        except Abteilung.DoesNotExist:
            return super(AbteilungForm, self).save(*args, **kwargs)


class AnmeldungForm(forms.ModelForm):
    class Meta:
        model = Anmeldung
        exclude = ('kurs', 'user', 'anmeldung_erhalten', 'notfallblatt_erhalten',
                   'bezahlt')

    def __init__(self, *args, **kwargs):
        super(AnmeldungForm, self).__init__(*args, **kwargs)
        choices = tuple(self.fields['abteilung'].choices)
        choices += (('andere', 'Andere Abteilung'),)
        self.fields['abteilung'].choices = choices

    def make_immutable(self):
        for name, field in self.fields.iteritems():
            field.widget.attrs['readonly'] = 'readonly'


class NotfallblattForm(forms.ModelForm):
    class Meta:
        model = Notfallblatt
        exclude = ('anmeldung',)
