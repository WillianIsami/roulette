from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import BetListApiView, BetDetailApiView, UserCreateView

urlpatterns = [
    path("api", BetListApiView.as_view()),
    path("api/<int:bet_id>/", BetDetailApiView.as_view()),
    path('api/create/', UserCreateView.as_view(), name='user-create'),
    path("api-token-auth/", obtain_auth_token, name='api_token_auth'),
]
