from django.db import models
from django.contrib import auth
# Create your models here.
class User(auth.models.AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Admin'),
        (2, 'Teacher'),
        (3, 'Student'),
    )

    user_type = models.PositiveIntegerField(choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Administrator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
