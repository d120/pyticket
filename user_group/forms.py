from django.forms import ModelForm
from ajax_select.fields import AutoCompleteSelectMultipleField
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _


class AddGroupForm(ModelForm):
    """
    Form to add user to a group.
    members: input box with search function to search for users
    """
    class Meta:
        model = Group
        exclude = ['permissions']
    # not part of model Group, adds a FormField for selecting members of the group
    members = AutoCompleteSelectMultipleField('look_members', required=True,
                                              help_text=_(
                                                  "Suche nach Mitgliedern(Nutzername, Vor- und Nachname). Vorgeschlagene Nutzer auswählen."),
                                                label='Mitglieder',
                                              widget_options={'attrs': {
                                                  'placeholder': _(
                                                      'Suche nach Nutzern')}})
