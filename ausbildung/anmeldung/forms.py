
from django import forms

from .models import Anmeldung


class AnmeldungForm(forms.ModelForm):

    class Meta:
        model = Anmeldung
        exclude = ('kurs', 'user')

    def make_immutable(self):
        for name, field in self.fields.iteritems():
            field.widget.attrs['readonly'] = 'readonly'

