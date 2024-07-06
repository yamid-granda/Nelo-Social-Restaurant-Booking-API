from django.urls import path, include
from rest_framework import routers
from .views import ReservationView

router = routers.DefaultRouter()
router.register(r"reservations", ReservationView, "reservations")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
