from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime, timedelta
import pytz
from django.contrib import messages
from .filters import TicketFilter
from django.contrib.auth import get_user_model
from .models import Ticket, Comment, TicketLog, Log
from notification.models import EmailBucket
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from .forms import AddTicketForm, AddCommentForm, EditTicketForm
from notification.functions import send_email, send_assigned_notification, \
    send_ticket_edit_notification, send_user_commented_ticket, send_ticket_rejected_notification, send_ticket_deadline_notification, send_email_now
import copy
from django.utils.text import Truncator
import bleach
from account.models import MyUser
from django.contrib.auth.models import Group

class NewTicketView(LoginRequiredMixin, View):
    """ Backend to create a new ticket template in new_ticket.html """
    template_new_ticket = "ticket/pages/new_ticket.html"

    def get(self, *args, **kwargs):
        form = AddTicketForm(initial={"assigned_user": self.request.user})

        content = {
            "form": form,
        }
        return render(self.request, self.template_new_ticket, content)

    def post(self, *args, **kwargs):
        form = AddTicketForm(self.request.POST)
        user = self.request.user
        # get recurrences from POST parameter recurrences
        recurrences = self.request.POST.get('recurrences', '')
        if form.is_valid():
            # ticket instance created by the form.save
            instance = form.save(commit=False)
            # set the creator of the ticket
            instance.creator_user = user
            # set the recurrences of the ticket manually
            instance.recurrences = recurrences
            # if Ticket is self-assigned
            if instance.assigned_user == self.request.user:
                instance.accepted = True
            # elseif assigned_user is not None but differs from request.user
            elif instance.assigned_user:
                # set the dispatcher to requested user
                instance.dispatcher = user
                instance.save()
                send_assigned_notification(user, instance)
            # save the changes made
            instance.save()

            ticket = form.instance

            messages.success(self.request,
                             _(get_ticket(ticket) + 'wurde erfolgreich erstellt'),
                             extra_tags='safe')
            # create a ticket log that the ticket has been created
            create_ticket_log(ticket, user, "add")
            # if everthing went well go to dashboard
            return HttpResponseRedirect(reverse('dashboard'))

        content = {
            "form": form,
            "recurrences": recurrences,
        }
        messages.error(self.request, _('Ticket konnte nicht erstellt werden'))
        return render(self.request, self.template_new_ticket, content)


class ShowTicketView(LoginRequiredMixin, View):
    """ Backend to show details of a ticket template in show_ticket.html """
    template_show_ticket = "ticket/pages/show_ticket.html"

    def get(self, *args, **kwargs):
        # get the given ticket object
        ticket = Ticket.objects.get(id=self.kwargs["ticket_id"])
        # retrieve all comments made for this ticket
        comments = Comment.objects.filter(ticket=ticket).order_by("created_at")
        form = AddCommentForm()
        # retrieve all Ticketlogs that are associated with given ticket
        history = TicketLog.objects.filter(ticket=ticket).order_by("-created_at")

        content = {
            "ticket": ticket,
            "form": form,
            "comments": comments,
            "history": history,
        }
        return render(self.request, self.template_show_ticket, content)

    def post(self, *args, **kwargs):
        # get the given ticket object
        ticket = Ticket.objects.get(id=self.kwargs["ticket_id"])
        # retrieve all comments made for this ticket
        comments = Comment.objects.filter(ticket=ticket).order_by("created_at")
        form = AddCommentForm(self.request.POST)

        if form.is_valid():
            # get the comment instance made by form.save
            instance = form.save(commit=False)
            user = self.request.user
            # set the ticket associated with the comment
            instance.ticket = ticket
            # set the user which made the comment
            instance.user = user
            # if button 'close and comment' submitted and current state is open
            if '_closeandcomm' in self.request.POST and ticket.state == 'open':
                # change state of ticket to done
                ticket.state = 'done'
                # change rejected state of ticket to False
                ticket.rejected = False
                # save changes made to ticket instance
                ticket.save()
            # save changes made to comment instance
            instance.save()
            if '_closeandcomm' in self.request.POST:
                messages.success(self.request, _(
                    'Ticket erfolgreich kommentiert und geschlossen.'))
            else:
                messages.success(self.request,
                                 _('Kommentar wurde erfolgreich hinzugefügt.'))

            # send it to the ticket owner and to everyboy who commented the ticket
            user_notification_list = []
            if ticket.assigned_user != user and ticket.assigned_user:
                user_notification_list.append(ticket.assigned_user)
            # iterate over retrieved comments
            for comment in comments:
                # if creator of comment differs from requested user
                if user != comment.user:
                    # append creator of comment to notification list
                    user_notification_list.append(comment.user)

            user_notification_list = list(
                dict.fromkeys(user_notification_list))
            # iterate over the user_notification_list
            for user_notification in user_notification_list:
                # send a notification to the user given in user_notification
                send_user_commented_ticket(user, user_notification, ticket)

            return HttpResponseRedirect(
                reverse('show_ticket', kwargs={'ticket_id': ticket.id}))

        content = {
            "ticket": ticket,
            "form": form,
            "comments": comments
        }
        messages.error(self.request, _('Kommentar konnte nicht erstellt werden'))
        return render(self.request, self.template_show_ticket, content)


class PendingTicketView(LoginRequiredMixin, View):
    """ Backend to show not accepted tickets template in inbox_ticket.html """
    template_pending_tickets = "ticket/pages/inbox_ticket.html"

    def get(self, *args, **kwargs):
        user = self.request.user
        # get all tickets which belongs to request user and are open and not accepted
        tickets = Ticket.objects.filter(accepted=False, assigned_user=user, state='open')
        # get all groups in which the user is member of
        my_groups = user.groups.all()
        # get all open, not accepted and unassigned tickets of my_groups which are not ignored
        group_tickets = Ticket.objects.filter(assigned_group__in=my_groups,
                                              assigned_user=None,
                                              accepted=False, state='open').exclude(
            ignored_by=user)
        content = {
            "tickets": tickets,
            "group_tickets": group_tickets
        }
        return render(self.request, self.template_pending_tickets, content)

    def post(self, *args, **kwargs):
        try:
            user = self.request.user
            # if button accepted is pressed
            if '_acc' in self.request.POST:
                # get the given ticket
                ticket = Ticket.objects.get(
                    id=int(self.request.POST.get('_acc')))
                # if ticket is not accpeted
                if not ticket.accepted:
                    # change assigned_user to requested user
                    ticket.assigned_user = user
                    # self-assignment includes an acceptance
                    ticket.accepted = True
                    ticket.time_assign_user = datetime.now()
                    ticket.rejected = False
                    # create a ticket log that ticket has been accepted
                    create_ticket_log(ticket, user, "accepted")
                    messages.success(self.request, _(get_ticket(
                        ticket) + 'erfolgreich akzeptiert'), extra_tags='safe')
                else:
                    messages.error(self.request, _(
                        'Ticket wurde bereits von einem Nutzer akzeptiert.'))
            # if button rejected is pressed
            if '_rej' in self.request.POST:
                # get the given ticket
                ticket = Ticket.objects.get(
                    id=int(self.request.POST.get('_rej')))
                # if requested user equals with assigned_user
                if ticket.assigned_user == user:
                    # set assigned_user of ticket to None
                    ticket.assigned_user = None
                    # set accepted state to false
                    ticket.accepted = False
                    ticket.rejected = True
                    # create a ticket log that the ticket has been rejected
                    create_ticket_log(ticket, user, "rejected")
                    send_ticket_rejected_notification(user, ticket)
                    messages.success(self.request, _(get_ticket(
                        ticket) + 'erfolgreich abgelehnt'), extra_tags='safe')
                # if current assigned_user is not the requested user
                else:
                    messages.error(self.request, _(
                        'Ticket ist bereits einem anderen Nutzer zugewiesen worden.'))
            # if button ignore is pressed
            if '_ignore' in self.request.POST:
                ticket = Ticket.objects.get(
                    id=int(self.request.POST.get('_ignore')))
                # if ticket is assigned to a group and user is member of that group
                if (
                        ticket.assigned_group and user in ticket.assigned_group.user_set.all() and not user in ticket.ignored_by.all()):
                    # add user to ignored_by list
                    ticket.ignored_by.add(user)
            # save changes made to ticket object
            ticket.save()

            # if next parameter is in the request.POST
            if 'next' in self.request.POST:
                return HttpResponseRedirect(self.request.POST.get("next"))

        except Exception as e:
            messages.error(self.request, _('Ticket existiert nicht.'))
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'),
                                    '/inbox/')


class EditTicketView(LoginRequiredMixin, View):
    """ Backend to edit a ticket template in edit_ticket.html """
    template_edit_ticket = "ticket/pages/edit_ticket.html"

    def get(self, *args, **kwargs):
        # get the given ticket
        ticket = Ticket.objects.get(id=self.kwargs["ticket_id"])
        form = EditTicketForm(instance=ticket)
        # retrieve recurrences from the ticket object
        recurrences = ticket.recurrences
        content = {
            "ticket": ticket,
            "form": form,
            "recurrences": recurrences,
        }
        return render(self.request, self.template_edit_ticket, content)

    def post(self, *args, **kwargs):
        user = self.request.user
        # get the given ticket
        ticket = Ticket.objects.get(id=self.kwargs["ticket_id"])
        # make a temp copy of the ticket
        old_ticket = copy.deepcopy(ticket)
        # get recurrences from request.POST parameter recurrences
        recurrences = self.request.POST.get('recurrences', ticket.recurrences)
        form = EditTicketForm(self.request.POST, instance=ticket)
        if form.is_valid():
            # if anything has changed
            if form.changed_data:
                message = ""
                i = 0
                changes = []
                # iterate over the parameters that have been changed
                for name in form.changed_data:
                    # create a log of the field containing value before and after editing
                    log = Log()
                    log.before = getattr(old_ticket, name)
                    log.after = getattr(ticket, name)
                    log.fieldname = Ticket._meta.get_field(name).verbose_name.title()
                    log.save()
                    # append the log to changes list
                    changes.append(log)


                # return HttpResponse(message)
                create_ticket_log(ticket, user, "changed", message, changes)
                # if requested user is not owner of the ticket
                if ticket.assigned_user != user and ticket.assigned_user:
                    send_ticket_edit_notification(user, ticket)
                # if assigned_user has been changed
                if 'assigned_user' in form.changed_data:
                    ticket.accepted = False
                    ticket.rejected = False
                    # if user self-assignment
                    if form.cleaned_data['assigned_user'] and \
                            form.cleaned_data['assigned_user'] == user:
                        ticket.accepted = True
                        ticket.rejected = False
                    # if assignment to another user
                    elif form.cleaned_data['assigned_user']:
                        send_assigned_notification(user, ticket)
                        ticket.time_assign_user = datetime.now()
                        ticket.rejected = False
                        ticket.accepted = False
                        ticket.dispatcher = user
                    # if assignment to None
                    else:
                        ticket.rejected = True
                        ticket.accepted = False
                # if assigned_group has been changed
                if 'assigned_group' in form.changed_data:
                    # clear ignored_by list
                    ticket.ignored_by.clear()
                    # if assigned_group has been changed to a specific group and ticket is rejected
                    if form.cleaned_data['assigned_group'] and ticket.rejected:
                        ticket.rejected = False

                if 'state' in form.changed_data:
                    if form.cleaned_data['state']  == 'done':
                        ticket.rejected = False

            ticket.recurrences = recurrences
            # save the changes made above
            form.save()
            messages.success(self.request,
                             _(get_ticket(ticket) + 'erfolgreich aktualisiert'),
                             extra_tags='safe')

            return HttpResponseRedirect(reverse('dashboard'))

        content = {
            "ticket": ticket,
            "form": form,
            "recurrences": recurrences,
        }
        messages.error(self.request,
                       _('Ticket ' + ticket.name + ' konnte nicht aktualisiert werden.'))
        return render(self.request, self.template_edit_ticket, content)


class SearchTicketView(LoginRequiredMixin, View):
    """ Backend to search for a ticket on template search_ticket.html """

    def get(self, *args, **kwargs):
        # get all Tickets
        ticket_list = Ticket.objects.all()
        # initialize the TicketFilter with given criterias from request.Get
        ticket_filter = TicketFilter(self.request.GET, queryset=ticket_list)
        return render(self.request, 'ticket/pages/search_ticket.html',
                      {'filter': ticket_filter})


class RestoreTicketView(LoginRequiredMixin, View):
    """ Backend to restore a ticket """

    def get(self, *args, **kwargs):
        try:
            ticket = Ticket.objects.get(id=self.kwargs["ticket_id"])
            # user can only restore ticket if it is done
            if ticket.state == 'done':
                ticket.state = 'open'
                ticket.rejected = False
                ticket.save()
                # create an undo html href for status message
                undo = " <a href='/ticket/close/{0}' title='Das Ticket schließen.'>Undo<i class='fas fa-undo'></i></a>".format(
                    ticket.id)
                messages.success(self.request, _(get_ticket(
                    ticket) + 'erfolgreich wiederhergestellt.') + undo,
                                 extra_tags='safe')
            else:
                messages.error(self.request, _(
                    'Das Ticket konnte nicht wiederhergestellt werden, da es nicht als erledigt markiert ist.'))
        except Exception as e:
            messages.error(self.request, _('Das Ticket existiert nicht.'))
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))


class CloseTicketView(LoginRequiredMixin, View):
    """ Backend to close a ticket """

    def get(self, *args, **kwargs):
        try:
            user = self.request.user
            ticket = Ticket.objects.get(id=self.kwargs["ticket_id"])
            # user can only close a ticket if it is open
            if ticket.state == 'open':
                ticket.state = 'done'
                ticket.rejected = False
                ticket.save()
                # create an undo html href for status message
                undo = " <a href='/ticket/restore/{0}' title='Das Ticket wiederherstellen.'>Undo<i class='fas fa-undo'></i></a>".format(
                    ticket.id)
                messages.success(self.request, _(get_ticket(
                    ticket) + 'erfolgreich geschlossen.') + undo, extra_tags='safe')
                create_ticket_log(ticket, user, "closed")
                # if next parameter in request
                if 'next' in self.request.GET:
                    return HttpResponseRedirect(self.request.GET.get("next"),'/')
            else:
                messages.error(self.request, _(
                    '%s konnte nicht geschlossen werden, da es bereits geschlossen ist.' % get_ticket(
                        ticket)), extra_tags='safe')
        except Exception as e:
            messages.error(self.request, _('Das Ticket existiert nicht.'))
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'), '/')


class DashboardView(LoginRequiredMixin, View):
    """ Backend for the dashboard view template in dashboard.html """
    template_settings = "ticket/pages/dashboard.html"

    def get(self, *args, **kwargs):
        now = datetime.utcnow()

        datetime_plus_one_day = datetime.now() + timedelta(days=1)
        day = datetime_plus_one_day.day
        month = datetime_plus_one_day.month
        year = datetime_plus_one_day.year

        user = self.request.user
        # get all open, accepted tickets which belong to user
        open_tickets = Ticket.objects.filter(assigned_user=user,
                                             accepted=True).exclude(
            state='done')
        #  get the number of open tickets
        open_tickets_count = Ticket.objects.filter(
            assigned_user=user, accepted=True).exclude(
            state='done').count()
        # get all groups in which the user is member
        groups = user.groups.all()

        dict = {}
        # iterate over the groups
        for group in groups:

            tickets = Ticket.objects.filter(assigned_group=group.id)
            openTickets = tickets.filter(state="open").count()
            doneTickets = tickets.count()

            if doneTickets == 0:
                dict[group.name] = 0
            elif doneTickets == doneTickets + openTickets:
                dict[group.name] = 100
            else:
                dict[group.name] = 100 - round(
                    100 * (openTickets / doneTickets))
        content = {
            "user": user,
            "myDate": now,
            "openTickets": open_tickets,
            "openTicketsCount": open_tickets_count,
            "groups": groups,
            "dict": dict,
            "day": day,
            "month": month,
            "year": year
        }

        return render(self.request, self.template_settings, content)

    def post(self, *args, **kwargs):
        pass


class MyTicketsView(LoginRequiredMixin, View):
    """ Backend to show all open tickets template in my_ticket.html """
    template_tickets = "ticket/pages/my_tickets.html"

    def get(self, *args, **kwargs):
        user = self.request.user
        # get all accepted, open tickets which belong to user
        tickets = Ticket.objects.filter(
            assigned_user=user, accepted=True).exclude(state='done')
        # get all groups in which user is member
        groups = user.groups.all()

        content = {
            "tickets": tickets,
            "groups": groups
        }
        return render(self.request, self.template_tickets, content)

    def post(self, *args, **kwargs):
        pass


class RecurringTicketView(LoginRequiredMixin, View):
    """ Backend to show recurring tickets template in recurring_ticket.html """
    template_tickets = "ticket/pages/recurring_ticket.html"

    def get(self, *args, **kwargs):
        # get all recurring tickets not considering relevance in terms of time
        tickets = Ticket.objects.exclude(recurrences__isnull=True).exclude(
            recurrences__exact='')
        content = {
            "tickets": tickets,
        }
        return render(self.request, self.template_tickets, content)

    def post(self, *args, **kwargs):
        """
        tries to remove the recurrences from the given ticket
        """
        try:
            ticket = Ticket.objects.get(
                id=int(self.request.POST.get('_turnoff')))
            if '_turnoff' in self.request.POST and ticket.recurrences:
                # remove recurrences from the given ticket
                ticket.recurrences = ''
                ticket.save()
                messages.success(self.request,
                    _('Die Wiederholungen von {0} erfolgreich ausgeschaltet'.format(
                    get_ticket(ticket))), extra_tags='safe')
        except Exception as e:
            messages.error(self.request, _('Ticket existiert nicht.'))
        return HttpResponseRedirect('/recurring/')


class RejectedTicketView(LoginRequiredMixin, View):
    """ Backend to show rejected tickets template in rejected_ticket.html """
    template_tickets = "ticket/pages/rejected_ticket.html"

    def get(self, *args, **kwargs):
        # user list
        users = []
        user = self.request.user
        # get all rejected tickets for which the user is creator or dispatcher
        rej_tickets = Ticket.objects.filter(
            Q(creator_user=user, assigned_user=None, rejected=True) | Q(
                dispatcher=user, assigned_user=None, rejected=True))
        if rej_tickets:
            # get all availabe users
            users = get_user_model().objects.all()
        content = {
            "tickets": rej_tickets,
            "users": users,
        }
        return render(self.request, self.template_tickets, content)

    def post(self, *args, **kwargs):
        try:
            ticket = Ticket.objects.get(
                id=int(self.request.POST.get('_assign')))
            # if assign button is pressed and ticket is not accepted
            if '_assign' in self.request.POST and not ticket.accepted:
                # retrieve the id of the selectedUser
                id = int(self.request.POST.get("selectUser"))
                # get the user object corresponding to the retrieved id
                usr = get_user_model().objects.get(id=id)
                # set the selectedUser as assigned_user
                ticket.assigned_user = usr
                ticket.rejected = False
                ticket.time_assign_user = datetime.now()
                # if self-assignment
                if usr == self.request.user:
                    ticket.accepted = True
                # if not self-assignment
                else:
                    ticket.dispatcher = self.request.user
                ticket.save()
                messages.success(self.request, _(get_ticket(
                    ticket) + 'wurde erfolgreich zugewiesen.'),
                                 extra_tags='safe')
            else:
                messages.error(self.request, _(
                    '%s wurde bereits von einem Nutzer akzeptiert.' % get_ticket(
                        ticket)), extra_tags='safe')
        except Exception as e:
            messages.error(self.request,
                           _('Ticket oder Nutzer existiert nicht.'))
        return HttpResponseRedirect('/rejected_ticket/')


def rec_cron(request):
    """
    cron job for sending summary mails to users, deadline notification
    and recurring tickets
    param: the request from user
    """
    if request.GET.get('t') != 'e7d3685715939842749cc27b38d0ccb9706d4d14a5304ef9eee093780eab5df9':
        return HttpResponse("No Access rights")
    # retrieve all recurring tickets
    tickets = Ticket.objects.exclude(recurrences__isnull=True).exclude(
        recurrences__exact='')
    # iterate over the recurring tickets
    for ticket in tickets:
        tz = pytz.timezone('Europe/Berlin')
        today = datetime.combine(datetime.now(), datetime.min.time())
        today = tz.localize(today)
        # get the next occurences of the ticket
        occ = ticket.recurrences.after(today, inc=True,
            dtstart=datetime(2010,1,1,0,0,0).replace(tzinfo=pytz.utc))
        # get the next day
        tomorrow = today + timedelta(days=1)
        # if next occurence is tomorrow
        if occ.date() == tomorrow.date():
            # create a new duplicate of the ticket
            dup = ticket
            dup.pk = None
            dup.id = None
            dup.state = 'open'
            dup.assigned_user = None
            dup.time_assign_user = None
            dup.accepted = False
            dup.created_at = datetime.now()
            dup.updated_at = datetime.now()
            dup.deadline = None
            dup.recurrences = ''
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


    return HttpResponse("Done.")

def create_ticket_log(ticket, user, state, message=None, changes=None):
    log = TicketLog()
    log.ticket = ticket
    log.user = user
    log.state = state
    if message:
        log.message = message
    if changes:
        log.save()
        for change in changes:
            log.changes.add(change)
    log.save()


def get_ticket(ticket):
    """
    is used for generating a part of status messages
    param: ticket - given ticket object
    return: String - href to the ticket
    """
    return 'Ticket <a href=''/ticket/%s>%s</a> ' % (str(ticket.id), Truncator(bleach.clean(ticket.name, [])).chars(32))
