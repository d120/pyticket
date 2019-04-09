from django.urls import reverse, resolve
from django.test import TestCase

#account URLs test cases
class TestUrls(TestCase):

    def test_login_url(self):
       path = reverse('login')
       assert resolve(path).view_name == 'login'

    def test_logout_url(self):
        path = reverse('logout')
        assert resolve(path).view_name == 'logout'

    def test_settings_url(self):
        path = reverse('settings')
        assert resolve(path).view_name == 'settings'

