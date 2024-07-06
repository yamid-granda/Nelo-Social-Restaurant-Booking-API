from django.urls import path, include
from rest_framework import routers
from .views import RestaurantDietView

router = routers.DefaultRouter()
router.register(r"restaurants-diets", RestaurantDietView, "restaurants-diets")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
