<<<<<<< HEAD
import asyncio
import time
from datetime import timedelta

from homeassistant.components.automation import ATTR_LAST_TRIGGERED
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import STATE_ON
from homeassistant.core import callback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util.dt import now

from . import DOMAIN
from .core.converters import Converter, GATEWAY
from .core.device import XDevice
from .core.entity import XEntity
from .core.gateway import XGateway

SCAN_INTERVAL = timedelta(seconds=60)

CONF_INVERT_STATE = "invert_state"
CONF_OCCUPANCY_TIMEOUT = "occupancy_timeout"


async def async_setup_entry(hass, config_entry, async_add_entities):
    def setup(gateway: XGateway, device: XDevice, conv: Converter):
        if conv.attr in device.entities:
            entity: XEntity = device.entities[conv.attr]
            entity.gw = gateway
        elif conv.attr == "motion":
            entity = XiaomiMotionSensor(gateway, device, conv)
        elif conv.attr == GATEWAY:
            entity = XiaomiGateway(gateway, device, conv)
        else:
            entity = XiaomiBinarySensor(gateway, device, conv)
        async_add_entities([entity])

    gw: XGateway = hass.data[DOMAIN][config_entry.entry_id]
    gw.add_setup(__name__, setup)


class XiaomiBinaryBase(XEntity, BinarySensorEntity):
    @callback
    def async_set_state(self, data: dict):
        if self.attr in data:
            # support invert_state for sensor
            self._attr_is_on = not data[self.attr] \
                if self.customize.get(CONF_INVERT_STATE, False) \
                else data[self.attr]

        for k, v in data.items():
            if k in self.subscribed_attrs and k != self.attr:
                self._attr_extra_state_attributes[k] = v


class XiaomiBinarySensor(XiaomiBinaryBase, RestoreEntity):
    @callback
    def async_restore_last_state(self, state: str, attrs: dict):
        self._attr_is_on = state == STATE_ON
        for k, v in attrs.items():
            if k in self.subscribed_attrs:
                self._attr_extra_state_attributes[k] = v

    async def async_update(self):
        await self.device_read(self.subscribed_attrs)


class XiaomiGateway(XiaomiBinaryBase):
    @callback
    def async_update_available(self):
        # sensor state=connected when whole gateway available
        self._attr_is_on = self.gw.available

    @property
    def available(self):
        return True


class XiaomiMotionSensor(XEntity, BinarySensorEntity):
    _attr_is_on = False
    _default_delay = None
    _last_on = 0
    _last_off = 0
    _timeout_pos = 0
    _clear_task: asyncio.Task = None

    async def async_clear_state(self, delay: float):
        await asyncio.sleep(delay)

        self._last_off = time.time()
        self._timeout_pos = 0

        self._attr_is_on = False
        self.async_write_ha_state()

    async def async_will_remove_from_hass(self):
        if self._clear_task:
            self._clear_task.cancel()

        if self._attr_is_on:
            self._attr_is_on = False
            self.async_write_ha_state()

        await super().async_will_remove_from_hass()

    @callback
    def async_set_state(self, data: dict):
        # fix 1.4.7_0115 heartbeat error (has motion in heartbeat)
        if "battery" in data or not self.hass:
            return

        assert data[self.attr] == True

        # don't trigger motion right after illumination
        ts = time.time()
        if ts - self._last_on < 1:
            return

        if self._clear_task:
            self._clear_task.cancel()

        self._attr_is_on = True
        self._attr_extra_state_attributes[ATTR_LAST_TRIGGERED] = \
            now().isoformat(timespec="seconds")
        self._last_on = ts

        # if customize of any entity will be changed from GUI - default value
        # for all motion sensors will be erased
        timeout = self.customize.get(CONF_OCCUPANCY_TIMEOUT, 90)
=======
import logging
import time

from homeassistant.components.automation import ATTR_LAST_TRIGGERED
from homeassistant.components.binary_sensor import BinarySensorEntity, \
    DEVICE_CLASS_DOOR, DEVICE_CLASS_MOISTURE
from homeassistant.config import DATA_CUSTOMIZE
from homeassistant.helpers.event import async_call_later
from homeassistant.util.dt import now

from . import DOMAIN
from .core.gateway3 import Gateway3
from .core.helpers import XiaomiEntity

_LOGGER = logging.getLogger(__name__)

DEVICE_CLASS = {
    'contact': DEVICE_CLASS_DOOR,
    'water_leak': DEVICE_CLASS_MOISTURE,
}

CONF_INVERT_STATE = 'invert_state'
CONF_OCCUPANCY_TIMEOUT = 'occupancy_timeout'


async def async_setup_entry(hass, config_entry, async_add_entities):
    def setup(gateway: Gateway3, device: dict, attr: str):
        if attr == 'motion':
            async_add_entities([XiaomiMotionSensor(gateway, device, attr)])
        elif attr == 'power':
            async_add_entities([XiaomiKettleSensor(gateway, device, attr)])
        else:
            async_add_entities([XiaomiBinarySensor(gateway, device, attr)])

    gw: Gateway3 = hass.data[DOMAIN][config_entry.entry_id]
    gw.add_setup('binary_sensor', setup)


class XiaomiBinarySensor(XiaomiEntity, BinarySensorEntity):
    @property
    def is_on(self):
        return self._state

    @property
    def device_class(self):
        return DEVICE_CLASS.get(self.attr, self.attr)

    def update(self, data: dict = None):
        if self.attr in data:
            custom = self.hass.data[DATA_CUSTOMIZE].get(self.entity_id)
            if not custom.get(CONF_INVERT_STATE):
                # gas and smoke => 1 and 2
                self._state = bool(data[self.attr])
            else:
                self._state = not data[self.attr]

        self.schedule_update_ha_state()


KETTLE = {
    0: 'idle',
    1: 'heat',
    2: 'cool_down',
    3: 'warm_up',
}


class XiaomiKettleSensor(XiaomiBinarySensor):
    def update(self, data: dict = None):
        if self.attr in data:
            value = data[self.attr]
            self._state = bool(value)
            self._attrs['action_id'] = value
            self._attrs['action'] = KETTLE[value]

        self.schedule_update_ha_state()


class XiaomiMotionBase(XiaomiEntity):
    _default_delay = None
    _last_off = 0
    _timeout_pos = 0
    _unsub_set_no_motion = None
    _state_off = False

    async def async_added_to_hass(self):
        # old version
        self._default_delay = self.device.get(CONF_OCCUPANCY_TIMEOUT, 90)

        custom: dict = self.hass.data[DATA_CUSTOMIZE].get(self.entity_id)
        custom.setdefault(CONF_OCCUPANCY_TIMEOUT, self._default_delay)

        await super().async_added_to_hass()

    async def _start_no_motion_timer(self, delay: float):
        if self._unsub_set_no_motion:
            self._unsub_set_no_motion()

        self._unsub_set_no_motion = async_call_later(
            self.hass, abs(delay), self._set_no_motion)

    async def _set_no_motion(self, *args):
        self.debug("Clear motion")

        self._last_off = time.time()
        self._timeout_pos = 0
        self._unsub_set_no_motion = None
        self._state = self._state_off
        self.schedule_update_ha_state()

    def _trigger_motion(self):
        self._attrs[ATTR_LAST_TRIGGERED] = now().isoformat(timespec='seconds')

        if self._unsub_set_no_motion:
            self._unsub_set_no_motion()

        custom = self.hass.data[DATA_CUSTOMIZE].get(self.entity_id)
        # if customize of any entity will be changed from GUI - default value
        # for all motion sensors will be erased
        timeout = custom.get(CONF_OCCUPANCY_TIMEOUT, self._default_delay)
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        if timeout:
            if isinstance(timeout, list):
                pos = min(self._timeout_pos, len(timeout) - 1)
                delay = timeout[pos]
                self._timeout_pos += 1
            else:
                delay = timeout

<<<<<<< HEAD
            if delay < 0 and ts + delay < self._last_off:
=======
            if delay < 0 and time.time() + delay < self._last_off:
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
                delay *= 2

            self.debug(f"Extend delay: {delay} seconds")

<<<<<<< HEAD
            self._clear_task = self.hass.loop.create_task(
                self.async_clear_state(abs(delay))
            )

        # repeat event from Aqara integration
        self.hass.bus.async_fire("xiaomi_aqara.motion", {
            "entity_id": self.entity_id
=======
            self.hass.add_job(self._start_no_motion_timer, delay)

        return True


class XiaomiMotionSensor(XiaomiMotionBase, XiaomiBinarySensor):
    _last_on = 0

    def update(self, data: dict = None):
        # fix 1.4.7_0115 heartbeat error (has motion in heartbeat)
        if 'battery' in data:
            return

        # https://github.com/AlexxIT/XiaomiGateway3/issues/135
        if 'illuminance' in data and ('lumi.sensor_motion.aq2' in
                                      self.device['device_model']):
            data[self.attr] = 1

        # check only motion=1
        if data.get(self.attr) != 1:
            # handle available change
            self.schedule_update_ha_state()
            return

        # don't trigger motion right after illumination
        t = time.time()
        if t - self._last_on < 1:
            return
        self._last_on = t

        self._state = True
        self._trigger_motion()

        # handle available change
        self.schedule_update_ha_state()

        # repeat event from Aqara integration
        self.hass.bus.fire('xiaomi_aqara.motion', {
            'entity_id': self.entity_id
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        })
