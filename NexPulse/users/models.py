from datetime import datetime

from django.db import models


class UserDetails(models.Model):
    first_name = models.CharField(max_length=50, default='', blank=True, null=True)
    last_name = models.CharField(max_length=50, default='',blank=True, null=True)
    username = models.CharField(max_length=50, default='', blank=True, null=True)
    city = models.CharField(max_length=50, default='', blank=True, null=True)
    country = models.CharField(max_length=50, default='', blank=True, null=True)
    email_id = models.EmailField()
    password = models.CharField(max_length=20)
    totalFollowers = models.IntegerField(default=0)

    def __str__(self):
        return "<"+self.username+" "+self.email_id+">"


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    isScam = models.BooleanField(default=False)
    createdAt = models.DateField(default=datetime.today())
    totalLikes = models.IntegerField(default=0)
    spamReported = models.IntegerField(default=0)

    def __str__(self):
        return f'Post by {self.user.email_id}: {self.content[:20]}: {self.isScam}'

    class Meta:
        ordering = ['-id']  # Orders posts by id in descending order (newest first)


class Communities(models.Model):
    communityName = models.CharField(max_length=50)
    communityHead = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    totalMembers = models.IntegerField(default=1)

    def __init__(self):
        return "<community: "+self.communityName+" "+self.totalMembers+" members>"


class Friends(models.Model):
    userFollower = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name="follower")
    userFollowed = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name="followed")
    followingSince = models.DateField(default=datetime.now())


class LikedPosts(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class SavedPosts(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)