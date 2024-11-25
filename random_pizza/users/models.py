from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from pizza.models import IsActiveManager


class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True, db_index=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    update_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = IsActiveManager()


class Address(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='user', blank=True, null=True)
    street = models.CharField(max_length=100)
    house_number = models.IntegerField()
    entrance = models.CharField(blank=True, null=True, max_length=10)
    room_number = models.IntegerField(blank=True, null=True)


class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.RESTRICT, related_name='user_by_cart')