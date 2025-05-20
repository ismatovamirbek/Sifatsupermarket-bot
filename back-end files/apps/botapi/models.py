from django.db import models
from shared.models import BaseModel


class Chanel(BaseModel):
    chanel_name = models.CharField(max_length=100)
    chanel_username = models.CharField(max_length=100)
    chanel_id = models.CharField(max_length=100)

    def __str__(self):
        return self.chanel_name
