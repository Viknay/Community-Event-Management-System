from django.contrib import admin
from .models import User, Event, Category  , RSVP

# Register the User model
admin.site.register(User)

# Register the Event model
@admin.register(Event)  
class EventAdmin( admin.ModelAdmin):
    list_display = ('id','title', 'date', 'time', 'location','category', 'organizer')  
    readonly_fields = ('rsvp_limit', 'rsvp_count')
    list_filter = ('location','category','date')  # filter model using location, category or date
    search_fields = ('title',)  # search any specific event using event name
    ordering = ['date'] # Newly added  events will show above all events
    sortable_by = ( 'date', 'time') # can sort model based on date and time

# Register the Category model
admin.site.register(Category)

# If you want to register the RSVP model, you can uncomment this part:
admin.site.register(RSVP)
