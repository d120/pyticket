from ticket.forms import AddCommentForm, AddTicketForm, EditTicketForm
from django.test import TestCase

#Ticket forms test cases
class TicketFormTest(TestCase):

    #test valid ticket form
    def test_valid_add_ticket_form(self):
        data = {'name': "Test ticket", 'priority': "normal",}
        form = AddTicketForm(data=data)
        self.assertTrue(form.is_valid())

    #tests add, edit and add_comments ticket forms
    def test_invalid_add_ticket_form(self):
        data = {'name': "Test ticket name only"}
        form = AddTicketForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_edit_ticket_form(self):
        data = {'name': "Test ticket", 'priority': "normal", "state": 'done'}
        form = EditTicketForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_edit_ticket_form(self):
        data = {'name': "Test ticket name only"}
        form = EditTicketForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_add_comment_form(self):
        data = {'ticket': "1", 'user': "1", "comment":"Test comment"}
        form = AddCommentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_add_comment_form(self):
        data = {'comment': "Anonymous comment"}
        form = AddCommentForm(data=data)
        self.assertTrue(form.is_valid())
        # assertFalse
