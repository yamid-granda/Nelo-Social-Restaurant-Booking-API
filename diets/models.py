from base.models import BaseModel
from django.db import models


class Diet(BaseModel):
    name = models.TextField(
        unique=True,
        max_length=200,
    )
