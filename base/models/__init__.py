from django.db import models
from uuid import uuid4

class BaseModel(models.Model):
  id = models.UUIDField(
    primary_key=True,
    unique=True,
    default=uuid4,
    editable=False,
  )
  created_at = models.DateTimeField(auto_now_add = True)

  class Meta:
    abstract = True

  def __str__(self):
    return self.name
