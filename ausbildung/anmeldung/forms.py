
from django import forms

from .models import Anmeldung


class AnmeldungForm(forms.ModelForm):

    class Meta:
        model = Anmeldung
        exclude = ('kurs',)
