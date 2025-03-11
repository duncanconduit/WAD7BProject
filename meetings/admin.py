from django.contrib import admin
from meetings.models import Meeting, Place, Invitation

admin.site.register(Meeting)
admin.site.register(Place)
admin.site.register(Invitation)
