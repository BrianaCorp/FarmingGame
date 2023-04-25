from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Item(models.Model):
    def __str__(self):
        return self.item_name

    item_name = models.CharField(max_length=200)
    item_type = models.CharField(max_length=100, default='Seeds')
    plant_type = models.CharField(max_length=100, default='Turnip')
    item_cost = models.IntegerField()
    item_image = models.ImageField(upload_to='images/items', default='/images/items/none.jpg')


class InventoryItem(models.Model):
    def __str__(self):
        return self.item.item_name

    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=1)
    item_quantity = models.IntegerField()


class Points(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    points_total = models.IntegerField(default=500)


class Plot(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    plot_plant = models.CharField(max_length=200, default="None")
    plot_growth = models.IntegerField(default=0)
    plot_watered = models.BooleanField(default=False)
    plot_image = models.ImageField(upload_to='images/plots', default='/images/plots/dirt.png')
    water_time = models.DateTimeField(default=timezone.now)
    growth_time = models.DateTimeField(default=timezone.now)
