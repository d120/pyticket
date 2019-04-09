from django.db import models

from django.contrib.auth import get_user_model


# Storage for emails from users who only want to have a summary once a day
class EmailBucket(models.Model):
    send_to = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject + " " + self.send_to.email

