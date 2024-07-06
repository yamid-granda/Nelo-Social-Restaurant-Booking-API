from base.models import BaseModel
from django.db import models
from restaurants.models import Restaurant
from diets.models import Diet


class RestaurantDiet(BaseModel):
    restaurant_id = models.ForeignKey(
        Restaurant,
        on_delete=models.PROTECT,
        # related_name='restaurants'
    )
    diet_id = models.ForeignKey(
        Diet,
        on_delete=models.PROTECT,
        # related_name='diets'
    )

    def __str__(self):
        return f"{self.restaurant_id} - {self.diet_id}"
