from django.contrib import admin

# Register your models here.
from .models import Offer, Topic, Message

admin.site.register(Offer)
admin.site.register(Topic)
admin.site.register(Message)

