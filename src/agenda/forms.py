from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Agenda, Event
import datetime

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2"]


class AgendaForm(forms.Form):
    agenda_name = forms.CharField(label="Your Agenda Name", max_length=120)

    class Meta:
        model = Agenda
        fields = ["agenda_name"]


class CreateEventForm(forms.ModelForm):
    title = forms.CharField(label="Title", max_length=255)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': '5'}), label="Description")
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), initial=datetime.date.today, label="Start Date")
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), label="End Date")
    start_time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}), initial=datetime.time, label="Start Time")
    end_time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}), label="End Time")
    
    class Meta:
        model = Event
        fields = ["title", "description", "start_date", "end_date", "start_time", "end_time"]
    