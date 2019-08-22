import enum
from typing import Optional
from .client import Device
from .util import lookup_enum, lookup_reference_name, lookup_reference_title, lookup_reference_comment

class DehumOperation(enum.Enum):
    ON = "@operation_on"
    OFF = "@operation_off"

class DehumAIRREMOVAL(enum.Enum):
    OFF = "@AP_OFF_W"
    ON = "@AP_ON_W"

class DehumDevice(Device):
    """A higher-level interface for a dehum."""

    def set_on(self, is_on):
        mode = DehumOperation.ON if is_on else DehumOperation.OFF
        mode_value = self.model.enum_value('Operation', mode.value)
        self._set_control('Operation', mode_value)
            
    def set_mode(self, mode):
        mode_value = self.model.enum_value('OpMode', mode.value)
        self._set_control('OpMode', mode_value)

    def set_humidity(self, hum):
        """Set the device's target temperature in Celsius degrees.
        """
        self._set_control('HumidityCfg', hum)
    
    def set_windstrength(self, mode):
        windstrength_value = self.model.enum_value('WindStrength', mode.value)
        self._set_control('WindStrength', windstrength_value)
    
    def set_airremoval(self, is_on):
        mode = DehumAIRREMOVAL.ON if is_on else DehumAIRREMOVAL.OFF
        mode_value = self.model.enum_value('AirRemoval', mode.value)
        self._set_control('AirRemoval', mode_value)

    def poll(self) -> Optional['dehumStatus']:
        """Poll the device's current state.

        Monitoring must be started first with `monitor_start`.

        :returns: Either a `dehumStatus` instance or `None` if the status is
            not yet available.
        """
        # Abort if monitoring has not started yet.
        if not hasattr(self, 'mon'):
            return None

        data = self.mon.poll()
        if data:
            res = self.model.decode_monitor(data)
            return DehumStatus(self, res)
        
        else:
            return None


class DehumStatus(object):
    """Higher-level information about a dehum's current status.

    :param dehum: The DehumDevice instance.
    :param data: JSON data from the API.
    """

    def __init__(self, dehum: DehumDevice, data: dict):
        self.dehum = dehum
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
        """Get the type of the dehum."""
        return self.dehum.device.name

    @property
    def device_type(self):
        """Get the type of the dehum."""
        return self.dehum.model.model_type

    @property
    def is_on(self):
        op = DehumOperation(lookup_enum('Operation', self.data, self.dehum))
        return op == DehumOperation.ON

    @property
    def state(self):
        """Get the state of the dryer."""
        key = 'Operation'
        value = lookup_enum(key, self.data, self.dehum)
        if value is None:
            return 'Off'
        return value

    @property
    def mode(self):
        key = 'OpMode'
        value = lookup_enum(key, self.data, self.dehum)
        return value
   
    @property
    def windstrength_state(self):
        key = 'WindStrength'
        value = lookup_enum(key, self.data, self.dehum)
        return value
    
    @property
    def airremoval_state(self):
        key = 'AirRemoval'
        value = lookup_enum(key, self.data, self.dehum)
        return value
    
    @property
    def current_humidity(self):
        return self.data['SensorHumidity']
    
    @property
    def target_humidity(self):
        return self.data['HumidityCfg']