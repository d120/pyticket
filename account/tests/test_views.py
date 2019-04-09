from django.test import TestCase
from account.models import MyUser
from django.urls import reverse

#account views test cases
class MyUserViewsTest(TestCase):
    fixtures = ['fixtures/accounts.json']

    #login view test
    def test_login_view(self, username='test_user', email='mail@test.com', password='Testing123'):
        url = reverse('login')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        form = resp.context['form']
        data = form.initial
        data['username'] = 'test_user2'
        data['password'] = 'Coolpass123'

        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)

        # settings test
        url = reverse('settings')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        form = resp.context['form']
        data = form.initial
        data['sending_email_once_a_day'] = 'on'
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)

    #logout view test
    def test_logout_view(self):
        url = reverse('logout')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
