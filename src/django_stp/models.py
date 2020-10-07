from django.db import models
from django.db.models.base import ModelBase

from .query import PolymorphicQuerySet


class PolymorphicMeta(ModelBase):

    def __new__(cls, name, bases, attrs, **kwargs):
        attr_meta = attrs.get('Meta', None)
        proxy = getattr(attr_meta, 'proxy', False)

        new_class = super().__new__(cls, name, bases, attrs, **kwargs)

        if proxy:
            for parent in new_class._meta.parents:
                if issubclass(parent, PolymorphicBase):
                    break
            else:
                parent = None

            if parent:
                polymorphic_identities = getattr(parent._meta, 'polymorphic_identities', [])
                polymorphic_identities.append(new_class)
                parent._meta.polymorphic_identities = polymorphic_identities
                new_class._meta.polymorphic_identities = polymorphic_identities
            elif new_class._meta.parents:
                raise RuntimeError('Polymorphic meta used on a not PolymorphicBase based model.')
        else:
            new_class._meta.polymorphic_identities = [new_class]

        return new_class


class PolymorphicBase(models.Model, metaclass=PolymorphicMeta):

    objects = PolymorphicQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._meta.proxy or not getattr(self, self._polymorphic_on, None):
            setattr(self, self._polymorphic_on, self._polymorphic_identity)

        super().save(*args, **kwargs)
