import uuid
import weakref
from typing import Sequence, List, Union, Optional, Callable, Set

from ._elemental_base import ElementalBase


def process_uuid_value(value: Union[str, uuid.UUID]) -> Optional[uuid.UUID]:
    """
    Processes a value into a UUID.

    Args:
        value (str or uuid): Data to process into a uuid.

    Returns:
        UUID if `value`, else None.

    Raises:
        ValueError: If `value` is not a UUID instance and cannot be converted
            into a UUID instance.
    """
    if not value:
        return None

    if isinstance(value, uuid.UUID):
        return value

    try:
        result = uuid.UUID(value)
    except (TypeError, ValueError):
        msg = f"Invalid uuid value: '{value}'"
        raise ValueError(msg)

    return result


def process_uuids_value(value: Sequence[Union[str, uuid.UUID]]) -> List[uuid.UUID]:
    """
    Processes a sequence of values into a sequence of UUIDs.

    Args:
        value (List[str or uuid]): Sequence of values to process.

    Returns:
        List[uuid]: Sequence of unique UUID instances.

    Raises:
        TypeError: If any item in `value` is not a UUID instance and cannot
            be converted into a UUID instance.
    """
    result = value or list()

    if isinstance(value, str):
        result = [result]
    else:
        try:
            result = list(result)
        except TypeError:
            result = [result]

    valid_values = []
    invalid_values = []
    for _id in result:
        try:
            _id = process_uuid_value(_id)
        except ValueError:
            invalid_values.append(_id)
        else:
            valid_values.append(_id)

    if invalid_values:
        invalid_values = [f"'{_id}'" for _id in invalid_values]
        msg = f"Invalid uuid values: {', '.join(invalid_values)}"
        raise ValueError(msg)

    seen: Set[uuid.UUID] = set()
    result = [id for id in valid_values if id and not (id in seen or seen.add(id))]

    return result


def process_elemental_class_value(
    value: Union[str, ElementalBase]
) -> Optional[ElementalBase]:
    """
    Processes a name into an Elemental class.

    Args:
        value (str or cls): Name of an `ElementalBase` subclass.

    Returns:
        A `ElementalBase` subclass if successful, None otherwise.
    """
    try:
        result = value if issubclass(value, ElementalBase) else None
    except TypeError:
        result = None

    if not result:
        value = str(value).lower().strip().replace(" ", "")
        for elemental_cls in ElementalBase.iter_elemental_types():
            if value == elemental_cls.__name__.lower():
                result = elemental_cls
                break

    return result


def process_data_format_value(value: str) -> Optional[str]:
    """
    Computes a standardized label for a data format.

    Args:
        value (str): Name of a data format

    Returns:
        Formatted string if successful, None otherwise.
    """
    if value:
        return str(value).lower().strip().replace(" ", "_")
    return None


def create_weak_ref(
    item: Union[Callable, object]
) -> Union[weakref.WeakMethod, weakref.ReferenceType, object]:
    try:
        result = weakref.WeakMethod(item)
    except TypeError:
        try:
            result = weakref.ref(item)
        except TypeError:
            result = item

    return result


def restore_weak_ref(
    item_ref: Union[Callable, object, weakref.ReferenceType]
) -> Union[weakref.ReferenceType, object]:
    result = item_ref
    if isinstance(result, weakref.ReferenceType):
        result = result()
    return result
