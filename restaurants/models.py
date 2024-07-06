from base.models import BaseModel
from django.db import models


class Restaurant(BaseModel):
    name = models.TextField(
        unique=True,
        max_length=200,
    )
