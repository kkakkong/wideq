import enum
from typing import Optional
from .client import Device
from .util import lookup_lang, lookup_enum, lookup_enum_lang, lookup_enum_value, lookup_reference_name, lookup_reference_title, lookup_reference_comment

RinseCount = {
    '0':'선택 안 함',
    '1': '1회',
    '2': '2회',
    '3': '3회',
    '4': '4회',
    '5': '5회',
    '6': '6회',
}

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
            return '꺼짐'
        else:
            return '켜짐'

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
        value = lookup_enum_lang(key, self.data, self.washer)
        if value is None:
            return '꺼짐'
        return value

    @property
    def previous_state(self):
        """Get the previous state of the washer."""
        key = 'PreState'
        value = lookup_enum_lang(key, self.data, self.washer)
        if value is None:
            return '꺼짐'
        return value

    @property
    def is_on(self) -> bool:
        """Check if the washer is on or not."""
        return self.state != '꺼짐'

    @property
    def remaining_time(self) -> int:
        """Get the remaining time in minutes."""
        if self.state == '대기 중':
            return 0
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
        if self.state == '대기 중':
            return 0
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

    @property
    def soil_level(self):
        key = 'SoilLevel'
        value = lookup_enum(key, self.data, self.washer)
        if value is None:
            return '꺼짐'
        elif value == '-':
            return '꺼짐'
        elif value == 'ON':
            return '켜짐'
        elif value == 'OFF':
            return '꺼짐'
        value = lookup_enum_lang(key, self.data, self.washer)
        return value

    @property
    def water_temp(self):
        key = 'WaterTemp'
        if self.device_type == 'TL':
            key = 'WTemp'
        value = lookup_enum(key, self.data, self.washer)
        if value is None:
            return '꺼짐'
        elif value == '-':
            return '꺼짐'
        elif value == 'ON':
            return '켜짐'
        elif value == 'OFF':
            return '꺼짐'
        value = lookup_enum_lang(key, self.data, self.washer)
        return value

    @property
    def spin_speed(self):
        key = 'SpinSpeed'
        value = lookup_enum(key, self.data, self.washer)
        if value is None:
            return '꺼짐'
        elif value == '-':
            return '꺼짐'
        elif value == 'ON':
            return '켜짐'
        elif value == 'OFF':
            return '꺼짐'
        value = lookup_enum_lang(key, self.data, self.washer)
        return value

    @property
    def rinse_count(self):
        key = 'RinseCount'
        value = lookup_enum(key, self.data, self.washer)
        if value is None:
            return '꺼짐'
        elif value == '-':
            return '꺼짐'
        elif value == 'ON':
            return '켜짐'
        elif value == 'OFF':
            return '꺼짐'
        try:
            value = RinseCount[str(int(value))]
        except ValueError:
            value = lookup_enum_lang(key, self.data, self.washer)
        return value

    @property
    def dry_level(self):
        key = 'DryLevel'
        if self.device_type == 'TL':
            return '없음'
        value = lookup_enum(key, self.data, self.washer)
        if value is None:
            return '꺼짐'
        elif value == '-':
            return '꺼짐'
        elif value == 'ON':
            return '켜짐'
        elif value == 'OFF':
            return '꺼짐'
        value = lookup_enum_lang(key, self.data, self.washer)
        return value

    @property
    def water_level(self):
        key = 'WLevel'
        if self.device_type == 'FL':
            return '없음'
        value = lookup_enum(key, self.data, self.washer)
        if value is None:
            return '꺼짐'
        elif value == '-':
            return '꺼짐'
        elif value == 'ON':
            return '켜짐'
        elif value == 'OFF':
            return '꺼짐'
        value = lookup_enum_lang(key, self.data, self.washer)
        return value

    @property
    def water_flow(self):
        key = 'WFlow'
        if self.device_type == 'FL':
            return '없음'
        value = lookup_enum(key, self.data, self.washer)
        if value is None:
            return '꺼짐'
        elif value == '-':
            return '꺼짐'
        elif value == 'ON':
            return '켜짐'
        elif value == 'OFF':
            return '꺼짐'
        value = lookup_enum_lang(key, self.data, self.washer)
        return value

    @property
    def soak(self):
        key = 'Soak'
        if self.device_type == 'FL':
            return '없음'
        value = lookup_enum(key, self.data, self.washer)
        if value is None:
            return '꺼짐'
        elif value == '-':
            return '꺼짐'
        elif value == 'ON':
            return '켜짐'
        elif value == 'OFF':
            return '꺼짐'
        value = lookup_enum_lang(key, self.data, self.washer)
        return value

    @property
    def fresh_care(self):
        key = 'Option1'
        index = 4
        if self.device_type == 'TL':
            return '없음'
        return self.get_bit(key, index)

    @property
    def child_lock(self):
        key = 'Option1'
        if self.device_type == 'FL':
          index = 3
        if self.device_type == 'TL':
          index = 0
        if index == 99:
            return '없음'
        return self.get_bit(key, index)

    @property
    def door_lock(self):
        key = 'Option1'
        if self.device_type == 'FL':
          index = 99
        if self.device_type == 'TL':
          index = 3
        if index == 99:
            return '없음'
        return self.get_bit(key, index)

    @property
    def steam(self):
        key = 'Option1'
        if self.device_type == 'FL':
          index = 4
        if self.device_type == 'TL':
          index = 2
        if index == 99:
            return '없음'
        return self.get_bit(key, index)

    @property
    def turbo_shot(self):
        key = 'Option2'
        if self.device_type == 'FL':
          index = 7
        if self.device_type == 'TL':
          index = 3
        if index == 99:
            return '없음'
        return self.get_bit(key, index)

    @property
    def buzzer(self):
        key = 'Option2'
        if self.device_type == 'FL':
          index = 99
        if self.device_type == 'TL':
          index = 0
        if index == 99:
            return '없음'
        return self.get_bit(key, index)

    @property
    def sterilize(self):
        key = 'Option2'
        if self.device_type == 'FL':
          index = 99
        if self.device_type == 'TL':
          index = 1
        if index == 99:
            return '없음'
        return self.get_bit(key, index)

    @property
    def heater(self):
        key = 'Option2'
        if self.device_type == 'FL':
          index = 99
        if self.device_type == 'TL':
          index = 2
        if index == 99:
            return '없음'
        return self.get_bit(key, index)

    @property
    def tubclean_count(self):
        if self.device_type == 'TL':
            return '없음'
        return self.data['TCLCount']

    @property
    def load_level(self):
        key = 'LoadLevel'
        if self.device_type == 'TL':
            return '없음'
        value = lookup_enum(key, self.data, self.washer)
        if value is None:
            return '꺼짐'
        elif value == '-':
            return '꺼짐'
        elif value == '0':
            return '없음'
        elif value == '1':
            return '소량'
        elif value == '2':
            return '적음'
        elif value == '3':
            return '보통'
        elif value == '4':
            return '많음'
        return value
