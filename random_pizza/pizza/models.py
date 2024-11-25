from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class IsActiveManager(models.Manager):
    def get_query_set(self):
        return super().get_query_set().filter(is_active=True)


class Pizza(models.Model):

    class Size(models.IntegerChoices):
        SMALL = 20, 'Маленькая'
        MIDDLE = 30, 'Средняя'
        BIG = 35, 'Большая'

    name = models.CharField(max_length=100, verbose_name='Название')
    photo = models.ImageField(blank=True, null=True, upload_to='pizza')
    size = models.IntegerField(choices=Size.choices, default=Size.SMALL, verbose_name='Размер')
    weight = models.IntegerField(null=True, blank=True, default=400)
    price = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='tags')
    description = models.TextField(null=True, blank=True)
    ingredients = models.ManyToManyField('Ingredient', blank=True, related_name='ingredients')

    objects = models.Manager()
    active = IsActiveManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('pizza', kwargs={'pizza_id': self.pk})


class Tag(models.Model):
    tag = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_id': self.pk})


class Ingredient(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    price = models.IntegerField()