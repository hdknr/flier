from django.db import models
from django.contrib.auth.models import User


class Channel(models.Model):
    pass


class PointNode(models.Model):
    channel = models.ForeignKey(Channel)
    parent = models.ForeignKey(
        'PointNode',
        blank=True, null=True, default=None,  on_delete=models.SET_NULL)
    shops = models.ManyToManyField(
        'Shop',
        blank=True, null=True, default=None,)


class Shop(models.Model):
    channel = models.ForeignKey(Channel)


class ChannelAttribute(models.Models):
    channel = models.ForeignKey(Channel)
    name = models.CharField('Channel Attribute')


class ShopAttribute(models.Model):
    shop = models.ForeignKey(Shop)
    key = models.ForeignKey(ChannelAttribute)
    value = models.CharField('Attribute Value')


class Customer(models.Model):
    user = models.ForeignKey(
        User,
        blank=True, null=True, default=None,  on_delete=models.SET_NULL)


class Target(models.Model):
    channel = models.ForeignKey(Channel)
    customers = models.ManyToManyField(
        Customer,
        blank=True, null=True, default=None,)


class Promotion(models.Model):
    channel = models.ForeignKey(Channel)
    targets = models.ManyToManyField(
        Target,
        blank=True, null=True, default=None,)

    title = models.CharField('Title')
    message = models.TextField('Promotion Message')


class Flier(models.Model):
    promotion = models.ForeignKey(Promotion)
    customer = models.ForeignKey(Customer)

    message = models.TextField('Filer Message')
    error = models.TextField('Flier Error')
