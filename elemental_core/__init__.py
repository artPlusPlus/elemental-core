from ._no_value import NoValue, NO_VALUE
from ._elemental_error import ElementalError
from ._elemental_base import ElementalBase
from ._hook import Hook
from ._hook_data import HookDataBase
from ._hook_data import ValueChangedHookData
from ._forward_reference import ForwardReference
from . import util


__title__ = "elemental-core"
__summary__ = "Functionality shared across Elemental CMS."
__url__ = "https://github.com/artPlusPlus/elemental-core"

__version__ = "0.3.0.dev0"

__author__ = "Matt Robinson"
__email__ = "matt@technicalartisan.com"

__license__ = "Mozilla Public License 2.0 (MPL 2.0)"
__copyright__ = "Copyright 2016 Matt Robinson"

__all__ = (
    "__title__",
    "__summary__",
    "__url__",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
    "ElementalError",
    "ElementalBase",
    "Hook",
    "HookDataBase",
    "ValueChangedHookData",
    "util",
    "NO_VALUE",
)
