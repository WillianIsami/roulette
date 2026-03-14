from django.urls import path

from .views import (
    BetApiView,
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    IsAuthenticatedView,
    LogoutView,
    SpinRouletteView,
    TransactionListView,
    UserCreateView,
    WalletDepositView,
    WalletView,
)

urlpatterns = [
    path('api/', BetApiView.as_view(), name='bet_api'),
    path('api/create/', UserCreateView.as_view(), name='user_create'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/is-authenticated/', IsAuthenticatedView.as_view(), name='is_authenticated'),
    path('api/token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('api/wallet/', WalletView.as_view(), name='wallet'),
    path('api/wallet/deposit/', WalletDepositView.as_view(), name='wallet_deposit'),
    path('api/transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('api/spin/', SpinRouletteView.as_view(), name='spin_roulette'),
]
