from django.contrib import admin
from .models import Event, Agenda

admin.site.register(Agenda)
admin.site.register(Event)
