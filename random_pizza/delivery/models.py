from django.contrib.auth import get_user_model
from django.db import models
from pizza.models import IsActiveManager, Pizza
from users.models import Address, Cart


class Courier(models.Model):

    class Transport(models.IntegerChoices):
        WALK = 1, 'Пешком'
        SCOOTER = 2, 'Самокат'
        CAR = 3, 'Автомобиль'

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    transport = models.IntegerField(choices=Transport.choices, default=Transport.WALK)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = IsActiveManager()


class Order(models.Model):

    class Status(models.IntegerChoices):
        CANCELLED = 0, 'Отменен'
        IN_PROCESSING = 1, 'В обработке'
        IN_THE_KITCHEN = 2, 'Повара готовят'
        ON_THE_ROAD = 3, 'В пути к вам'
        DONE = 4, 'Заказ доставлен'

    class PaymentStatus(models.IntegerChoices):
        PAID = 1, 'Заказ оплачен'
        IS_NOT_PAID = 2, 'Не оплачен'

    class PaymentType(models.IntegerChoices):
        ON_SITE = 1, 'Картой на сайте'
        CASH_ON_DELIVERY = 2, 'Оплата при получении'

    user = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT, related_name='orders')
    courier = models.ForeignKey(Courier, on_delete=models.RESTRICT, related_name='deliveries')
    address = models.ForeignKey(Address, on_delete=models.RESTRICT, related_name='address_orders')
    status = models.IntegerField(choices=Status.choices, default=Status.IN_PROCESSING)
    payment_status = models.IntegerField(choices=PaymentStatus.choices, default=PaymentStatus.IS_NOT_PAID)
    payment_type = models.IntegerField(choices=PaymentType.choices, default=PaymentType.CASH_ON_DELIVERY)
    note = models.TextField(blank=True, null=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING, related_name='items', null=True, blank=True)
    pizza = models.ManyToManyField(Pizza, on_delete=models.DO_NOTHING, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name='items', null=True, blank=True)