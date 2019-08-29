from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

app_name = 'api'

urlpatterns = [
    path('tickets/', views.TicketList.as_view(), name='all_tickets'),
    path('tickets/<int:pk>/', views.TicketDetail.as_view(), name='specific_ticket'),
    path('users/', views.UserList.as_view(), name='all_users'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='specific_user'),
    path('groups/', views.GroupList.as_view(), name='all_groups'),
    path('groups/<int:pk>/', views.GroupDetail.as_view(), name='specific_group'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
