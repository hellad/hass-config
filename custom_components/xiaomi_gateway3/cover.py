<<<<<<< HEAD
from homeassistant.components.cover import CoverEntity, ATTR_POSITION, \
    ATTR_CURRENT_POSITION
from homeassistant.const import STATE_CLOSING, STATE_OPENING
from homeassistant.core import callback
from homeassistant.helpers.restore_state import RestoreEntity

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
            entity = XiaomiCover(gateway, device, conv)
        async_add_entities([entity])

    gw: XGateway = hass.data[DOMAIN][config_entry.entry_id]
    gw.add_setup(__name__, setup)


# noinspection PyAbstractClass
class XiaomiCover(XEntity, CoverEntity, RestoreEntity):
    _attr_current_cover_position = 0
    _attr_is_closed = None

    @callback
    def async_set_state(self, data: dict):
        if 'run_state' in data:
            self._attr_state = data["run_state"]
            self._attr_is_opening = self._attr_state == STATE_OPENING
            self._attr_is_closing = self._attr_state == STATE_CLOSING
        if 'position' in data:
            self._attr_current_cover_position = data['position']
            self._attr_is_closed = self._attr_current_cover_position == 0

    @callback
    def async_restore_last_state(self, state: str, attrs: dict):
        if not state:
            return
        self.async_set_state({
            "run_state": state,
            "position": attrs[ATTR_CURRENT_POSITION]
        })

    async def async_open_cover(self, **kwargs):
        await self.device_send({self.attr: "open"})

    async def async_close_cover(self, **kwargs):
        await self.device_send({self.attr: "close"})

    async def async_stop_cover(self, **kwargs):
        await self.device_send({self.attr: "stop"})

    async def async_set_cover_position(self, **kwargs):
        await self.device_send({"position": kwargs[ATTR_POSITION]})
=======
import logging

from homeassistant.components.cover import CoverEntity, ATTR_POSITION, \
    ATTR_CURRENT_POSITION
from homeassistant.const import STATE_CLOSING, STATE_OPENING

from . import DOMAIN
from .core.gateway3 import Gateway3
from .core.helpers import XiaomiEntity

_LOGGER = logging.getLogger(__name__)

RUN_STATES = {0: STATE_CLOSING, 1: STATE_OPENING}


async def async_setup_entry(hass, config_entry, async_add_entities):
    def setup(gateway: Gateway3, device: dict, attr: str):
        if device.get('lumi_spec'):
            async_add_entities([XiaomiCover(gateway, device, attr)])
        else:
            async_add_entities([XiaomiCoverMIOT(gateway, device, attr)])

    gw: Gateway3 = hass.data[DOMAIN][config_entry.entry_id]
    gw.add_setup('cover', setup)


class XiaomiCover(XiaomiEntity, CoverEntity):
    @property
    def current_cover_position(self):
        return self._attrs.get(ATTR_CURRENT_POSITION)

    @property
    def is_opening(self):
        return self._state == STATE_OPENING

    @property
    def is_closing(self):
        return self._state == STATE_CLOSING

    @property
    def is_closed(self):
        return self.current_cover_position == 0

    def update(self, data: dict = None):
        if 'run_state' in data:
            self._state = RUN_STATES.get(data['run_state'])

        if 'position' in data:
            self._attrs[ATTR_CURRENT_POSITION] = data['position']

        self.schedule_update_ha_state()

    def open_cover(self, **kwargs):
        self.gw.send(self.device, {'motor': 1})

    def close_cover(self, **kwargs):
        self.gw.send(self.device, {'motor': 0})

    def stop_cover(self, **kwargs):
        self.gw.send(self.device, {'motor': 2})

    def set_cover_position(self, **kwargs):
        position = kwargs.get(ATTR_POSITION)
        self.gw.send(self.device, {'position': position})


class XiaomiCoverMIOT(XiaomiCover):
    def open_cover(self, **kwargs):
        self.gw.send(self.device, {'motor': 2})

    def close_cover(self, **kwargs):
        self.gw.send(self.device, {'motor': 1})

    def stop_cover(self, **kwargs):
        self.gw.send(self.device, {'motor': 0})

    def set_cover_position(self, **kwargs):
        position = kwargs.get(ATTR_POSITION)
        self.gw.send(self.device, {'target_position': position})
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
