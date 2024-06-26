from django.db import models


class UserDetails(models.Model):
    email_id = models.EmailField()
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.email_id


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()

    def __str__(self):
        return f'Post by {self.user.email_id}: {self.content[:20]}'

    class Meta:
        ordering = ['-id']  # Orders posts by id in descending order (newest first)