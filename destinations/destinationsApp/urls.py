from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('users/new/', views.new_user, name='new_user'),
    path('sessions/new/', views.new_session, name='new_session'),
    path('users/', views.users, name='users'),
    path('sessions/', views.sessions, name='sessions'),
    path('sessions/destroy/', views.destroy_session, name='destroy_session'),
    path('destinations/', views.destinations, name='destinations'),
    path('destinations/new/', views.new_destination, name='new_destination'),
    path('destinations/<int:id>/', views.edit_dest, name='edit_dest'),
    path('destinations/<int:id>/destroy/', views.destroy_dest, name='destroy_dest'),
]
