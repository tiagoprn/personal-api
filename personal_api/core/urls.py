from django.urls import path

from core.views import GreetingsView

urlpatterns = [path('greetings/', GreetingsView.as_view(), name='greetings')]
