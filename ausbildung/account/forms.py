
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _


class EmailAuthenticationForm(forms.Form):
    """
    Form for authenticating users by their email address.
    """
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                'class': 'input-xlarge',
                'required': True
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Passwort',
                'class': 'input-xlarge',
                'required': True
            }
        )
    )

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email', '').lower()
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    'Anmeldung fehlgeschlagen. Bitte nochmals probieren')
            elif not self.user_cache.is_active:
                raise forms.ValidationError("Account inaktive")
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(
                _("Your Web browser doesn't appear to have cookies enabled. "
                  "Cookies are required for logging in."))

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
