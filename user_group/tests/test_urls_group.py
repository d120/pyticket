from django.urls import reverse, resolve
from django.test import TestCase

#User_group URLs test cases
class TestUrls(TestCase):

    def test_group_url(self):
       path = reverse('dashboard_group', kwargs={'group_id':1})
       assert resolve(path).view_name == 'dashboard_group'

    def test_new_group_url(self):
        path = reverse('new_group')
        assert resolve(path).view_name == 'new_group'

    def test_edit_group_url(self):
        path = reverse('edit_group', kwargs={'group_id':1})
        assert resolve(path).view_name == 'edit_group'

    def test_group_delete_url(self):
        path = reverse('delete_group', kwargs={'group_id':1})
        assert resolve(path).view_name == 'delete_group'
