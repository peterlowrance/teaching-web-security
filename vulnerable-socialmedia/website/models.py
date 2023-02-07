from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    session = models.CharField(max_length=255)
    balance = models.IntegerField(default=10000)
    bio = models.CharField(max_length=1000, default='Hi!  This is my bio.')
    friends = models.ManyToManyField("User", blank=True)
    has_xss_flag_1 = models.BooleanField(default=False)
    email = models.CharField(max_length=255, default="my_email@email.com")