from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, CreateEventForm, AgendaForm
from .models import Event, Agenda
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import agenda_already_set


@login_required(login_url='login')
@agenda_already_set
def home(request):
    if request.method == "POST":
        agendaform = AgendaForm(request.POST)

        if agendaform.is_valid():
            agenda = Agenda()
            agenda.name = agendaform.cleaned_data['agenda_name']
            agenda.owner = request.user
            agenda.save()

            messages.success(request, "Agenda Successfully setup!")
            return redirect("/events")
    else:
        agendaform = AgendaForm()

    context = {
        "agendaform": agendaform
    }

    return render(request, "agenda/agenda_name.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect('/events')
    else:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data['username']
                messages.success(
                    request, "Account Successfully Created for " + user)
                return redirect("/login")

        else:
            form = RegisterForm()

    context = {"form": form}

    return render(request, "agenda/register.html", context)


@login_required(login_url='login')
def events(request):
    agendas = Agenda.objects.all().values('id', 'owner', 'name')
    agendas = list(agendas)
    
    global agenda_id, agenda_name
    
    for agenda in agendas:
        if agenda['owner'] == request.user.id:
            print("Current owner", agenda['owner'])
            agenda_id = agenda['id']
            agenda_name = agenda['name']
            print("Event agenda id: ", agenda)
                
    if request.method == 'POST':
        eventform = CreateEventForm(request.POST)

        if eventform.is_valid():
            
            event = Event.objects.create(
                title=eventform.cleaned_data["title"],
                description=eventform.cleaned_data["description"],
                start_date=eventform.cleaned_data["start_date"],
                end_date=eventform.cleaned_data["end_date"],
                start_time=eventform.cleaned_data["start_time"],
                end_time=eventform.cleaned_data["end_time"],
                agenda=Agenda.objects.get(id=agenda_id)
            )

            messages.info(request, 'Event Successfully Added')            
            
            eventform = Agenda.objects.get(id=agenda_id)
            print("Event form:", eventform)
            eventform.save()
            
            events = Event.objects.filter(agenda_id=agenda_id).order_by("-created")
            print("Events: ", events)
            
            return redirect("/events")

    else:
        eventform = CreateEventForm()
        events = Event.objects.filter(agenda_id=agenda_id).order_by("-created")
        print("Events: ", events)

    context = {
        "eventform": eventform,
        "events": events,
        "agenda_name": agenda_name

    }
    
    return render(request, "agenda/events.html", context)


def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)
    global events
    
    agenda = Agenda.objects.get(owner=request.user)
    
    if request.method == 'POST':
        eventform = CreateEventForm(request.POST, instance=event)
        
        if eventform.is_valid():
            eventform.save()
            return redirect("/events")
        
        events = Event.objects.filter(agenda_id=agenda.id).order_by("-created")
        
        messages.success(request, "Event Successfully Updated!")
    else:
        eventform = CreateEventForm(instance=event)  
        
        events = Event.objects.filter(agenda_id=agenda.id).order_by("-created")
        
    context = {
        "event": event,
        "events": events,
        "eventform": eventform,
        "agenda_name": agenda.name
    }
    
    return render(request, "agenda/events.html", context)

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    agenda = Agenda.objects.get(owner=request.user)
        
    if event.delete():
        return redirect("/events")
    
    events = Event.objects.filter(agenda_id=agenda.id).order_by("-created")
    
    context = {
        "events": events,
        "agenda_name": agenda.name
    }
    
    return render(request, "agenda/events.html", context)


