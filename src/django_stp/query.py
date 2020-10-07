from django.db.models.query import ModelIterable, QuerySet
from django.db.models.query_utils import Q

Polymorphic_QuerySet_objects_per_request = 100


class PolymorphicIterable(ModelIterable):

    def __iter__(self):
        base_iter = super().__iter__()
        if self.queryset.polymorphic_disabled:
            return base_iter
        return self._polymorphic_iterator(base_iter)

    def _polymorphic_iterator(self, base_iter):
        """
        Here we do the same as::
            real_results = queryset._get_real_instances(list(base_iter))
            for o in real_results: yield o
        but it requests the objects in chunks from the database,
        with Polymorphic_QuerySet_objects_per_request per chunk
        """
        while True:
            base_result_objects = []
            reached_end = False

            # Make sure the base iterator is read in chunks instead of
            # reading it completely, in case our caller read only a few objects.
            for i in range(Polymorphic_QuerySet_objects_per_request):

                try:
                    o = next(base_iter)
                    base_result_objects.append(o)
                except StopIteration:
                    reached_end = True
                    break

            real_results = self.queryset._get_real_instances(base_result_objects)

            for o in real_results:
                yield o

            if reached_end:
                return


def transmogrify(cls, obj):
    """
    Upcast a class to a different type without asking questions.
    """
    if "__init__" not in obj.__dict__:
        # Just assign __class__ to a different value.
        new = obj
        new.__class__ = cls
    else:
        # Run constructor, reassign values
        new = cls()
        for k, v in obj.__dict__.items():
            new.__dict__[k] = v
    return new


class PolymorphicQuerySet(QuerySet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._iterable_class = PolymorphicIterable
        self.polymorphic_disabled = False

        if self.model and self.model._meta.proxy:
            identity_filter = {self.model._polymorphic_on: self.model._polymorphic_identity}
            self.query.add_q(Q(**identity_filter))

    def _get_real_instances(self, base_result_objects):
        resultlist = []

        polymorphic_identities = {pi._polymorphic_identity: pi for pi in self.model._meta.polymorphic_identities}

        for base_object in base_result_objects:
            identity = getattr(base_object, base_object._polymorphic_on)
            real_identity = polymorphic_identities[identity]

            if isinstance(base_object, real_identity):
                resultlist.append(base_object)
            else:
                real_object = transmogrify(real_identity, base_object)
                resultlist.append(real_object)

        return resultlist
