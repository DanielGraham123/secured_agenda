from django.urls import path
from .views import home, register, events, delete_event, edit_event

app_name = "agenda"

urlpatterns = [
    path('', home, name='home_page'),
    path('events', events, name='events_page'),
    path('register', register, name='register_page'),
    path('events/delete/<int:event_id>', delete_event, name='delete_event'),
    path('events/edit/<int:event_id>', edit_event, name='edit_event'),
]
