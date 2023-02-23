from django.contrib import admin
from .models import AccountTier, Account, Image

admin.site.register(Account)
admin.site.register(AccountTier)
admin.site.register(Image)
