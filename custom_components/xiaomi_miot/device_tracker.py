"""Support for Xiaomi device tracker."""
import logging
<<<<<<< HEAD
import time
=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
from datetime import timedelta

from homeassistant.const import *  # noqa: F401
from homeassistant.components.device_tracker import (
    DOMAIN as ENTITY_DOMAIN,
)
<<<<<<< HEAD
from homeassistant.components.device_tracker.const import SOURCE_TYPE_GPS
=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
from homeassistant.components.device_tracker.config_entry import TrackerEntity

from . import (
    DOMAIN,
    CONF_MODEL,
    XIAOMI_CONFIG_SCHEMA as PLATFORM_SCHEMA,  # noqa: F401
    MiotEntity,
    async_setup_config_entry,
    bind_services_to_entries,
)
from .core.miot_spec import (
    MiotSpec,
    MiotService,
)
from .binary_sensor import MiotBinarySensorSubEntity

_LOGGER = logging.getLogger(__name__)
DATA_KEY = f'{ENTITY_DOMAIN}.{DOMAIN}'
SCAN_INTERVAL = timedelta(seconds=60)

SERVICE_TO_METHOD = {}


async def async_setup_entry(hass, config_entry, async_add_entities):
    await async_setup_config_entry(hass, config_entry, async_setup_platform, async_add_entities, ENTITY_DOMAIN)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    hass.data.setdefault(DATA_KEY, {})
    hass.data[DOMAIN]['add_entities'][ENTITY_DOMAIN] = async_add_entities
<<<<<<< HEAD
    config['hass'] = hass
    model = str(config.get(CONF_MODEL) or '')
    entities = []
    if miot := config.get('miot_type'):
        spec = await MiotSpec.async_from_type(hass, miot)
        for srv in spec.get_services('watch', 'rearview_mirror', 'head_up_display'):
            if 'xiaoxun.watch.' in model:
                entities.append(XiaoxunWatchTrackerEntity(config, srv))
            elif srv.get_property('latitude', 'longitude'):
                entities.append(MiotTrackerEntity(config, srv))
    if not entities and 'xiaoxun.watch.' in model:
        # xiaoxun.watch.sw763
        entities.append(XiaoxunWatchTrackerEntity(config))
=======
    model = str(config.get(CONF_MODEL) or '')
    if model.find('mirror') >= 0:
        _LOGGER.debug('Setup device_tracker: %s', config)
    entities = []
    miot = config.get('miot_type')
    if miot:
        spec = await MiotSpec.async_from_type(hass, miot)
        for srv in spec.get_services('watch', 'rearview_mirror', 'head_up_display'):
            if not srv.get_property('latitude', 'longitude'):
                continue
            entities.append(MiotTrackerEntity(config, srv))
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    for entity in entities:
        hass.data[DOMAIN]['entities'][entity.unique_id] = entity
    async_add_entities(entities, update_before_add=True)
    bind_services_to_entries(hass, SERVICE_TO_METHOD)


class MiotTrackerEntity(MiotEntity, TrackerEntity):
<<<<<<< HEAD
    _attr_latitude = None
    _attr_longitude = None
    _attr_location_name = None
    _attr_location_accuracy = 0
    _disable_location_name = False

    def __init__(self, config, miot_service: MiotService = None):
        super().__init__(miot_service, config=config, logger=_LOGGER)

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self._disable_location_name = self.custom_config_bool('disable_location_name')

    async def async_update(self):
        await super().async_update()
        if not self._available or not self._miot_service:
            return

        if prop := self._miot_service.get_property('latitude'):
            self._attr_latitude = prop.from_dict(self._state_attrs)
        if prop := self._miot_service.get_property('longitude'):
            self._attr_longitude = prop.from_dict(self._state_attrs)
        if prop := self._miot_service.get_property('current_address'):
            self._attr_location_name = prop.from_dict(self._state_attrs)

=======
    def __init__(self, config, miot_service: MiotService):
        super().__init__(miot_service, config=config, logger=_LOGGER)

    async def async_update(self):
        await super().async_update()
        if not self._available:
            return
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        add_binary_sensors = self._add_entities.get('binary_sensor')
        for p in self._miot_service.get_properties('driving_status'):
            if p.full_name in self._subs:
                self._subs[p.full_name].update()
            elif add_binary_sensors and p.format == 'bool':
                self._subs[p.full_name] = MiotBinarySensorSubEntity(self, p)
<<<<<<< HEAD
                add_binary_sensors([self._subs[p.full_name]], update_before_add=True)
=======
                add_binary_sensors([self._subs[p.full_name]])
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

    @property
    def should_poll(self):
        """No polling for entities that have location pushed."""
        return True

    @property
    def source_type(self):
        """Return the source type, eg gps or router, of the device."""
<<<<<<< HEAD
        return SOURCE_TYPE_GPS
=======
        return 'gps'
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

    @property
    def latitude(self):
        """Return latitude value of the device."""
<<<<<<< HEAD
        return self._attr_latitude
=======
        prop = self._miot_service.get_property('latitude')
        if prop:
            return prop.from_dict(self._state_attrs)
        return NotImplementedError
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

    @property
    def longitude(self):
        """Return longitude value of the device."""
<<<<<<< HEAD
        return self._attr_longitude
=======
        prop = self._miot_service.get_property('longitude')
        if prop:
            return prop.from_dict(self._state_attrs)
        return NotImplementedError
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

    @property
    def location_name(self):
        """Return a location name for the current location of the device."""
<<<<<<< HEAD
        if self._disable_location_name:
            return None
        return self._attr_location_name
=======
        prop = self._miot_service.get_property('current_address')
        if prop:
            return prop.from_dict(self._state_attrs)
        return None
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

    @property
    def location_accuracy(self):
        """Return the location accuracy of the device.
        Value in meters.
        """
<<<<<<< HEAD
        return self._attr_location_accuracy
=======
        return 0
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

    @property
    def battery_level(self):
        """Return the battery level of the device."""
<<<<<<< HEAD
        if not self._miot_service:
            return None
=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        sls = [self._miot_service, *self._miot_service.spec.get_services('battery')]
        for srv in sls:
            prop = srv.get_property('battery_level')
            if prop:
                return prop.from_dict(self._state_attrs)
        return None
<<<<<<< HEAD


class XiaoxunWatchTrackerEntity(MiotTrackerEntity):
    def __init__(self, config, miot_service: MiotService = None, miot_spec: MiotSpec = None):
        self._miot_spec = miot_spec
        super().__init__(config=config, miot_service=miot_service)

    @property
    def device_eid(self):
        did = f'{self.miot_did}'
        return did.replace('xiaoxun.', '')

    async def async_update(self):
        await super().async_update()
        await self.update_location()

    async def update_location(self):
        did = f'{self.miot_did}'
        mic = self.xiaomi_cloud
        if not did or not mic:
            return
        pms = {
            'app_id': '10025',
            'dids': [did],
            'params': {
                'CID': 50031,
                'model': self._model,
                'SN': int(time.time() / 1000),
                'PL': {
                    'Size': 1,
                    'Key': '78999898989898998',
                    'EID': self.device_eid,
                },
            },
        }
        rdt = await self.hass.async_add_executor_job(mic.request_miot_api, 'third/api', pms) or {}
        loc = {}
        for v in (rdt.get('result') or {}).get('PL', {}).get('List', {}).values():
            loc = v.get('result', {})
            break
        if not loc:
            self.logger.warning('%s: Got xiaoxun watch location faild: %s', self.name_model, rdt)
            return
        self.logger.debug('%s: Got xiaoxun watch location: %s', self.name_model, rdt)
        gps = f"{loc.get('location', '')},".split(',')
        self._attr_latitude = float(gps[1])
        self._attr_longitude = float(gps[0])
        self._attr_location_name = loc.get('desc')
        self._attr_location_accuracy = int(loc.get('radius') or 0)
        tim = loc.get('timestamp', '')
        self.update_attrs({
            'timestamp': f'{tim[0:4]}-{tim[4:6]}-{tim[6:8]} {tim[8:10]}:{tim[10:12]}:{tim[12:14]}',
        })
=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
