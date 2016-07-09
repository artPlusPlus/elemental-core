from ._elemental_error import ElementalError
from ._elemental_base import ElementalBase

from . import util


class _NoValue(object):
    def __bool__(self):
        # Python 3.x
        return False

    def __nonzero__(self):
        # Python 2.x
        return False


NO_VALUE = _NoValue()
