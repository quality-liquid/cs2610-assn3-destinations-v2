from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    email = models.TextField(unique=True)
    password_hash = models.TextField()


class Session(models.Model):
    id = models.BigAutoField(primary_key=True)
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.TextField()


class Destination(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    review = models.TextField()
    rating = models.IntegerField()
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    share_publicly = models.BooleanField()