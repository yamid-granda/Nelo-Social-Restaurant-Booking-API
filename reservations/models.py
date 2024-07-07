from base.models import BaseModel
from django.db import models
from tables.models import Table
from django.core.validators import MaxValueValidator, MinValueValidator
from tables.configs import TABLE_MIN_CAPACITY, TABLE_MAX_CAPACITY, TABLE_CHOICES


class Reservation(BaseModel):
    table_id = models.ForeignKey(
        Table, on_delete=models.PROTECT, related_name="reservations"
    )
    datetime = models.DateTimeField()
    made_out_to = models.TextField(max_length=200)
    quantity = models.IntegerField(
        default=TABLE_MIN_CAPACITY,
        choices=TABLE_CHOICES,
        validators=[
            MinValueValidator(TABLE_MIN_CAPACITY),
            MaxValueValidator(TABLE_MAX_CAPACITY),
        ],
    )

    def __str__(self):
        return self.datetime
