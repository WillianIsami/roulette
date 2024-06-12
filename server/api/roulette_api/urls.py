from django.urls import path
from .views import BetApiView, UserCreateView, SpinRouletteView, LogoutView, IsAuthenticatedView,CookieTokenObtainPairView, CookieTokenRefreshView

urlpatterns = [
    path('api/', BetApiView.as_view(), name='bet_api'),
    path('api/create/', UserCreateView.as_view(), name='user_create'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/is-authenticated/', IsAuthenticatedView.as_view(), name='is_authenticated'),
    path('api/token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('api/spin/', SpinRouletteView.as_view(), name='spin_roulette'),
]
