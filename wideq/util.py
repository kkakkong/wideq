from typing import TypeVar
from .client import Device

T = TypeVar('T', bound=Device)

def lookup_lang(attr: str, data: dict, device: T):
    """Looks up an enum value for the provided attr.

    :param attr: The attribute to lookup in the enum.
    :param data: The JSON data from the API.
    :param device: A sub-class instance of a Device.
    :returns: The enum value.
    """
    value = device.model.enum_name(attr, data[attr])
    if value is None:
        return 'Off'
    if value == '@operation_on':
        return 'On'
    elif value == '@operation_off':
        return 'Off'
    try:
        lang = device.lang_product.enum_name(attr, value)
    except KeyError:
        lang = value
    if str.find(lang, '@WM') != -1:
        try:
            lang = device.lang_model.enum_name(attr, value)
        except KeyError:
            lang = value
    return lang

def lookup_enum(attr: str, data: dict, device: T):
    """Looks up an enum value for the provided attr.

    :param attr: The attribute to lookup in the enum.
    :param data: The JSON data from the API.
    :param device: A sub-class instance of a Device.
    :returns: The enum value.
    """
    return device.model.enum_name(attr, data[attr])

def lookup_enum_value(attr: str, data: dict, device: T):
    """Looks up an enum value for the provided attr.

    :param attr: The attribute to lookup in the enum.
    :param data: The JSON data from the API.
    :param device: A sub-class instance of a Device.
    :returns: The enum value.
    """
    return device.model.enum_value(attr, data[attr])

def lookup_reference_name(attr: str, data: dict, device: T) -> str:
    """Look up a reference value for the provided attribute.

    :param attr: The attribute to find the value for.
    :param data: The JSON data from the API.
    :param device: A sub-class instance of a Device.
    :returns: The looked up value.
    """
    value = device.model.reference_name(attr, data[attr])
    if value is None:
        return 'Off'
    try:
        lang = device.lang_product['pack'][device.model.value(attr).reference.get(value, value)]
    except KeyError:
        lang = value
    if str.find(lang, '@WM') != -1:
        try:
            lang = device.lang_model['pack'][device.model.value(attr).reference.get(value, value)]
        except KeyError:
            lang = value
    return lang

def lookup_reference_title(attr: str, data: dict, device: T) -> str:
    """Look up a reference value for the provided attribute.

    :param attr: The attribute to find the value for.
    :param data: The JSON data from the API.
    :param device: A sub-class instance of a Device.
    :returns: The looked up value.
    """
    value = device.model.reference_title(attr, data[attr])
    if value is None:
        return 'Off'
    try:
        lang = device.lang_product['pack'][device.model.value(attr).reference.get(value, value)]
    except KeyError:
        lang = value
    if str.find(lang, '@WM') != -1:
        try:
            lang = device.lang_model['pack'][device.model.value(attr).reference.get(value, value)]
        except KeyError:
            lang = value
    return lang

def lookup_reference_comment(attr: str, data: dict, device: T) -> str:
    """Look up a reference value for the provided attribute.

    :param attr: The attribute to find the value for.
    :param data: The JSON data from the API.
    :param device: A sub-class instance of a Device.
    :returns: The looked up value.
    """
    value = device.model.reference_comment(attr, data[attr])
    if value is None:
        return 'Off'
    try:
        lang = device.lang_product['pack'][device.model.value(attr).reference.get(value, value)]
    except KeyError:
        lang = value
    if str.find(lang, '@WM') != -1:
        try:
            lang = device.lang_model['pack'][device.model.value(attr).reference.get(value, value)]
        except KeyError:
            lang = value
    return lang
