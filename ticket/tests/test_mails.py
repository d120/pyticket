from django.urls import reverse
from django.test.client import Client
from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from user_group.models import GroupEmail
from ticket.models import Ticket
from notification.functions import link_builder


class MailTest(TestCase):

    def setUp(self):
        self.group = Group.objects.create(name="mailtestgroup")
        self.group.save()
        group_mail = GroupEmail.objects.create(group=self.group, email="test@test.de")
        group_mail.save()
        u = get_user_model().objects.create_user(username="mailtestuser")
        u.groups.add(self.group)
        u.save()

        self.client = Client()
        self.client.force_login(u)

    def test_group_mail(self):
        url = reverse("new_ticket")
        resp = self.client.get(url)

        form = resp.context["form"]
        data = form.initial
        data["name"] = "Mail Ticket"
        data["text"] = "..."
        data["assigned_user"] = ""
        data["priority"] = "normal"
        data["assigned_group"] = self.group.id
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Ticket.objects.filter(name="Mail Ticket").exists())

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "[Ticketsystem] Neues Ticket Mail Ticket in der Gruppe mailtestgroup",
        )
        self.assertEqual(
            mail.outbox[0].body,
            'Ein neues Ticket "Mail Ticket" wurde von mailtestuser in der Gruppe mailtestgroup angelegt\n\n{}'.format(
                link_builder(Ticket.objects.get(name="Mail Ticket"))
            ),
        )
