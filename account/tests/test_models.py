from django.test import TestCase
from account.models import MyUser

#account models test cases
class MyUserTest(TestCase):
    fixtures = ['fixtures/accounts.json']

    #create test user
    def create_my_user(self, username='test_user', email='mail@test.com', password='Testing123'):
        return MyUser.objects.create_user(username, email, password)

    def test_my_user_creation(self):
        user = self.create_my_user()
        self.assertTrue(isinstance(user, MyUser))

    #create test user with mail settings
    def test_my_user_edition(self):
        user = MyUser.objects.get(username='test_user2')
        self.assertFalse(user.sending_email_once_a_day)
        user.sending_email_once_a_day = True
        user.save()

    #delete user
    def test_my_user_delete(self):
        self.assertTrue(MyUser.objects.filter(username='test_user2').exists())
        user = MyUser.objects.get(username='test_user2').delete()
        self.assertFalse(MyUser.objects.filter(username='test_user2').exists())