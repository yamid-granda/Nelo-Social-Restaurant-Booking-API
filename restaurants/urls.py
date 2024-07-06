from django.urls import path, include
from rest_framework import routers
from .views import RestaurantView

router = routers.DefaultRouter()
router.register(r"restaurants", RestaurantView, "restaurants")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
