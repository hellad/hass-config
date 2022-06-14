<<<<<<< HEAD
from homeassistant.const import STATE_ON
from homeassistant.core import callback
from homeassistant.helpers.entity import ToggleEntity
from homeassistant.helpers.restore_state import RestoreEntity

from . import DOMAIN
from .core.converters import Converter
from .core.device import XDevice
from .core.entity import XEntity
from .core.gateway import XGateway


async def async_setup_entry(hass, config_entry, add_entities):
    def setup(gateway: XGateway, device: XDevice, conv: Converter):
        if conv.attr in device.entities:
            entity: XEntity = device.entities[conv.attr]
            entity.gw = gateway
        else:
            entity = XiaomiSwitch(gateway, device, conv)
        add_entities([entity])

    gw: XGateway = hass.data[DOMAIN][config_entry.entry_id]
    gw.add_setup(__name__, setup)


# noinspection PyAbstractClass
class XiaomiSwitch(XEntity, ToggleEntity, RestoreEntity):
    _attr_is_on: bool = None

    @callback
    def async_set_state(self, data: dict):
        """Handle state update from gateway."""
        if self.attr in data:
            self._attr_is_on = data[self.attr]

    @callback
    def async_restore_last_state(self, state: str, attrs: dict):
        self._attr_is_on = state == STATE_ON

    async def async_turn_on(self):
        await self.device_send({self.attr: True})

    async def async_turn_off(self):
        await self.device_send({self.attr: False})

    async def async_update(self):
        await self.device_read(self.subscribed_attrs)
=======
import logging

from homeassistant.components import persistent_notification
from homeassistant.helpers.entity import ToggleEntity

from . import DOMAIN
from .core.gateway3 import Gateway3
from .core.helpers import XiaomiEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    def setup(gateway: Gateway3, device: dict, attr: str):
        if attr == 'firmware lock':
            async_add_entities([FirmwareLock(gateway, device, attr)])
        elif device['type'] == 'mesh':
            async_add_entities([XiaomiMeshSwitch(gateway, device, attr)])
        else:
            async_add_entities([XiaomiZigbeeSwitch(gateway, device, attr)])

    gw: Gateway3 = hass.data[DOMAIN][config_entry.entry_id]
    gw.add_setup('switch', setup)


class XiaomiZigbeeSwitch(XiaomiEntity, ToggleEntity):
    @property
    def is_on(self):
        return self._state

    def update(self, data: dict = None):
        # thread.run > mqtt.loop_forever > ... > thread.on_message
        #   > entity.update
        #   > entity.schedule_update_ha_state *
        #   > hass.add_job *
        #   > loop.call_soon_threadsafe *
        #   > hass.async_add_job *
        #   > hass.async_add_hass_job *
        #   > loop.create_task *
        #   > entity.async_update_ha_state *
        #   > entyty._async_write_ha_state
        #   > hass.states.async_set
        #   > bus.async_fire
        #   > hass.async_add_hass_job
        #   > loop.call_soon
        if self.attr in data:
            self._state = bool(data[self.attr])
        self.schedule_update_ha_state()

    def turn_on(self):
        self.gw.send(self.device, {self.attr: 1})

    def turn_off(self):
        self.gw.send(self.device, {self.attr: 0})


class XiaomiMeshSwitch(XiaomiEntity, ToggleEntity):
    @property
    def should_poll(self):
        return False

    @property
    def is_on(self):
        return self._state

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

        self.schedule_update_ha_state()

    def turn_on(self, **kwargs):
        self._state = True

        self.gw.send_mesh(self.device, {self.attr: True})

        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        self._state = False

        self.gw.send_mesh(self.device, {self.attr: False})

        self.schedule_update_ha_state()


class FirmwareLock(XiaomiZigbeeSwitch):
    @property
    def icon(self):
        return 'mdi:cloud-lock'

    def turn_on(self):
        if self.gw.lock_firmware(enable=True):
            self._state = True
            self.schedule_update_ha_state()

            persistent_notification.create(
                self.hass, "Firmware update is locked. You can sleep well.",
                "Xiaomi Gateway 3"
            )

    def turn_off(self):
        if self.gw.lock_firmware(enable=False):
            self._state = False
            self.schedule_update_ha_state()
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
