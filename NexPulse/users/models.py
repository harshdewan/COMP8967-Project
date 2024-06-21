from django.db import models


class UserDetails(models.Model):
    email_id = models.EmailField()
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.email_id
