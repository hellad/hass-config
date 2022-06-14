<<<<<<< HEAD
import asyncio

from homeassistant.components.light import *
from homeassistant.const import STATE_ON
from homeassistant.core import callback
from homeassistant.helpers.restore_state import RestoreEntity

from . import DOMAIN
from .core.converters import ZIGBEE, MESH_GROUP_MODEL, Converter
from .core.device import XDevice
from .core.entity import XEntity
from .core.gateway import XGateway
=======
import logging
import math

from homeassistant.components.light import LightEntity, SUPPORT_BRIGHTNESS, \
    ATTR_BRIGHTNESS, SUPPORT_COLOR_TEMP, ATTR_COLOR_TEMP, ATTR_TRANSITION
from homeassistant.config import DATA_CUSTOMIZE
from homeassistant.util import color

from . import DOMAIN
from .core.gateway3 import Gateway3
from .core.helpers import XiaomiEntity

_LOGGER = logging.getLogger(__name__)
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

CONF_DEFAULT_TRANSITION = 'default_transition'


async def async_setup_entry(hass, config_entry, async_add_entities):
<<<<<<< HEAD
    def setup(gateway: XGateway, device: XDevice, conv: Converter):
        if conv.attr in device.entities:
            entity: XEntity = device.entities[conv.attr]
            entity.gw = gateway
        elif device.type == ZIGBEE:
            entity = XiaomiZigbeeLight(gateway, device, conv)
        elif device.model == MESH_GROUP_MODEL:
            entity = XiaomiMeshGroup(gateway, device, conv)
        else:
            entity = XiaomiMeshLight(gateway, device, conv)
        async_add_entities([entity])

    gw: XGateway = hass.data[DOMAIN][config_entry.entry_id]
    gw.add_setup(__name__, setup)


# noinspection PyAbstractClass
class XiaomiLight(XEntity, LightEntity, RestoreEntity):
    _attr_is_on = None

    def __init__(self, gateway: 'XGateway', device: XDevice, conv: Converter):
        super().__init__(gateway, device, conv)

        for conv in device.converters:
            if conv.attr == ATTR_BRIGHTNESS:
                self._attr_supported_features |= (
                        SUPPORT_BRIGHTNESS | SUPPORT_TRANSITION
                )
            elif conv.attr == ATTR_COLOR_TEMP:
                self._attr_supported_features |= SUPPORT_COLOR_TEMP
                if hasattr(conv, "minm") and hasattr(conv, "maxm"):
                    self._attr_min_mireds = conv.minm
                    self._attr_max_mireds = conv.maxm
                elif hasattr(conv, "mink") and hasattr(conv, "maxk"):
                    self._attr_min_mireds = int(1000000 / conv.maxk)
                    self._attr_max_mireds = int(1000000 / conv.mink)

    @callback
    def async_set_state(self, data: dict):
        if self.attr in data:
            self._attr_is_on = data[self.attr]
        # sometimes brightness and color_temp stored as string in Xiaomi DB
        if ATTR_BRIGHTNESS in data:
            self._attr_brightness = data[ATTR_BRIGHTNESS]
        if ATTR_COLOR_TEMP in data:
            self._attr_color_temp = data[ATTR_COLOR_TEMP]

    @callback
    def async_restore_last_state(self, state: str, attrs: dict):
        self._attr_is_on = state == STATE_ON
        self._attr_brightness = attrs.get(ATTR_BRIGHTNESS)
        self._attr_color_temp = attrs.get(ATTR_COLOR_TEMP)

    async def async_update(self):
        await self.device_read(self.subscribed_attrs)


# noinspection PyAbstractClass
class XiaomiZigbeeLight(XiaomiLight):
    async def async_turn_on(self, **kwargs):
        if ATTR_TRANSITION in kwargs:
            tr = kwargs.pop(ATTR_TRANSITION)
        elif CONF_DEFAULT_TRANSITION in self.customize:
            tr = self.customize[CONF_DEFAULT_TRANSITION]
        else:
            tr = None

        if tr is not None:
            if kwargs:
                # For the Aqara bulb, it is important that the brightness
                # parameter comes before the color_temp parameter. Only this
                # way transition will work. So we use `kwargs.pop` func to set
                # the exact order of parameters.
                for k in (ATTR_BRIGHTNESS, ATTR_COLOR_TEMP):
                    if k in kwargs:
                        kwargs[k] = (kwargs.pop(k), tr)
            else:
                kwargs[ATTR_BRIGHTNESS] = (255, tr)

        if not kwargs:
            kwargs[self.attr] = True

        await self.device_send(kwargs)

    async def async_turn_off(self, **kwargs):
        if ATTR_TRANSITION in kwargs:
            tr = kwargs[ATTR_TRANSITION]
        elif CONF_DEFAULT_TRANSITION in self.customize:
            tr = self.customize[CONF_DEFAULT_TRANSITION]
        else:
            tr = None

        if tr is not None:
            await self.device_send({ATTR_BRIGHTNESS: (0, tr)})
        else:
            await self.device_send({self.attr: False})


# noinspection PyAbstractClass
class XiaomiMeshBase(XiaomiLight):
    async def async_turn_on(self, **kwargs):
        kwargs[self.attr] = True
        await self.device_send(kwargs)

    async def async_turn_off(self):
        await self.device_send({self.attr: False})


# noinspection PyAbstractClass
class XiaomiMeshLight(XiaomiMeshBase):
    @callback
    def async_set_state(self, data: dict):
        super().async_set_state(data)

        if "group" not in self.device.entities:
            return
        # convert light attr to group attr
        if self.attr in data:
            data["group"] = data.pop(self.attr)
        group = self.device.entities["group"]
        group.async_set_state(data)
        group.async_write_ha_state()


# noinspection PyAbstractClass
class XiaomiMeshGroup(XiaomiMeshBase):
    def __init__(self, gateway: 'XGateway', device: XDevice, conv: Converter):
        super().__init__(gateway, device, conv)

        if not device.extra["childs"]:
            device.available = False
            return

        for did in device.extra["childs"]:
            child = gateway.devices[did]
            child.entities[self.attr] = self

    async def async_will_remove_from_hass(self) -> None:
        await super().async_will_remove_from_hass()
        for did in self.device.extra["childs"]:
            child = self.gw.devices[did]
            child.entities.pop(self.attr)

    async def async_update(self):
        # To update a group - request an update of its children
        # update_ha_state for all child light entities
        try:
            childs = []
            for did in self.device.extra["childs"]:
                light = self.gw.devices[did].entities.get("light")
                childs.append(light.async_update_ha_state(True))
            if childs:
                await asyncio.gather(*childs)

        except Exception as e:
            self.debug("Can't update child states", exc_info=e)
=======
    def setup(gateway: Gateway3, device: dict, attr: str):
        if device['type'] == 'zigbee':
            async_add_entities([XiaomiZigbeeLight(gateway, device, attr)])
        elif 'childs' in device:
            async_add_entities([XiaomiMeshGroup(gateway, device, attr)])
        else:
            async_add_entities([XiaomiMeshLight(gateway, device, attr)], True)

    gw: Gateway3 = hass.data[DOMAIN][config_entry.entry_id]
    gw.add_setup('light', setup)


class XiaomiZigbeeLight(XiaomiEntity, LightEntity):
    _brightness = None
    _color_temp = None

    @property
    def is_on(self) -> bool:
        return self._state

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""
        return self._brightness

    @property
    def color_temp(self):
        return self._color_temp

    @property
    def supported_features(self):
        return SUPPORT_BRIGHTNESS | SUPPORT_COLOR_TEMP

    def update(self, data: dict = None):
        if self.attr in data:
            self._state = bool(data[self.attr])
        # sometimes brightness and color_temp stored as string in Xiaomi DB
        if 'brightness' in data:
            self._brightness = int(data['brightness']) / 100.0 * 255.0
        if 'color_temp' in data:
            self._color_temp = int(data['color_temp'])

        self.schedule_update_ha_state()

    def turn_on(self, **kwargs):
        if ATTR_TRANSITION not in kwargs:
            custom = self.hass.data[DATA_CUSTOMIZE].get(self.entity_id)
            if CONF_DEFAULT_TRANSITION in custom:
                kwargs[ATTR_TRANSITION] = custom[CONF_DEFAULT_TRANSITION]

        # transition works only with raw zigbee commands
        # nwk empty for new device, it reloads only after restart integration
        if ATTR_TRANSITION in kwargs and 'nwk' in self.device:
            # is the amount of time, in tenths of a second
            tr = int(kwargs[ATTR_TRANSITION] * 10.0)
            commands = []

            # if only turn_on with transition restore last brightness
            if ATTR_BRIGHTNESS not in kwargs and ATTR_COLOR_TEMP not in kwargs:
                kwargs[ATTR_BRIGHTNESS] = self.brightness or 255

            if ATTR_BRIGHTNESS in kwargs:
                br = int(kwargs[ATTR_BRIGHTNESS])
                commands += [
                    f"zcl level-control o-mv-to-level {br} {tr}",
                    f"send 0x{self.device['nwk']} 1 1"
                ]

            if ATTR_COLOR_TEMP in kwargs:
                ct = int(kwargs[ATTR_COLOR_TEMP])
                commands += [
                    f"zcl color-control movetocolortemp {ct} {tr} 0 0",
                    f"send 0x{self.device['nwk']} 1 1"
                ]

            self.gw.send_zigbee_cli(commands)
            return

        payload = {}

        if ATTR_BRIGHTNESS in kwargs:
            payload['brightness'] = \
                int(kwargs[ATTR_BRIGHTNESS] / 255.0 * 100.0)

        if ATTR_COLOR_TEMP in kwargs:
            payload['color_temp'] = kwargs[ATTR_COLOR_TEMP]

        if not payload:
            payload[self.attr] = 1

        self.gw.send(self.device, payload)

    def turn_off(self, **kwargs):
        if ATTR_TRANSITION not in kwargs:
            custom = self.hass.data[DATA_CUSTOMIZE].get(self.entity_id)
            if CONF_DEFAULT_TRANSITION in custom:
                kwargs[ATTR_TRANSITION] = custom[CONF_DEFAULT_TRANSITION]

        # transition works only with raw zigbee commands
        if ATTR_TRANSITION in kwargs and 'nwk' in self.device:
            # is the amount of time, in tenths of a second
            tr = int(kwargs[ATTR_TRANSITION] * 10.0)
            commands = [
                f"zcl level-control o-mv-to-level 0 {tr}",
                f"send 0x{self.device['nwk']} 1 1"
            ]
            self.gw.send_zigbee_cli(commands)
            return

        self.gw.send(self.device, {self.attr: 0})


class XiaomiMeshLight(XiaomiEntity, LightEntity):
    _brightness = None
    _max_brightness = 65535
    _color_temp = None
    _min_mireds = int(1000000 / 6500)
    _max_mireds = int(1000000 / 2700)

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def is_on(self) -> bool:
        return self._state

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""
        return self._brightness

    @property
    def color_temp(self):
        return self._color_temp

    @property
    def min_mireds(self):
        return self._min_mireds

    @property
    def max_mireds(self):
        return self._max_mireds

    @property
    def supported_features(self):
        return SUPPORT_BRIGHTNESS | SUPPORT_COLOR_TEMP

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        color_temp = self.device.get('color_temp')
        if color_temp:
            self._min_mireds = math.floor(1000000 / color_temp[1])
            self._max_mireds = math.ceil(1000000 / color_temp[0])
        max_brightness = self.device.get('max_brightness')
        if max_brightness:
            self._max_brightness = max_brightness

    def update(self, data: dict = None):
        if data is None:
            self.gw.mesh_force_update()
            return

        if self.attr in data:
            # handle main attribute as online state
            if data[self.attr] is not None:
                self._state = bool(data[self.attr])
                self.device['online'] = True
            else:
                self.device['online'] = False

        if 'brightness' in data and data['brightness'] is not None:
            # 0...65535
            self._brightness = \
                data['brightness'] * 255.0 / self._max_brightness
        if 'color_temp' in data and data['color_temp']:
            # 2700..6500 => 370..153
            self._color_temp = \
                color.color_temperature_kelvin_to_mired(data['color_temp'])

        self.schedule_update_ha_state()

    def turn_on(self, **kwargs):
        # instantly change the HA state, and after 2 seconds check the actual
        # state of the lamp (optimistic change state)
        payload = {}

        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = kwargs[ATTR_BRIGHTNESS]
            payload['brightness'] = \
                int(self._brightness / 255.0 * self._max_brightness)

        if ATTR_COLOR_TEMP in kwargs:
            self._color_temp = kwargs[ATTR_COLOR_TEMP]
            if self._color_temp < self._min_mireds:
                self._color_temp = self._min_mireds
            if self._color_temp > self._max_mireds:
                self._color_temp = self._max_mireds
            payload['color_temp'] = \
                color.color_temperature_mired_to_kelvin(self._color_temp)

        if not payload:
            payload[self.attr] = True

        self._state = True

        self.gw.send_mesh(self.device, payload)

        self.schedule_update_ha_state()

    def turn_off(self):
        # instantly change the HA state, and after 2 seconds check the actual
        # state of the lamp (optimistic change state)
        self._state = False

        self.gw.send_mesh(self.device, {self.attr: False})

        self.schedule_update_ha_state()


class XiaomiMeshGroup(XiaomiMeshLight):
    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        if 'childs' in self.device:
            # add group to child bulb entities for processing update
            for did in self.device['childs']:
                self.gw.devices[did]['entities']['group'] = self

    async def async_will_remove_from_hass(self) -> None:
        await super().async_will_remove_from_hass()

        if 'childs' in self.device:
            for did in self.device['childs']:
                self.gw.devices[did]['entities'].pop('group')

    @property
    def should_poll(self):
        return False

    @property
    def icon(self):
        return 'mdi:lightbulb-group'
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
