from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    """
    Form for the login page.
    username: input box for the username
    password: input box for the password
    """
    username = forms.CharField(label=_('Nutzername'), max_length=100)
    password = forms.CharField(label=_("Passwort"), widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(
                _("Entschuldigung, die eingegebenen Daten sind ungültig."))
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class SettingsForm(forms.Form):
    """
    Form for the available settings
    sending_email_once_a_day: activating the daily activity summary
    """
    sending_email_once_a_day = forms.BooleanField(
        label=_("Sende mir täglich eine Zusammenfassung per E-Mail."),
        required=False,
        help_text=_("Gibt an, ob du über alle Aktivitäten gesammelt oder über "
                  "jede Aktivität einzeln benachrichtigt wirst."))