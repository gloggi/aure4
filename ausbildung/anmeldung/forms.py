# encoding: utf-8

from django import forms
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError

from .models import Abteilung, Anmeldung, Notfallblatt, ALFeedback


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
    tos = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'required':'required'})
    )

    class Meta:
        model = Anmeldung
        exclude = ('kurs', 'user', 'anmeldung_erhalten', 'notfallblatt_erhalten',
                   'bezahlt')

    def __init__(self, *args, **kwargs):
        super(AnmeldungForm, self).__init__(*args, **kwargs)
        if not self.instance.id:
            choices = tuple(self.fields['abteilung'].choices)
            choices += (('andere', 'Andere Abteilung'),)
            self.fields['abteilung'].choices = choices

    def clean_tos(self):
        tos = self.cleaned_data.get('tos', False)
        if not tos:
            raise ValidationError('Du musst die Anmeldebedingungen akzeptieren')
        return tos

    def make_immutable(self):
        for name, field in self.fields.iteritems():
            field.widget.attrs['readonly'] = 'readonly'


class NotfallblattForm(forms.ModelForm):
    class Meta:
        model = Notfallblatt
        exclude = ('anmeldung',)


class Horizontal(forms.RadioSelect.renderer):

    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


BLOCKINPUT = {'class': 'input-block-level'}

YES_OR_NO = (
    (True, u'Ja, ich bestätige diese Anmeldung'),
    (False, u'Nein, aus folgendem Grund')
)


class ALFeedbackForm(forms.ModelForm):
    ok = forms.TypedChoiceField(
        label=u'Bestätigung',
        choices=YES_OR_NO,
        widget=forms.RadioSelect(renderer=Horizontal),
        required=True
    )

    class Meta:
        model = ALFeedback
        exclude = ('user',)
        widgets = {
            'anmeldung': forms.HiddenInput(),
            'mitteilung': forms.Textarea(attrs=BLOCKINPUT),
            'kontaktperson': forms.TextInput(attrs=BLOCKINPUT),
            'mobiltelefon': forms.TextInput(attrs=BLOCKINPUT),
        }
