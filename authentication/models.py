from django.db import models
from django.contrib import auth
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail, EmailMessage
import os


# Create your models here.
class User(auth.models.AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Admin'),
        (2, 'Teacher'),
        (3, 'Student'),
    )

    user_type = models.PositiveIntegerField(choices=USER_TYPE_CHOICES, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Administrator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# SIGNAL
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('api:password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        #title:
        "Password Reset for {title}".format(title="Some Website title"),
        #message:
        email_plaintext_message,
        #from:
        os.environ.get("EMAIL_USER"),
        #to:
        [reset_password_token.user.email],
        fail_silently=False,
    )
    # email = EmailMessage(
    #     "Password Reset for LMS",
    #     email_plaintext_message,
    #     to=[reset_password_token.user.email]
    # )
    # email.content_subtype = "html"
    # email.send()
