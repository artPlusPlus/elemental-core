import logging
from typing import Any, Callable

from ._no_value import NO_VALUE
from .util import create_weak_ref, restore_weak_ref

_LOG = logging.getLogger(__name__)


class BoundForwardReference(object):
    @property
    def reference_key(self):
        if self._key_getter:
            result = self._key_getter(self._instance)
        else:
            result = NO_VALUE

        return result

    def __init__(self, instance, key_getter, populated_setter, reference_resolver):
        super(BoundForwardReference, self).__init__()

        self._instance = instance
        self._key_getter = key_getter
        self._populated_setter = populated_setter
        self._reference_resolver = reference_resolver

    def _resolve_reference(self):
        if self._key_getter:
            ref_key = self._key_getter(self._instance)
        else:
            ref_key = NO_VALUE

        try:
            if ref_key is NO_VALUE:
                result = self._reference_resolver()
            else:
                result = self._reference_resolver(ref_key)
        except Exception as e:
            if ref_key is NO_VALUE:
                msg = "Failed to resolve reference: {0} - {1}"
                msg = msg.format(type(e).__name__, e)
            else:
                msg = 'Failed to resolve reference "{0}": {1} - {2}'
                msg = msg.format(ref_key, type(e).__name__, e)
            _LOG.debug(msg)
        else:
            msg = 'Resolved Resource: "{0}"'
            msg = msg.format(repr(result))
            _LOG.debug(msg)

        return result

    def populate(self, reference_target: Any):
        return self._populated_setter(self._instance, reference_target)

    def __call__(self):
        return self._resolve_reference()


class ForwardReference(object):
    @property
    def reference_resolver(self) -> Callable:
        return restore_weak_ref(self._reference_resolver_ref)

    @reference_resolver.setter
    def reference_resolver(self, value: Callable):
        self._reference_resolver = create_weak_ref(value)

    def __init__(self, key_getter=None, populated_setter=None, reference_resolver=None):
        super(ForwardReference, self).__init__()

        self._key_getter = key_getter
        self._populated_setter = populated_setter
        self._reference_resolver = reference_resolver

    def key_getter(self, key_getter: Callable) -> "ForwardReference":
        return type(self)(
            key_getter=key_getter,
            populated_setter=self._populated_setter,
            reference_resolver=self._reference_resolver,
        )

    def populated(self, populated_setter: Callable) -> "ForwardReference":
        return type(self)(
            key_getter=self._key_getter,
            populated_setter=populated_setter,
            reference_resolver=self._reference_resolver,
        )

    def resolver(self, reference_resolver: Callable) -> "ForwardReference":
        return type(self)(
            key_getter=self._key_getter,
            populated_setter=self._populated_setter,
            reference_resolver=reference_resolver,
        )

    def __get__(self, instance, owner=None):
        if not instance:
            return self

        return self._create_bound_forward_reference(instance)

    def __set__(self, instance, value):
        if not instance:
            msg = "Cannot set ForwardReference."
            raise TypeError(msg)

        if not self._populated_setter:
            return

        self._create_bound_forward_reference(instance).populate(value)

    def _create_bound_forward_reference(self, instance):
        reference_resolver = restore_weak_ref(self._reference_resolver)

        result = BoundForwardReference(
            instance, self._key_getter, self._populated_setter, reference_resolver
        )

        return result
