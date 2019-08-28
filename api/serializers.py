from rest_framework import serializers
from ticket.models import Ticket, PRIORITY_CHOICES, STATE_CHOICES
from django.contrib.auth.models import Group
from account.models import MyUser

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'name', 'state', 'assigned_user', 'assigned_group', 'text', 'priority', 'deadline', 'recurrences']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'groups']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
