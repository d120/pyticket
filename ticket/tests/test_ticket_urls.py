from django.urls import reverse, resolve
from django.test import TestCase

#Ticket URLs test cases
class TestUrls(TestCase):

    def test_dashboard_url(self):
        path = reverse('dashboard')
        assert resolve(path).view_name == 'dashboard'

    def test_new_ticket_url(self):
        path = reverse('new_ticket')
        assert resolve(path).view_name == 'new_ticket'

    def test_show_ticket_url(self):
        path = reverse('show_ticket', kwargs={'ticket_id': 1})
        assert resolve(path).view_name == 'show_ticket'

    def test_inbox_ticket_url(self):
        path = reverse('inbox_ticket')
        assert resolve(path).view_name == 'inbox_ticket'

    def test_edit_ticket_url(self):
        path = reverse('edit_ticket', kwargs={'ticket_id': 1})
        assert resolve(path).view_name == 'edit_ticket'

    def test_restore_ticket_url(self):
        path = reverse('restore_ticket', kwargs={'ticket_id': 1})
        assert resolve(path).view_name == 'restore_ticket'

    def test_close_ticket_url(self):
        path = reverse('close_ticket', kwargs={'ticket_id': 1})
        assert resolve(path).view_name == 'close_ticket'

    def test_search_url(self):
        path = reverse('search')
        assert resolve(path).view_name == 'search'

    def test_my_ticket_url(self):
        path = reverse('my_tickets')
        assert resolve(path).view_name == 'my_tickets'

    def test_recurring_ticket_url(self):
        path = reverse('recurring_ticket')
        assert resolve(path).view_name == 'recurring_ticket'

    def test_recurrence_cron_ticket_url(self):
        path = reverse('recurrence_cron')
        assert resolve(path).view_name == 'recurrence_cron'

    def test_rejected_ticket_url(self):
        path = reverse('rejected_ticket')
        assert resolve(path).view_name == 'rejected_ticket'



