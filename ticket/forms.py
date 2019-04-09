from django.forms import ModelForm
from .models import Ticket, Comment
from django import forms
from datetime import date
from dateutil.relativedelta import relativedelta
from bootstrap_datepicker_plus import DatePickerInput
from django.utils.translation import ugettext_lazy as _

def valid_deadline(value):
	"""
	validate deadline: checks if given date is in the past
						or in the remote future(10 years from now)
	param: value(datetime.date) - given date which we want to validate
	return: value if no error else ValidationError
	"""
	today = date.today()
	upper_limit = today + relativedelta(years=10)
	if value < today:
		raise forms.ValidationError(_('Das Datum darf nicht in der Vergangenheit liegen.'))
	if value > upper_limit:
		raise forms.ValidationError(_('Das Datum liegt zu weit in der Zukunft.'))
	return value

class AddTicketForm(ModelForm):
	"""
	modelform for creating a ticket, used in new_ticket.html/ NewTicketView
	"""
	deadline = forms.DateField(input_formats=['%d.%m.%Y'],widget=DatePickerInput(format='%d.%m.%Y',attrs={'placeholder': 'TT.MM.JJJJ'}, options={
                    "showTodayButton": False,
					"locale": "de-DE",
					"minDate": date.today().isoformat(),
					"allowInputToggle": True,
					"keepInvalid": False,
					"useCurrent": False,
                }), required=False, help_text=_("Der Tag bis das Ticket erledigt sein soll."), validators=[valid_deadline])
	class Meta:
		model = Ticket
		fields = ["name", "text", "assigned_user", "assigned_group", "priority", "deadline"]

class AddCommentForm(ModelForm):
	"""
	modelform for adding a comment to a ticket
	used in ShowTicketView/show_ticket.html
	"""
	class Meta:
		model = Comment
		fields = ["comment"]
		labels = {
			"comment": _("Schreibe einen Kommentar"),
		}
		widgets = {
            'comment': forms.Textarea(
                attrs={'placeholder': _('Schreibe einen Kommentar')}),
        }

class EditTicketForm(ModelForm):
	"""
	modelform for editing a ticket
	used in EditTicketView/edit_ticket.html
	"""
	deadline = forms.DateField(input_formats=['%d.%m.%Y'],widget=DatePickerInput(format='%d.%m.%Y',attrs={'placeholder': 'TT.MM.JJJJ'}, options={
                    "showTodayButton": False,
					"locale": "de-DE",
					"minDate": date.today().isoformat(),
					"allowInputToggle": True,
					"keepInvalid": True,
					"useCurrent": False,
                }), required=False, help_text=_("Der Tag bis das Ticket erledigt sein soll."))
	class Meta:
		model = Ticket
		fields = ["name", "state", "text", "assigned_user", "assigned_group", "priority", "deadline"]

	def clean(self):
		"""
		overrides modelform clean method
		checks if given deadline is valid else raises ValidationError
		"""
		cleaned_data = super().clean()
		if self.has_changed() and self.is_valid():
			if 'deadline' in self.changed_data:
				try:
					valid_deadline(self.cleaned_data["deadline"])
				except forms.ValidationError as err:
					self.add_error('deadline', err)
