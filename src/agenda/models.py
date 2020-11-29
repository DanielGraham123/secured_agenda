from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid

class Agenda(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)

    def __str__(self):
        return str(self.name + ' - ' + self.owner.username)


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(blank=True, null=True, default='')
    end_date = models.DateField(blank=True, null=True, default='')
    start_time = models.TimeField(blank=True, null=True, default=timezone.now())
    end_time = models.TimeField(blank=True, null=True, default='')

    class Meta:
        ordering = ["-created"]  # ordering by the created date

    def __str__(self):
        return self.title
