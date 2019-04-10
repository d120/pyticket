"""This module wraps the cron command"""
from datetime import datetime, timedelta
import pytz

from django.core.management.base import BaseCommand, CommandError
from ticket.models import Ticket
from account.models import MyUser
from notification.models import EmailBucket
from notification.functions import send_email_now, send_ticket_deadline_notification


class Command(BaseCommand):
    help = 'Run maintenance tasks like reminders'

    def handle(self, *args, **options):
        # schedule recurring tickets
        tickets = Ticket.objects.exclude(recurrences__isnull=True).exclude(
            recurrences__exact=""
        )
        # iterate over the recurring tickets
        for ticket in tickets:
            tz = pytz.timezone("Europe/Berlin")
            today = datetime.combine(datetime.now(), datetime.min.time())
            today = tz.localize(today)
            # get the next occurences of the ticket
            occ = ticket.recurrences.after(
                today,
                inc=True,
                dtstart=datetime(2010, 1, 1, 0, 0, 0).replace(tzinfo=pytz.utc),
            )
            # get the next day
            tomorrow = today + timedelta(days=1)
            # if next occurence is tomorrow
            if occ.date() == tomorrow.date():
                # create a new duplicate of the ticket
                dup = ticket
                dup.pk = None
                dup.id = None
                dup.state = "open"
                dup.assigned_user = None
                dup.time_assign_user = None
                dup.accepted = False
                dup.created_at = datetime.now()
                dup.updated_at = datetime.now()
                dup.deadline = None
                dup.recurrences = ""
                dup.save()
        # notify users if deadline is reached
        tickets_notify = Ticket.objects.filter(accepted=True, deadline=datetime.today())
        for ticket in tickets_notify:
            send_ticket_deadline_notification(ticket)

        # send email summary
        users = MyUser.objects.all()
        for user in users:

            emails_to_send = EmailBucket.objects.filter(send_to=user, sent=False)
            if emails_to_send:
                message = ""
                for email in emails_to_send:
                    message += email.message + "\n"
                    email.sent = True
                    email.save()

                subject = "Deine Tägliche Zusammenfassung"

                send_email_now([].append(user.email), subject, message)
