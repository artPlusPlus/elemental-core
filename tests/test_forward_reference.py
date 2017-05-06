from elemental_core import (
    ForwardReference,
    NO_VALUE
)

_function_key = 'func_key'
_keyed_function_thing = 'keyed_func_thing'
_un_keyed_function_thing = 'un_keyed_func_thing'

_method_key = 'method_key'
_keyed_method_thing = 'keyed_method_thing'
_un_keyed_method_thing = 'un_keyed_method_thing'


def _un_keyed_function_resolver():
    return _un_keyed_function_thing


def _keyed_function_resolver(key):
    if key == _function_key:
        return _keyed_function_thing
    return NO_VALUE


class _ResolverCls(object):
    def __init__(self):
        self._key = _method_key
        self._keyed_thing = _keyed_method_thing
        self._un_keyed_thing = _un_keyed_method_thing

    def keyed_method_resolver(self, key):
        if key == self._key:
            return self._keyed_thing
        return NO_VALUE

    def un_keyed_method_resolver(self):
        return self._un_keyed_thing


class HasForwardReferences(object):
    no_key_test = ForwardReference()

    @no_key_test.populated
    def no_key_test(self, value):
        self.no_key_test_populated = value

    @ForwardReference
    def key_func_test(self):
        return _function_key

    @key_func_test.populated
    def key_func_test(self, value):
        self.key_func_test_populated = value

    @ForwardReference
    def key_method_test(self):
        return _method_key

    @key_method_test.populated
    def key_method_test(self, value):
        self.key_method_test_populated = value

    def __init__(self):
        super(HasForwardReferences, self).__init__()

        self.no_key_test_populated = False
        self.key_func_test_populated = False
        self.key_method_test_populated = False


def test_function_resolver_with_no_key():
    HasForwardReferences.no_key_test.reference_resolver = _un_keyed_function_resolver

    has_fwd_refs = HasForwardReferences()
    has_fwd_refs.no_key_test = _un_keyed_function_resolver()

    assert has_fwd_refs.no_key_test() == _un_keyed_function_thing
    assert has_fwd_refs.no_key_test_populated == _un_keyed_function_thing

    del has_fwd_refs


def test_function_resolver_with_key():
    HasForwardReferences.key_func_test.reference_resolver = _keyed_function_resolver

    has_fwd_refs = HasForwardReferences()
    has_fwd_refs.key_func_test = _keyed_function_thing

    assert has_fwd_refs.key_func_test() == _keyed_function_thing
    assert has_fwd_refs.key_func_test_populated == _keyed_function_thing

    del has_fwd_refs


def test_method_resolver_with_no_key():
    resolver_inst = _ResolverCls()

    HasForwardReferences.no_key_test.reference_resolver = resolver_inst.un_keyed_method_resolver

    has_fwd_refs = HasForwardReferences()
    has_fwd_refs.no_key_test = _un_keyed_method_thing

    assert has_fwd_refs.no_key_test() == _un_keyed_method_thing
    assert has_fwd_refs.no_key_test_populated == _un_keyed_method_thing

    del has_fwd_refs


def test_get_key_from_method_and_resolve_reference():
    resolver_inst = _ResolverCls()

    HasForwardReferences.key_method_test.reference_resolver = resolver_inst.keyed_method_resolver

    has_fwd_refs = HasForwardReferences()
    has_fwd_refs.key_method_test = _keyed_method_thing

    assert has_fwd_refs.key_method_test() == _keyed_method_thing
    assert has_fwd_refs.key_method_test_populated == _keyed_method_thing

    del has_fwd_refs
