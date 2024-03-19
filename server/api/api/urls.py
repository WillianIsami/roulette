from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("bets/", include("roulette_api.urls")),
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]