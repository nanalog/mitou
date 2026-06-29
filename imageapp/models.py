from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class ImageData(models.Model):

    class Meta:
        db_table = 'image_data'

    title = models.CharField(
        max_length=100,
        default='',
    )

    image = models.ImageField(
        upload_to='images/'
    )

    prediction = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    probability = models.FloatField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
