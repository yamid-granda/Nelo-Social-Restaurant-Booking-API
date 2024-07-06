from rest_framework import viewsets
from .serializers import DietSerializer
from .models import Diet


class DietView(viewsets.ModelViewSet):
    serializer_class = DietSerializer
    queryset = Diet.objects.all()
