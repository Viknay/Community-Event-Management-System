from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('create_event/', views.create_event, name='create_event'),
    path('get_event/', views.get_event, name='get_event'),
    path('get_event/<int:id>/', views.get_event, name='get_event_by_id'),
    path('update_event/<int:id>/', views.update_event, name='update_event'),
    path('delete_event/<int:id>/', views.delete_event, name='delete_event'),
    path('get_category/', views.get_category, name='get_category'),
    path('rsvp/<int:event_id>/', views.rsvp, name ='rsvp'), 


]
