from django.test import TestCase
from account.models import MyUser
from django.contrib.auth.models import Group
from ticket.models import Ticket, Comment

#ticket models test cases
class TicketTest(TestCase):

    #install fixtures
    fixtures = ['fixtures/ticket.json', 'fixtures/auth_groups.json', 'fixtures/accounts.json']

    @staticmethod

    #create test ticket
    def create_ticket():
        group = Group.objects.get(id=1)
        user1 = MyUser.objects.get(id=1)
        user2 = MyUser.objects.get(id=2)

        ticket = Ticket.objects.create(
            name='Test ticket',
            assigned_user=user1,
            assigned_group=group,
            text='test ticket text',
            creator_user=user2
        )
        return ticket

    def test_ticket_creation(self):
        ticket = self.create_ticket()
        self.assertTrue(isinstance(ticket, Ticket))
        self.assertEqual(ticket.__str__(), 'Test ticket')

    #tests ticket edition, delete, create comment
    def test_ticket_edition(self):
        ticket = Ticket.objects.get(pk=1)
        self.assertEqual(ticket.state, "open")
        ticket.state = 'done'
        ticket.save()

    def test_ticket_delete(self):
        self.assertTrue(Ticket.objects.filter(pk=1).exists())
        Ticket.objects.get(pk=1).delete()
        self.assertFalse(Ticket.objects.filter(pk=1).exists())

    def create_comment(self):
        ticket = Ticket.objects.get(id=1)
        user = MyUser.objects.get(id=1)

        comment = Comment.objects.create(
            ticket=ticket,
            user=user,
            comment='test comment',
        )

        return comment

    def test_comment_creation(self):
        comment = self.create_comment()
        self.assertTrue(isinstance(comment, Comment))
        self.assertEqual(comment.__str__(), 'test comment')

    #comment edition and save
    def test_comment_edition(self):
        comment = Comment.objects.get(pk=1)
        self.assertEqual(comment.comment, "Test comment 1")
        comment.comment = "New test comment"
        comment.save()

    #comment delete
    def test_comment_delete(self):
        self.assertTrue(Comment.objects.filter(pk=1).exists())
        Comment.objects.get(pk=1).delete()
        self.assertFalse(Comment.objects.filter(pk=1).exists())

    def test_markdown(self):
        ticket = Ticket.objects.get(id=1)
        ticket.get_markdown
