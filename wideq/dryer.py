import enum
from typing import Optional
from .client import Device
from .util import lookup_enum, lookup_reference_name, lookup_reference_title, lookup_reference_comment

class DryerDevice(Device):
    """A higher-level interface for a dryer."""

    def poll(self) -> Optional['dryerStatus']:
        """Poll the device's current state.

        Monitoring must be started first with `monitor_start`.

        :returns: Either a `dryerStatus` instance or `None` if the status is
            not yet available.
        """
        # Abort if monitoring has not started yet.
        if not hasattr(self, 'mon'):
            return None

        data = self.mon.poll()
        if data:
            res = self.model.decode_monitor(data)
            return DryerStatus(self, res)
        else:
            return None


class DryerStatus(object):
    """Higher-level information about a dryer's current status.

    :param dryer: The DryerDevice instance.
    :param data: JSON data from the API.
    """

    def __init__(self, dryer: DryerDevice, data: dict):
        self.dryer = dryer
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
        """Get the type of the dryer."""
        return self.dryer.device.name

    @property
    def device_type(self):
        """Get the type of the dryer."""
        return self.dryer.model.model_type

    @property
    def state(self):
        """Get the state of the dryer."""
        key = 'State'
        value = lookup_enum(key, self.data, self.dryer)
        if value is None:
            return 'Off'
        if value == '세탁 중':
            return '건조 중'
        if value == '전원 OFF':
            return 'Off'
        return value

    @property
    def dry_level(self):
        """Get the dry level."""
        key = 'DryLevel'
        value = lookup_enum(key, self.data, self.dryer)
        if value is None:
            return 'Off'
        if value == '-':
            return 'Off'
        return value

    @property
    def process_state(self):
        key = 'ProcessState'
        value = lookup_enum(key, self.data, self.dryer)
        return value

    @property
    def is_on(self) -> bool:
        """Check if the dryer is on or not."""
        return self.state != 'Off'

    @property
    def remaining_time(self) -> int:
        """Get the remaining time in minutes."""
        return (int(self.data['Remain_Time_H']) * 60 +
                int(self.data['Remain_Time_M']))

    @property
    def initial_time(self) -> int:
        """Get the initial time in minutes."""
        return (
            int(self.data['Initial_Time_H']) * 60 +
            int(self.data['Initial_Time_M']))

    @property
    def reserve_time(self) -> int:
        """Get the initial time in minutes."""
        return (
            int(self.data['Reserve_Initial_Time_H']) * 60 +
            int(self.data['Reserve_Initial_Time_M']))

    @property
    def course(self) -> str:
        """Get the current course."""
        key = 'Course'
        value = lookup_reference_name(key, self.data, self.dryer)
        return value

    @property
    def smart_course(self) -> str:
        """Get the current smart course."""
        key = 'SmartCourse'
        value = lookup_reference_name(key, self.data, self.dryer)
        return value

    @property
    def error(self) -> str:
        """Get the current error."""
        key = 'Error'
        value = lookup_reference_title(key, self.data, self.dryer)
        if value == "ERROR_NOERROR_TITLE":
            return "No"
        return value
