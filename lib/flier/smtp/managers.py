''' Email Delivery Subsystem
'''
from django.db import models


class RelayQuerySet(models.QuerySet):
    pass


class MessageQuerySet(models.QuerySet):
    pass
