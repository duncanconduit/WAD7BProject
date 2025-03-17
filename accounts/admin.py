from django.contrib import admin
from accounts.models import User, Organisation

admin.site.register(User)
admin.site.register(Organisation)
