from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Dish(models.Model):
    name = models.CharField(max_length=300)
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return str(self.pk) + ": " + self.name

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def get_username(self):
        return self.user.username
    
    def get_password(self):
        return self.user.password
    
    def __str__(self): 
        return f"{self.pk}: {self.user.username}"