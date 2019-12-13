from django.db import models
from django.contrib.auth.models import Group

class GroupEmail(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
