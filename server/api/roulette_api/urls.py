from django.urls import path
from .views import BetListApiView, BetDetailApiView

urlpatterns = [
    path("api", BetListApiView.as_view()),
    path("api/<int:bet_id>/", BetDetailApiView.as_view()),
]