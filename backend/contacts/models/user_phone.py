from django.db import models
from django.utils import timezone
from contacts.models import User
from phonenumber_field.modelfields import PhoneNumberField


class UserPhone(models.Model):
    phone = PhoneNumberField(blank=False, unique=True)
    user = models.ForeignKey(User, related_name='phones', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return "/users/%i/phones/%i" % self.user_id, self.id
