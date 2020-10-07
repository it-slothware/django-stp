from django.db import models

from django_stp.models import PolymorphicBase

from . import DeviceType


class Device(PolymorphicBase):
    type = models.CharField(max_length=7, choices=DeviceType.CHOICES)

    _polymorphic_on = 'type'
    _polymorphic_identity = DeviceType.GENERIC


class Button(Device):
    _polymorphic_identity = DeviceType.BUTTON

    class Meta:
        proxy = True


class Display(Device):
    _polymorphic_identity = DeviceType.DISPLAY

    class Meta:
        proxy = True


class Speaker(Device):
    _polymorphic_identity = DeviceType.SPEAKER

    class Meta:
        proxy = True
