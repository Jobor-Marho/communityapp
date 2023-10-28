from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class AdminUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Indigene(models.Model):
    SEX = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    full_Name = models.CharField(max_length=264, unique=True)
    date_of_Birth = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=SEX)
    alive = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.full_Name}'s data"

    def get_absolute_url(self):
        return reverse("censusapp:all_indigene")


class Adult(models.Model):
    name = models.ForeignKey(Indigene, related_name='adults', on_delete=models.CASCADE)
    employment_status = models.BooleanField()

    def __str__(self):
        return f"{self.name.full_Name}'s data"


class Child(models.Model):
    name = models.ForeignKey(Indigene, related_name='children', on_delete=models.CASCADE)
    primary_education = models.BooleanField()


    def __str__(self):
        return f"{self.name.full_Name}'s data"
    

