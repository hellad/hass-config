from homeassistant.components.climate import *
from homeassistant.components.climate.const import *
<<<<<<< HEAD
from homeassistant.core import callback

from . import DOMAIN
from .core.converters import Converter
from .core.device import XDevice
from .core.entity import XEntity
from .core.gateway import XGateway


async def async_setup_entry(hass, config_entry, async_add_entities):
    def setup(gateway: XGateway, device: XDevice, conv: Converter):
        if conv.attr in device.entities:
            entity: XEntity = device.entities[conv.attr]
            entity.gw = gateway
        else:
            entity = XiaomiClimate(gateway, device, conv)
        async_add_entities([entity])

    gw: XGateway = hass.data[DOMAIN][config_entry.entry_id]
    gw.add_setup(__name__, setup)


# noinspection PyAbstractClass
class XiaomiClimate(XEntity, ClimateEntity):
    _attr_fan_mode = None
    _attr_fan_modes = [FAN_LOW, FAN_MEDIUM, FAN_HIGH, FAN_AUTO]
    _attr_hvac_mode = None
    _attr_hvac_modes = [HVAC_MODE_OFF, HVAC_MODE_COOL, HVAC_MODE_HEAT]
    _attr_precision = PRECISION_WHOLE
    _attr_supported_features = SUPPORT_TARGET_TEMPERATURE | SUPPORT_FAN_MODE
    _attr_temperature_unit = TEMP_CELSIUS
    # support only KTWKQ03ES for now
    _attr_max_temp = 30
    _attr_min_temp = 17
    _attr_target_temperature_step = 1

    @callback
    def async_set_state(self, data: dict):
        self._attr_current_temperature = data.get("current_temp")
        self._attr_fan_mode = data.get("fan_mode")
        self._attr_hvac_mode = data.get("hvac_mode")
        # fix scenes with turned off climate
        # https://github.com/AlexxIT/XiaomiGateway3/issues/101#issuecomment-757781988
        self._attr_target_temperature = data.get("target_temp", 0)

    async def async_update(self):
        await self.device_read(self.subscribed_attrs)

    async def async_set_temperature(self, **kwargs) -> None:
        if kwargs[ATTR_TEMPERATURE] == 0:
            return
        payload = {"target_temp": kwargs[ATTR_TEMPERATURE]}
        await self.device_send({self.attr: payload})

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        payload = {"fan_mode": fan_mode}
        await self.device_send({self.attr: payload})

    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        payload = {"hvac_mode": hvac_mode}
        await self.device_send({self.attr: payload})
=======

from . import DOMAIN
from .core.gateway3 import Gateway3
from .core.helpers import XiaomiEntity

_LOGGER = logging.getLogger(__name__)

HVAC_MODES = [HVAC_MODE_HEAT, HVAC_MODE_COOL, HVAC_MODE_OFF]
FAN_MODES = [FAN_LOW, FAN_MEDIUM, FAN_HIGH, FAN_AUTO]

AC_STATE_HVAC = {
    HVAC_MODE_OFF: 0x01,
    HVAC_MODE_HEAT: 0x10,
    HVAC_MODE_COOL: 0x11
}
AC_STATE_FAN = {
    FAN_LOW: 0x00,
    FAN_MEDIUM: 0x10,
    FAN_HIGH: 0x20,
    FAN_AUTO: 0x30
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    def setup(gateway: Gateway3, device: dict, attr: str):
        async_add_entities([XiaomiClimate(gateway, device, attr)])

    gw: Gateway3 = hass.data[DOMAIN][config_entry.entry_id]
    gw.add_setup('climate', setup)


# noinspection PyAbstractClass
class XiaomiClimate(XiaomiEntity, ClimateEntity):
    _current_hvac = None
    _current_temp = None
    _fan_mode = None
    _hvac_mode = None
    _is_on = None
    _state: bytearray = None
    # fix scenes with turned off climate
    # https://github.com/AlexxIT/XiaomiGateway3/issues/101#issuecomment-757781988
    _target_temp = 0

    @property
    def precision(self) -> float:
        return PRECISION_WHOLE

    @property
    def temperature_unit(self):
        return TEMP_CELSIUS

    @property
    def hvac_mode(self) -> str:
        return self._hvac_mode if self._is_on else HVAC_MODE_OFF

    @property
    def hvac_modes(self):
        return [HVAC_MODE_OFF, HVAC_MODE_COOL, HVAC_MODE_HEAT]

    @property
    def current_temperature(self):
        return self._current_temp

    @property
    def target_temperature(self):
        return self._target_temp

    @property
    def fan_mode(self):
        return self._fan_mode

    @property
    def fan_modes(self):
        return FAN_MODES

    @property
    def supported_features(self):
        return SUPPORT_TARGET_TEMPERATURE | SUPPORT_FAN_MODE

    def update(self, data: dict = None):
        try:
            if 'power' in data:  # 0 - off, 1 - on
                self._is_on = data['power']

                # with power off all data come with empty values
                # https://github.com/AlexxIT/XiaomiGateway3/issues/101#issuecomment-747305596
                if self._is_on:
                    if 'mode' in data:  # 0 - heat, 1 - cool, 15 - off
                        self._hvac_mode = HVAC_MODES[data['mode']]
                    if 'fan_mode' in data:  # 0 - low, 3 - auto, 15 - off
                        self._fan_mode = FAN_MODES[data['fan_mode']]
                    if 'target_temperature' in data:  # 255 - off
                        self._target_temp = data['target_temperature']

                else:
                    self._fan_mode = None
                    self._hvac_mode = None
                    self._target_temp = 0

            if 'current_temperature' in data:
                self._current_temp = data['current_temperature']

            if self.attr in data:
                self._state = bytearray(
                    int(data[self.attr]).to_bytes(4, 'big')
                )

                # only first time when retain from gateway
                if isinstance(data[self.attr], str):
                    self._hvac_mode = next(
                        k for k, v in AC_STATE_HVAC.items()
                        if v == self._state[0]
                    )
                    self._fan_mode = next(
                        k for k, v in AC_STATE_FAN.items()
                        if v == self._state[1]
                    )
                    self._target_temp = self._state[2]

        except:
            _LOGGER.exception(f"Can't read climate data: {data}")

        self.schedule_update_ha_state()

    def set_temperature(self, **kwargs) -> None:
        if not self._state or kwargs[ATTR_TEMPERATURE] == 0:
            self.debug(f"Can't set climate temperature: {self._state}")
            return
        self._state[2] = int(kwargs[ATTR_TEMPERATURE])
        state = int.from_bytes(self._state, 'big')
        self.gw.send(self.device, {self.attr: state})

    def set_fan_mode(self, fan_mode: str) -> None:
        if not self._state:
            return
        self._state[1] = AC_STATE_FAN[fan_mode]
        state = int.from_bytes(self._state, 'big')
        self.gw.send(self.device, {self.attr: state})

    def set_hvac_mode(self, hvac_mode: str) -> None:
        if not self._state:
            return
        self._state[0] = AC_STATE_HVAC[hvac_mode]
        state = int.from_bytes(self._state, 'big')
        self.gw.send(self.device, {self.attr: state})
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
