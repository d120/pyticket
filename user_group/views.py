from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib import messages
from ticket.models import Ticket
from .forms import AddGroupForm
from django.utils.translation import ugettext_lazy as _
from django.utils.text import Truncator


class RemoveUserGroupView(LoginRequiredMixin, View):
    """ Backend to remove a user from a group template in delete_group.html """
    template_delete_group = 'group/delete_group.html'

    def get(self, *args, **kwargs):
        # get the given group
        group = Group.objects.get(id=self.kwargs['group_id'])

        content = {
            "group": group,
        }
        return render(self.request, self.template_delete_group, content)

    def post(self, *args, **kwargs):
        group = Group.objects.get(id=self.kwargs['group_id'])
        user = self.request.user
        # if user is member of given group
        if user in group.user_set.all():
            # remove user from user_set
            group.user_set.remove(user)
            messages.success(self.request,
                         _('Sie sind nicht länger Mitglied der Gruppe {0}!'.format(get_group_name(group))))
        else:
            messages.error(self.request,_('Sie sind kein Mitglied der Gruppe {0}'.format(get_group_name(group))))
        return HttpResponseRedirect(reverse("dashboard"))


class EditGroupView(LoginRequiredMixin, View):
    """ Backend to edit an existing group template in edit_group.html """
    template_edit_group = 'group/edit_group.html'

    def get(self, *args, **kwargs):
        group = Group.objects.get(id=self.kwargs["group_id"])
        # get all users who are currently members of the group
        members = group.user_set.all()
        form = AddGroupForm(instance=group, initial={'members': members})

        content = {
            "group": group,
            "form": form,
        }
        return render(self.request, self.template_edit_group, content)

    def post(self, *args, **kwargs):
        # get given group
        group = Group.objects.get(id=self.kwargs["group_id"])

        form = AddGroupForm(self.request.POST, instance=group)

        if (form.is_valid()):
            try:
                form.save()
                # set the given users(passed as parameter members) as members of the group
                group.user_set.set(form.cleaned_data["members"])
                group.save()
                messages.success(self.request,
                             _('Gruppe {0} wurde erfolgreich editiert!'.format(get_group_name(group))))
                return HttpResponseRedirect(reverse("dashboard"))
            except Exception as e:
                pass

        content = {
            "group": group,
            "form": form,
        }
        messages.error(self.request, _('Änderungen an der Gruppe konnten nicht übernommen werden!'))
        return render(self.request, self.template_edit_group, content)


class NewGroupView(LoginRequiredMixin, View):
    """ Backend to create a new group template in new_group.html """
    template_new_group = "group/new_group.html"

    def get(self, *args, **kwargs):
        form = AddGroupForm(initial={'members': {self.request.user}})

        content = {
            "form": form,
        }
        return render(self.request, self.template_new_group, content)

    def post(self, *args, **kwargs):
        form = AddGroupForm(self.request.POST)
        if form.is_valid():
            group = form.save()
            try:
                # get all desired members for the group
                members = form.cleaned_data["members"]
                # iterate over members list
                for member in members:
                    # adding each member in members to user_set
                    group.user_set.add(member)
                group.save()
                messages.success(self.request,
                             _('Gruppe {0} wurde erfolgreich erstellt!'.format(get_group_name(group))))
                return HttpResponseRedirect(reverse('dashboard'))
            except Exception as e:
                group.delete()
        content = {
            "form": form,
        }
        messages.error(self.request, _('Gruppe konnte nicht erstellt werden!'))
        return render(self.request, self.template_new_group, content)


class DashboardGroupView(LoginRequiredMixin, View):
    """ Backend to monitor a group template in group.html """
    template_group = 'group/group.html'

    def get(self, *args, **kwargs):
        # get all tickets which belongs to given group
        tickets = Ticket.objects.filter(assigned_group=self.kwargs["group_id"])
        # get the given group as Group object
        group = Group.objects.get(id=self.kwargs["group_id"])
        user = self.request.user
        # get all groups in which the user is member of
        groups = user.groups.all()

        content = {
            "tickets": tickets,
            "group": group,
            "groups": groups
        }
        return render(self.request, self.template_group, content)

    def post(self, *args, **kwargs):
        pass


def get_group_name(group):
    """
    param: group - a Group object
    return: returns the truncated name of the given group as String
    """
    return Truncator(group.name).chars(20)
