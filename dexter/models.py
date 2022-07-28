from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Invention(models.Model):
    name  = models.CharField(max_length= 100)
    img  = models.ImageField(upload_to= 'pics')
    desc  = models.TextField()


class UserInvention(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.IntegerField()
