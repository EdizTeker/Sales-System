from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

class Item(models.Model):
    
    name = models.CharField(max_length=150)
    price = models.PositiveIntegerField(default=10)
    stock = models.PositiveIntegerField()
    category = models.CharField(max_length=60)
    #image = models.ImageField(null=True, blank=True)


    def sale(self, minus):
        if Item.stock != 0:
            Item.stock = Item.stock - minus

    def __str__(self):
        return self.name  
    
    def get_absolute_url(self):
        return reverse('item:detail', kwargs={'id': self.id})
    

class Cart (models.Model):
    cartnumber = models.PositiveIntegerField()
    cartitem = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def item_name(self):
        if self.cartitem:
            return self.cartitem.name
        return 'yok'
    def get_absolute_url(self):
        return reverse('item:detail', kwargs={'id': 1})
    

    

    

    

    


    
    


                       