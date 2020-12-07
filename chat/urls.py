from django.urls import path

from chat.views import course_chat_room

app_name = 'chat'

urlpatterns = [
    path('room/<int:course_id>/', course_chat_room, name='course_chat_room'),
]