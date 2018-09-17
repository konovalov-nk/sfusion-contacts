from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from contacts.models import User


class UserEmail(models.Model):
    email = models.EmailField(max_length=100, blank=False, unique=True)
    user = models.ForeignKey(User, related_name='emails', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def clean_fields(self, exclude=None):
        user_email_exists = UserEmail.objects.filter(email=self.email).exclude(id=self.id).exists()
        if user_email_exists:
            raise ValidationError({'email': 'Email already exists.'})
        super().clean_fields(exclude=exclude)

    def get_absolute_url(self):
        return "/users/%i/emails/%i" % self.user_id, self.id
