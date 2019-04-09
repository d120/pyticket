from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    # adding field for determining if user wishes only a summary mail per day
    sending_email_once_a_day = models.BooleanField(default=False)
