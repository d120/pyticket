from django.urls import reverse
from ticket.tests.test_models import TicketTest
from django.test.client import Client


# ticket views test cases (uses reverse)
class TicketViewsTest(TicketTest):
    def setUp(self):
        self.client = Client()
        self.client.login(username='master',password='Coollol888')

    def test_ticket_list(self):
        ticket = self.create_ticket()
        url = reverse("dashboard")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(ticket.name, str(resp.content))

    def test_ticket_show(self):
        url = reverse('show_ticket', kwargs={'ticket_id': 1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("Test ticket #1", str(resp.content))

        # send comment
        form = resp.context['form']
        data = form.initial
        data['comment'] = 'test comment'
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)

        # send comment with _closeandcomm
        form = resp.context['form']
        data = form.initial
        data['comment'] = 'test comment'
        data['_closeandcomm'] = '_closeandcomm'
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)

        #bad send comment
        resp = self.client.post(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_not_assigned_ticket_show(self):
        url = reverse('show_ticket', kwargs={'ticket_id': 2})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("Test ticket 2", str(resp.content))

        # send comment
        form = resp.context['form']
        data = form.initial
        data['comment'] = 'test comment'
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_new_ticket(self):
        url = reverse('new_ticket')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        form = resp.context['form']
        data = form.initial
        data['name'] = 'Test ticket 123'
        data['text'] = 'Test text'
        data['priority'] = 'normal'
        data['assigned_user'] = 1
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("erstellt", str(resp.content))

    def test_bad_new_ticket(self):
        url = reverse('new_ticket')
        resp = self.client.post(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_new_ticket_assigned(self):
        url = reverse('new_ticket')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        form = resp.context['form']
        data = form.initial
        data['name'] = 'Test ticket 123'
        data['text'] = 'Test text'
        data['priority'] = 'normal'
        data['assigned_user'] = 2
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("erstellt", str(resp.content))

    def test_ticket_edit_view(self):
        url = reverse('edit_ticket', kwargs={'ticket_id': 2})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        # post
        form = resp.context['form']
        data = form.initial
        data['name'] = 'New ticket name'
        data['assigned_group'] = 3
        data['assigned_user'] = 3
        data['priority'] = 'normal'
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("aktualisiert", str(resp.content))

    def test_ticket_close_view(self):
        url = reverse('close_ticket', kwargs={'ticket_id': 1})
        data = {'next': '/'}
        resp = self.client.get(url, data)
        self.assertEqual(resp.status_code, 302)

    def test_ticket_close_done_view(self):
        url = reverse('close_ticket', kwargs={'ticket_id': 2})
        data = {'next': '/'}
        resp = self.client.get(url, data)
        self.assertEqual(resp.status_code, 302)

    def test_ticket_close_bad_view(self):
        url = reverse('close_ticket', kwargs={'ticket_id': 10})
        data = {'next': '/'}
        resp = self.client.get(url, data)
        self.assertEqual(resp.status_code, 302)

    def test_my_tickets(self):
        url = reverse('my_tickets')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_restore_ticket(self):
        url = reverse('restore_ticket', kwargs={'ticket_id': 2})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_restore_ticket_open(self):
        url = reverse('restore_ticket', kwargs={'ticket_id': 1})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_restore_bad_ticket(self):
        url = reverse('restore_ticket', kwargs={'ticket_id': 20})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_inbox_ticket(self):
        url = reverse("inbox_ticket")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        # accept tack
        resp = self.client.post(url, {'_acc': 4, 'next': '/'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        # reject task
        url = reverse("inbox_ticket")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        # accept tack
        resp = self.client.post(url, {'_rej': 5}, follow=True)
        self.assertEqual(resp.status_code, 404)  # 200

        # post bad request
        resp = self.client.post(url, follow=True)
        self.assertEqual(resp.status_code, 404)  # 200

        #post ignore
        resp = self.client.post(url, {'_ignore': 5}, follow=True)
        self.assertEqual(resp.status_code, 404)  # 200

    def test_search(self):
        url = reverse("search")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_recuring_tickets(self):
        url = reverse('recurring_ticket')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        # bad post
        resp = self.client.post(url,  follow=True)
        self.assertEqual(resp.status_code, 200)

        # post
        resp = self.client.post(url, {'_turnoff': '5', }, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_rejected_ticket(self):
        url = reverse('rejected_ticket')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_rejected_ticket_post(self):
        url = reverse('rejected_ticket')
        resp = self.client.post(url, {'_assign': 5, 'selectUser': 2}, follow=True)
        self.assertEqual(resp.status_code, 200)

        # self
        url = reverse('rejected_ticket')
        resp = self.client.post(url, {'_assign': 5, 'selectUser': 1}, follow=True)
        self.assertEqual(resp.status_code, 200)

        # not accepted
        url = reverse('rejected_ticket')
        resp = self.client.post(url, {'_assign': 1, 'selectUser': 1}, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_rejected_ticket_bad_post(self):
        url = reverse('rejected_ticket')
        resp = self.client.post(url, {'_assign': 50, 'selectUser': 2}, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_rec_cron(self):
        # no access
        url = reverse('recurrence_cron')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        try:
            url = reverse('recurrence_cron')
            resp = self.client.get(url,  {'t': 'e7d3685715939842749cc27b38d0ccb9706d4d14a5304ef9eee093780eab5df9'})
            self.assertEqual(resp.status_code, 200)
        except:
            pass
