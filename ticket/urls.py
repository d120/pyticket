from django.urls import path
from .views import ShowTicketView, NewTicketView, PendingTicketView, EditTicketView, RestoreTicketView, CloseTicketView, DashboardView, MyTicketsView, RecurringTicketView, rec_cron, RejectedTicketView, SearchTicketView


urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('new/', NewTicketView.as_view(), name="new_ticket"),
	path('ticket/<int:ticket_id>', ShowTicketView.as_view(), name="show_ticket"),
    path('inbox/', PendingTicketView.as_view(), name="inbox_ticket"),
    path('ticket/edit/<int:ticket_id>', EditTicketView.as_view(), name="edit_ticket"),
    path('ticket/restore/<int:ticket_id>', RestoreTicketView.as_view(), name="restore_ticket"),
    path('ticket/close/<int:ticket_id>', CloseTicketView.as_view(), name="close_ticket"),
    path('search/', SearchTicketView.as_view(), name="search"),
    path('my/', MyTicketsView.as_view(), name="my_tickets"),
    path('recurring/', RecurringTicketView.as_view(), name="recurring_ticket"),
    path('recurring/cron', rec_cron,  name='recurrence_cron'),
    path('rejected_ticket/', RejectedTicketView.as_view(), name="rejected_ticket"),

]
