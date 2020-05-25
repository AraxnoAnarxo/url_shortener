import uuid
import base64


from django.db import models
from django.core.validators import URLValidator

HOST_NAME = 'http://127.0.0.1:8000/'


# Create your models here.
class UrlManager(models.Manager):
    def get_queryset(self):
        all_objects = super().get_queryset()
        return all_objects

class Url(models.Model):
    url = models.CharField(max_length=256, validators=[URLValidator()])
    url_hash = models.CharField(max_length=10, unique=True, db_index=True)
    short_url = models.CharField(max_length=256, validators=[URLValidator()], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    links = UrlManager()

    def save(self, *args, **kwargs):
        self.url_hash = self.generate_hash()
        self.short_url = self.create_short_url()
        super(Url, self).save(*args, **kwargs)

    def generate_hash(self):
        hash = base64.urlsafe_b64encode(uuid.uuid1().bytes)[:6]
        hash_exist = Url.links.filter(url_hash=hash)
        while hash_exist:
            hash = base64.urlsafe_b64decode(uuid.uuid1().bytes)[:6]
            hash_exist = Url.links.filter(url_hash=hash)
            continue
        hash = hash.decode('utf-8')
        return hash

    def create_short_url(self):
        return f'{HOST_NAME}{self.url_hash}'










