from datetime import timedelta


from django.db import models
from django.utils.timezone import now


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User')

    access_token = models.CharField(max_length=128)
    access_token_expires = models.DateTimeField(null=True, blank=True)
    access_token_scope = models.CharField(max_length=255)
    access_token_refresh_token = models.CharField(max_length=255)

    def set_access_token(access_token,
                         scope,
                         expires_in,
                         refresh_token):
        self.access_token = access_token
        self.access_token_expires = now() + timedelta(seconds=expires_in)
        self.access_token_scope = scope
        self.access_token_refresh_token = refresh_token
