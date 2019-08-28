from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .mistune_custom_renderer import CustomMarkdown, ListRenderer, CustomLexer
from recurrence.fields import RecurrenceField
from django.utils.translation import ugettext_lazy as _
import pytz

STATE_CHOICES = (
    ('done', 'done'),
    ('open', 'open'),
)

PRIORITY_CHOICES = (
    ('high', 'high'),
    ('normal', 'normal'),
    ('low', 'low'),
)

STATE_LOG = (
    ('add', "ADD"),
    ('accepted', "ACCEPTED"),
    ('rejected', "REJECTED"),
    ('closed','CLOSED'),
    ('changed', "CHANGED"),
)




class Ticket(models.Model):
    name = models.CharField(max_length=255,
                            help_text=_("Eine kurze Beschreibung der Aufgabe"))
    state = models.CharField("Status", max_length=4, choices=STATE_CHOICES,
                             default='open',
                             help_text=_("Der aktuelle Status des Tickets"))
    assigned_user = models.ForeignKey(get_user_model(),
                                      on_delete=models.SET_NULL, blank=True,
                                      null=True, related_name="assigned_tasks",
                                      verbose_name="zugewiesener Nutzer",
                                      help_text=_("Der Nutzer, der für diese Aufgabe verantwortlich ist. Er bekommt die Aufgabe in die Inbox und kann sie dann annehmen oder ablehnen."))
    time_assign_user = models.DateTimeField(default=datetime.now, blank=True,
                                            null=True)
    assigned_group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                                        blank=True, null=True, verbose_name="gruppe",
                                       help_text=_("Die Gruppe, für die das Ticket interessant ist."))
    accepted = models.BooleanField("Akzeptiert", default=False)
    text = models.TextField(
        help_text=_("Eine ausführlichere Beschreibung der Aufgabe"), blank=True,
        null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    priority = models.CharField("Priorität", max_length=6, choices=PRIORITY_CHOICES,
                                default='normal',
                                help_text=_("Die Dringlichkeit des Tickets."))
    creator_user = models.ForeignKey(get_user_model(), verbose_name="ersteller",
                                     on_delete=models.SET_NULL, blank=True,
                                     null=True, related_name="created_tasks",
                                     help_text=_("Der Nutzer, der diese Aufgabe erstellt hat."))
    deadline = models.DateField(blank=True, null=True)
    recurrences = RecurrenceField(blank=True, default='',
                                verbose_name="wiederholungen")
    # only used if ticket is a group ticket
    ignored_by = models.ManyToManyField(get_user_model(), blank=True, verbose_name="ignoriert bei")
    # only used for assigned_user
    rejected = models.BooleanField("abgelehnt", default=False)
    # does not consider self assignments
    dispatcher = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                                   blank=True, null=True,
                                   related_name="dispatcher",
                                   verbose_name="zuteiler")

    def __str__(self):
        return self.name

    @property
    def get_markdown(self):
        """
        used on show_ticket.html
        return: String - saved text as parsed html
        """
        renderer = ListRenderer(escape=True)
        block_lexer = CustomLexer()
        markdown = CustomMarkdown(renderer=renderer, block=block_lexer)
        return markdown(self.text)

    @property
    def get_nextOccurence(self):
        """
        used on recurring_ticket.html
        return: datetime.date - next date of recurrence of the ticket
        """
        if (self.recurrences):
            tz = pytz.timezone('Europe/Berlin')
            nextocc= self.recurrences.after(
                tz.localize(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)),
                inc=True, dtstart=datetime(2010,1,1,0,0,0).replace(tzinfo=pytz.utc),
            )
            if(nextocc):
                nextocc = nextocc.date()
            return nextocc

class Log(models.Model):
    before = models.TextField(null=True)
    after = models.TextField(null=True)
    fieldname = models.CharField(max_length=255)

    def __str__(self):
        return self.fieldname


class TicketLog(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                             blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=100, choices=STATE_LOG)
    message = models.TextField(blank=True)
    changes = models.ManyToManyField(Log)


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    # user = User
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
