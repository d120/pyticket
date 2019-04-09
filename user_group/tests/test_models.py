from django.test import TestCase
from account.models import MyUser
from django.contrib.auth.models import Group as MyGroup

#user_group test cases
class UserGroupTest(TestCase):

    #install fixtures
    fixtures = ['fixtures/auth_groups.json', 'fixtures/accounts.json']

    @staticmethod

    #create, edit and delete test group
    def create_group():
        group = MyGroup.objects.create(name='test_group')
        user1 = MyUser.objects.get(id=1)
        user2 = MyUser.objects.get(id=2)
        group.user_set.add(user1)

        return group

    def test_group_creation(self):
        group = self.create_group()
        self.assertTrue(isinstance(group, MyGroup))
        self.assertEqual(group.__str__(), 'test_group')

    def test_group_edition(self):
        group = MyGroup.objects.get(pk=1)
        self.assertEqual(group.name, "TestGroup1")
        group.name = "Changed name"
        group.save()

    def test_group_delete(self):
        self.assertTrue(MyGroup.objects.filter(pk=1).exists())
        MyGroup.objects.get(pk=1).delete()
        self.assertFalse(MyGroup.objects.filter(pk=1).exists())
