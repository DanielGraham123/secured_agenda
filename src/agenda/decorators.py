from django.shortcuts import redirect
from .models import Agenda

def agenda_already_set(view_func):
    def wrapper_func(request, *args, **kwargs):
        if Agenda.objects.filter(owner_id=request.user.id).exists():
            return redirect("/events")
        else:
            return view_func(request, *args, **kwargs)
            
    return wrapper_func