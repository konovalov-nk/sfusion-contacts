from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator


class User(models.Model):
    first_name = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])
    last_name = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])
    date_of_birth = models.DateField(default=timezone.now)
