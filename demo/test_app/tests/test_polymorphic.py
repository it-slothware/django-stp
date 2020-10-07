from django.apps import apps, AppConfig

from django.test import TestCase

from .. import DeviceType
from ..models import Device, Button, Display, Speaker


class PolymorphismTest(TestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.dev_1 = Device.objects.create(type=DeviceType.BUTTON)
        self.dev_2 = Device.objects.create(type=DeviceType.DISPLAY)
        self.dev_3 = Device.objects.create(type=DeviceType.SPEAKER)

    # def test_something(self):
    #     conf = list(apps.get_app_configs())[-1]
    #     self.assertEqual(conf.models, '')

    # def test_model_list(self):
    #     self.assertEqual(apps.get_models(), [])

    # def test_meta(self):
    #     self.assertEqual(list(Button.objects.all()), [])
    #
    # def test_parent(self):
    #     x = [
    #         Device._meta.polymorphic_identities,
    #     ]
    #     self.assertEqual(x, [])
    #
    # def test_devices(self):
    #     self.assertEqual(Device.objects.all(), [])
    #     dev_1, dev_2, dev_3 = Device.objects.all()
    #     self.assertTrue(isinstance(dev_1, Button))
    #     self.assertTrue(isinstance(dev_2, Display))
    #     self.assertTrue(isinstance(dev_3, Speaker))

    def test_creation(self):
        Device.objects.create(type=DeviceType.BUTTON)

        self.assertEqual(list(Device.objects.all()), [])
