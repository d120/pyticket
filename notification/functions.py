from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from .models import EmailBucket
from django.urls import reverse

# builds a complete link to the ticket
def link_builder(ticket):
        return settings.BASE_URL + reverse('show_ticket', kwargs={'ticket_id': ticket.id})

# user: the user that edits
# ticket: the ticket that has been edited
def send_ticket_deadline_notification(ticket):
        subject = '"{0}" hat heute seine Deadline erreicht'.format(ticket.name)
        message = '"{0}" hat heute seine Deadline erreicht'.format(ticket.name) + "\n\n" + link_builder(ticket)
        send_email(ticket.assigned_user, subject, message, ticket=ticket)

# user: the user that edits
# ticket: the ticket that has been edited
def send_ticket_rejected_notification(user, ticket):
        subject = '"{0}" wurde abgelehnt'.format(ticket.name)
        message = '"{0}" wurde von {1} abgelehnt'.format(user.username, ticket.name) + "\n\n" + link_builder(ticket)

        send_email(ticket.dispatcher, subject, message, ticket=ticket)

# user: the user that commented
# notify_user: the user to be notified
# ticket: the commented ticket
def send_user_commented_ticket(user, notify_user, ticket):
        subject = '"{0}" wurde kommentiert'.format(ticket.name)
        message = '"{0}" wurde von {1} kommentiert'.format(user.username, ticket.name) + "\n\n" + link_builder(ticket)

        send_email(notify_user, subject, message, ticket=ticket)

# user: the user that edits
# ticket: the ticket that is edited
def send_ticket_edit_notification(user, ticket):
        subject = '"{0}" wurde bearbeitet'.format(ticket.name)
        message = '"{0}" wurde von {1} bearbeitet'.format(user.username, ticket.name) + "\n\n" + link_builder(ticket)

        send_email(ticket.assigned_user, subject, message, ticket=ticket)

# user: the user that assigns
# ticket: the ticket that is assigned
def send_assigned_notification(user, ticket):
        subject = "Dir wurde ein Ticket zugewiesen"
        message = 'Dir wurde das Ticket "{0}" von {1} zugewiesen'.format(ticket.name, user.username) + "\n\n" + link_builder(ticket)

        send_email(ticket.assigned_user, subject, message, ticket=ticket)

def send_new_group_ticket(user, ticket):
    subject = "Neues Ticket {0} in der Gruppe {1}".format(ticket.name, ticket.assigned_group.name)
    message = 'Ein neues Ticket "{0}" wurde von {1} in der Gruppe {2} angelegt'.format(ticket.name, user.username, ticket.assigned_group.name) + '\n\n' + link_builder(ticket)

    send_email(ticket.assigned_user, subject, message, ticket=ticket)
    

# sends an email, eather directly or save it as an EmailBucket to send later
def send_email(user, subject, message, frm=settings.DEFAULT_FROM_EMAIL, pdf=None, ticket=None):
        if user:
            if user.sending_email_once_a_day:
                    email = EmailBucket()
                    email.send_to = user
                    email.subject = subject
                    email.message = message
                    email.save()
            else:
                    send_email_now([user.email], subject, message, frm=settings.DEFAULT_FROM_EMAIL, pdf=None)

        if ticket and ticket.assigned_group and ticket.assigned_group.groupemail:
        # send mail to group
            groupemail = ticket.assigned_group.groupemail.email
            if groupemail != None:
                    send_email_now([groupemail], subject, message, frm=settings.DEFAULT_FROM_EMAIL, pdf=None)

# send the email now
def send_email_now(to, subject, message, frm=settings.DEFAULT_FROM_EMAIL, pdf=None):
        subject = settings.EMAIL_TAG+" "+subject
        msg = EmailMultiAlternatives(subject, message, frm, to)
        if pdf:
                msg.attach_file(pdf)
        msg.send()
