from django.urls import path, include
from rest_framework import routers
from .views import TableView

router = routers.DefaultRouter()
router.register(r"tables", TableView, "tables")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
