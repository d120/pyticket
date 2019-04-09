from django.test import TestCase
from django.urls import reverse
from django.test.client import Client

#user_group test cases
class MyUserGroupViewsTest(TestCase):
    fixtures = ['fixtures/accounts.json', 'fixtures/auth_groups.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='master',password='Coollol888')

    def test_groups_view(self, username='test_user', email='mail@test.com', password='Testing123'):
        url = reverse('dashboard_group', kwargs={'group_id':1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('TestGroup1', str(resp.content))

    #create test group
    def test_new_group_view(self):
        url = reverse('new_group')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        form = resp.context['form']
        data = form.initial
        data['name'] = 'Test group 143'
        data['members'] = 1
        data['admins'] = 1
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Test group 143', str(resp.content))

    #edit group
    def test_edit_group_view(self):
        url = reverse('edit_group', kwargs={'group_id': 1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        form = resp.context['form']
        data = form.initial
        data['name'] = 'Test group 777'
        data['members'] = 1
        data['admins'] = 1

        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Test group 777', str(resp.content))

    #delete group
    def test_delete_group_view(self):
        url = reverse('delete_group', kwargs={'group_id': 1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(url, {}, follow=True)
        self.assertEqual(resp.status_code, 200)
