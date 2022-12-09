from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('events/', all_events, name='event_list'),
    path('my_events/', my_events, name='my_events'),
    path('add_venue/', add_venue, name='add_venue'),
    path('add_event/', add_event, name='add_event'),
    path('list_venues/', list_venues, name='list_venues'),
    path('search_venues/', search_venues, name='search_venues'),
    path('search_events/', search_events, name='search_events'),
    path('show_venue/<venue_id>', show_venue, name='show_venue'),
    path('update_venue/<venue_id>', update_venue, name='update_venue'),
    path('update_event/<event_id>', update_event, name='update_event'),
    path('delete_event/<event_id>', delete_event, name='delete_event'),
    path('delete_venue/<venue_id>', delete_venue, name='delete_venue'),
    path('venue_text/', venue_text, name='venue_text'),
    path('venue_csv/', venue_csv, name='venue_csv'),
    path('venue_pdf/', venue_pdf, name='venue_pdf'),
    path('admin_approval/', admin_approval, name='admin_approval'),
    path('venue_events/<venue_id>', venue_events, name='venue_events'),
    path('show_event/<event_id>', show_event, name='show_event'),
]
