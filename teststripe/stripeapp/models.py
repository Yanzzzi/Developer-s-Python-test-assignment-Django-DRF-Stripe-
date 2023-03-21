from django.db import models
from django.urls import reverse


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.FloatField()

    def get_abs_url(self):
        return reverse('item', kwargs={'item_id': self.pk})