from rest_framework import viewsets
from .serializers.default_serializer import TableSerializer
from .models import Table


class TableView(viewsets.ModelViewSet):
    serializer_class = TableSerializer
    queryset = Table.objects.all()
