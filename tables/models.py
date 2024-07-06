from base.models import BaseModel
from django.db import models
from restaurants.models import Restaurant
from django.core.validators import MaxValueValidator, MinValueValidator
from .configs import TABLE_MAX_CAPACITY, TABLE_MIN_CAPACITY, TABLE_CHOICES


class Table(BaseModel):
    restaurant_id = models.ForeignKey(
        Restaurant,
        on_delete=models.PROTECT,
        # related_name='restaurants'
    )

    name = models.TextField(max_length=200)

    capacity = models.PositiveIntegerField(
        default=TABLE_MIN_CAPACITY,
        choices=TABLE_CHOICES,
        validators=[
            MinValueValidator(TABLE_MIN_CAPACITY),
            MaxValueValidator(TABLE_MAX_CAPACITY),
        ],
    )

    def __str__(self):
        return f"{self.name}, capacity: {self.capacity} people"
