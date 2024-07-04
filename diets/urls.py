from django.urls import path, include
from rest_framework import routers
from .views import DietView

router = routers.DefaultRouter()
router.register(r'diets', DietView, 'diets')

urlpatterns = [
  path('api/v1/', include(router.urls)),
]