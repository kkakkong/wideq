import enum
from typing import Optional
from .client import Device
from .util import lookup_enum, lookup_reference_name, lookup_reference_title, lookup_reference_comment, lookup_lang

class WasherDevice(Device):
    """A higher-level interface for a washer."""

    def poll(self) -> Optional['washerStatus']:
        """Poll the device's current state.

        Monitoring must be started first with `monitor_start`.

        :returns: Either a `washerStatus` instance or `None` if the status is
            not yet available.
        """
        # Abort if monitoring has not started yet.
        if not hasattr(self, 'mon'):
            return None

        data = self.mon.poll()
        if data:
            res = self.model.decode_monitor(data)
            return WasherStatus(self, res)
        else:
            return None


class WasherStatus(object):
    """Higher-level information about a washer's current status.

    :param washer: The WasherDevice instance.
    :param data: JSON data from the API.
    """

    def __init__(self, washer: WasherDevice, data: dict):
        self.washer = washer
        self.data = data

    def get_bit(self, key: str, index: int) -> str:
        bit_value = int(self.data[key])
        bit_index = 2 ** index
        mode = bin(bit_value & bit_index)
        if mode == bin(0):
            return 'OFF'
        else:
            return 'ON'

    @property
    def device_name(self):
        """Get the type of the washer."""
        return self.washer.device.name

    @property
    def device_type(self):
        """Get the type of the washer."""
        return self.washer.model.model_type

    @property
    def state(self):
        """Get the state of the washer."""
        key = 'State'
        value = lookup_lang(key, self.data, self.washer)
        if value is None:
            return 'Off'
        return value

    @property
    def previous_state(self):
        """Get the previous state of the washer."""
        key = 'PreState'
        value = lookup_lang(key, self.data, self.washer)
        if value is None:
            return 'Off'
        return value

    @property
    def is_on(self) -> bool:
        """Check if the washer is on or not."""
        return self.state != 'Off'

    @property
    def remaining_time(self) -> int:
        """Get the remaining time in minutes."""
        return (int(self.data['Remain_Time_H']) * 60 +
                int(self.data['Remain_Time_M']))

    @property
    def reserve_time(self) -> int:
        """Get the initial time in minutes."""
        return (
            int(self.data['Reserve_Time_H']) * 60 +
            int(self.data['Reserve_Time_M']))

    @property
    def initial_time(self) -> int:
        """Get the initial time in minutes."""
        return (
            int(self.data['Initial_Time_H']) * 60 +
            int(self.data['Initial_Time_M']))

    @property
    def course(self) -> str:
        """Get the current course."""
        key = 'APCourse'
        if self.device_type == 'TL':
            key = 'Course'
        value = lookup_reference_name(key, self.data, self.washer)
        return value

    @property
    def smart_course(self) -> str:
        """Get the current smart course."""
        key = 'SmartCourse'
        value = lookup_reference_name(key, self.data, self.washer)
        return value

    @property
    def error(self) -> str:
        """Get the current error."""
        key = 'Error'
        value = lookup_reference_title(key, self.data, self.washer)
        return value
