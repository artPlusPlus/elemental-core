from elemental_core import ForwardReference

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
    raise KeyError()


class _ResolverCls(object):
    def __init__(self):
        self._key = _method_key
        self._keyed_thing = _keyed_method_thing
        self._un_keyed_thing = _un_keyed_method_thing

    def keyed_method_resolver(self, key):
        if key == self._key:
            return self._keyed_thing
        raise KeyError()

    def un_keyed_method_resolver(self):
        return self._un_keyed_thing


class HasForwardReferences(object):
    no_key_test = ForwardReference()

    @ForwardReference
    def key_func_test(self):
        return _function_key

    @ForwardReference
    def key_method_test(self):
        return _method_key


def test_function_resolver_with_no_key():
    has_fwd_refs = HasForwardReferences()

    has_fwd_refs.no_key_test.resolver = _un_keyed_function_resolver

    assert has_fwd_refs.no_key_test == _un_keyed_function_thing

    del has_fwd_refs

    assert len(HasForwardReferences.no_key_test._bound_fwd_refs) == 0


def test_function_resolver_with_key():
    has_fwd_refs = HasForwardReferences()

    has_fwd_refs.key_func_test.resolver = _keyed_function_resolver

    assert has_fwd_refs.key_func_test == _keyed_function_thing

    del has_fwd_refs

    assert len(HasForwardReferences.key_func_test._bound_fwd_refs) == 0


def test_method_resolver_with_no_key():
    resolver_inst = _ResolverCls()
    has_fwd_refs = HasForwardReferences()

    has_fwd_refs.no_key_test.resolver = resolver_inst.un_keyed_method_resolver

    assert has_fwd_refs.no_key_test == _un_keyed_method_thing

    del has_fwd_refs

    assert len(HasForwardReferences.no_key_test._bound_fwd_refs) == 0


def test_get_key_from_method_and_resolve_reference():
    resolver_inst = _ResolverCls()
    has_fwd_refs = HasForwardReferences()

    has_fwd_refs.key_method_test.resolver = resolver_inst.keyed_method_resolver

    assert has_fwd_refs.key_method_test == _keyed_method_thing

    del has_fwd_refs

    assert len(HasForwardReferences.key_method_test._bound_fwd_refs) == 0
