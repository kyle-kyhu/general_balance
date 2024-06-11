import hashlib
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.users.helpers import validate_profile_picture


def _get_avatar_filename(instance, filename):
    """Use random filename prevent overwriting existing files & to fix caching issues."""
    return f'profile-pictures/{uuid.uuid4()}.{filename.split(".")[-1]}'

class Company(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"


class CustomUser(AbstractUser):
    """
    Add additional fields to the user model here.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    avatar = models.FileField(upload_to=_get_avatar_filename, blank=True, validators=[validate_profile_picture])

    def __str__(self):
        return f"{self.get_full_name()} <{self.email or self.username}>"

    def get_display_name(self) -> str:
        if self.get_full_name().strip():
            return self.get_full_name()
        return self.email or self.username

    @property
    def avatar_url(self) -> str:
        if self.avatar:
            return self.avatar.url
        else:
            return "https://www.gravatar.com/avatar/{}?s=128&d=identicon".format(self.gravatar_id)

    @property
    def gravatar_id(self) -> str:
        # https://en.gravatar.com/site/implement/hash/
        return hashlib.md5(self.email.lower().strip().encode("utf-8")).hexdigest()
