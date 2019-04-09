from django.test import TestCase
from notification.models import EmailBucket
from account.models import MyUser

#notification models test cases
class EmailBucketTest(TestCase):
    fixtures = ['fixtures/notification.json', 'fixtures/accounts.json']

    #create test email
    def create_email(self, subject='test_subject', message='test_message',user_id=1):
        user = MyUser.objects.get(id=user_id)
        return EmailBucket.objects.create(subject=subject, message=message, send_to=user)

    def test_email_creation(self):
        email = self.create_email()
        self.assertTrue(isinstance(email, EmailBucket))

    #email edition
    def test_email_edition(self):
        email = EmailBucket.objects.get(pk=1)
        self.assertEqual(email.subject, "Test mail subj")
        email.subject = "Changed subject"
        email.save()

    #delete email
    def test_email_delete(self):
        self.assertTrue(EmailBucket.objects.filter(pk=1).exists())
        EmailBucket.objects.get(pk=1).delete()
        self.assertFalse(EmailBucket.objects.filter(pk=1).exists())
