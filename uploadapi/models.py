from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import Adjust



def upload_to(instance, filename):
    return f'images/{filename}'  


class AccountTier(models.Model):
    name = models.CharField(max_length=50)
    thumbnail_sizes = models.JSONField(default=list)
    has_image_link = models.BooleanField()
    has_expiring_links = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        managed=False
        db_table = 'images\".\"accounttier'

class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_account')
    account_tier = models.ForeignKey(AccountTier, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        managed=False
        db_table = 'images\".\"account'


class Image(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=32, null=True, blank=True)
    image = models.ImageField(upload_to=upload_to)
    binary = ImageSpecField(source='image', format='JPEG', options={'quality': 90}, processors=[Adjust(color=0)])


    class Meta:
        managed=False
        db_table = 'images\".\"image'