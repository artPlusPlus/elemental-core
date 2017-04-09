import logging
from typing import Callable
import weakref

from ._no_value import NO_VALUE

_LOG = logging.getLogger(__name__)


class BoundForwardReference(object):
    @property
    def resolver(self):
        return self._resolver

    @resolver.setter
    def resolver(self, value: Callable):
        try:
            self._resolver = weakref.WeakMethod(value)
        except TypeError:
            self._resolver = weakref.ref(value)

    def __init__(self, instance, resource_key_fget):
        super(BoundForwardReference, self).__init__()

        self._instance_ref = weakref.ref(instance)
        try:
            self._reference_key_getter_ref = weakref.ref(resource_key_fget)
        except TypeError:
            self._reference_key_getter_ref = resource_key_fget
        self._resolver = None

    def __call__(self, instance):
        if not instance:
            return self

        ref_key = NO_VALUE
        ref_key_getter = self._reference_key_getter_ref
        if ref_key_getter:
            if isinstance(ref_key_getter, weakref.ref):
                ref_key_getter = ref_key_getter()
                if not ref_key_getter:
                    msg = (
                        'Failed to resolve Reference: '
                        'Reference Key Getter is invalid.'
                    )
                    raise RuntimeError(msg)
            ref_key = ref_key_getter(instance)

        resolver = self._resolver
        if isinstance(resolver, weakref.ref):
            resolver = resolver()
        if not resolver:
            msg = 'Failed to resolve Resource: Resolver reference dead.'
            raise RuntimeError(msg)

        try:
            if ref_key is not NO_VALUE:
                result = resolver(ref_key)
            else:
                result = resolver()
        except Exception as e:
            if ref_key is not NO_VALUE:
                msg = 'Failed to resolve reference "{0}": {1} - {2}'
                msg = msg.format(ref_key, type(e).__name__, e)
            else:
                msg = 'Failed to resolve reference: {0} - {1}'
                msg = msg.format(type(e).__name__, e)
            _LOG.debug(msg)
        else:
            msg = 'Resolved Resource: "{0}"'
            msg = msg.format(repr(result))
            _LOG.debug(msg)

        return result


class ForwardReference(object):
    def __init__(self, resource_key_fget=None):
        super(ForwardReference, self).__init__()

        self._resource_key_fget = resource_key_fget
        self._bound_fwd_refs = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner=None):
        if not instance:
            return self

        try:
            result = self._bound_fwd_refs[instance]
        except KeyError:
            result = BoundForwardReference(instance, self._resource_key_fget)
            self._bound_fwd_refs[instance] = result
        else:
            result = result(instance)

        return result

    def __set__(self, instance, value):
        if self._bound_fwd_refs.get(instance) is value:
            return
        raise ValueError()
