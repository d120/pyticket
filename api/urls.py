from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('tickets/', views.TicketList.as_view()),
    path('tickets/<int:pk>/', views.TicketDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('groups/', views.GroupList.as_view()),
    path('groups/<int:pk>/', views.GroupDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
