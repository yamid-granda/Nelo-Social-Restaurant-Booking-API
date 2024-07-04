from rest_framework import viewsets
from .serializers import RestaurantDietSerializer
from .models import RestaurantDiet

class RestaurantDietView(viewsets.ModelViewSet):
  serializer_class = RestaurantDietSerializer
  queryset = RestaurantDiet.objects.all()