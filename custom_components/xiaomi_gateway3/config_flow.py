<<<<<<< HEAD
=======
import logging

>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, OptionsFlow, ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from . import DOMAIN
from .core import utils
<<<<<<< HEAD
from .core.xiaomi_cloud import MiCloud

ACTIONS = {
    "cloud": "Add Mi Cloud Account",
    "token": "Add Gateway using Token"
}

SERVERS = {
    "cn": "China",
    "de": "Europe",
    "i2": "India",
    "ru": "Russia",
    "sg": "Singapore",
    "us": "United States"
}

OPT_DEBUG = {
    "true": "Basic logs",
    "mqtt": "MQTT logs",
    "zigbee": "Zigbee logs",
}


class FlowHandler(ConfigFlow, domain=DOMAIN):
    VERSION = 1
=======
from .core.gateway3 import TELNET_CMD, Gateway3
from .core.xiaomi_cloud import MiCloud

_LOGGER = logging.getLogger(__name__)

ACTIONS = {
    'cloud': "Add Mi Cloud Account",
    'token': "Add Gateway using Token"
}

SERVERS = {
    'cn': "China",
    'de': "Europe",
    'i2': "India",
    'ru': "Russia",
    'sg': "Singapore",
    'us': "United States"
}

OPT_DEBUG = {
    'true': "Basic logs",
    'miio': "miIO logs",
    'mqtt': "MQTT logs"
}
OPT_PARENT = {
    -1: "Disabled", 0: "Manually", 60: "Hourly"
}
OPT_MODE = {
    False: "Mi Home",
    True: "Zigbee Home Automation (ZHA)",
    'z2m': "zigbee2mqtt"
}


class XiaomiGateway3FlowHandler(ConfigFlow, domain=DOMAIN):
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    cloud = None

    async def async_step_user(self, user_input=None):
        if user_input is not None:
<<<<<<< HEAD
            if user_input["action"] == "cloud":
                return await self.async_step_cloud()
            elif user_input["action"] == "token":
                return await self.async_step_token()
            else:
                device = next(
                    device for device in self.hass.data[DOMAIN]["devices"]
                    if device["did"] == user_input["action"]
                )
                return self.async_show_form(
                    step_id="token",
                    data_schema=vol.Schema({
                        vol.Required("host", default=device["localip"]): str,
                        vol.Required("token", default=device["token"]): str,
                        vol.Required("telnet_cmd"): str,
                    }),
                )

        if DOMAIN in self.hass.data and "devices" in self.hass.data[DOMAIN]:
            for device in self.hass.data[DOMAIN]["devices"]:
                if (device["model"] in utils.SUPPORTED_MODELS and
                        device["did"] not in ACTIONS):
                    name = f"Add {device['name']} ({device['localip']})"
                    ACTIONS[device["did"]] = name

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("action", default="cloud"): vol.In(ACTIONS)
=======
            if user_input['action'] == 'cloud':
                return await self.async_step_cloud()
            elif user_input['action'] == 'token':
                return await self.async_step_token()
            elif user_input['action'] == 'ble':
                return await self.async_step_ble()
            else:
                device = next(d for d in self.hass.data[DOMAIN]['devices']
                              if d['did'] == user_input['action'])
                return self.async_show_form(
                    step_id='token',
                    data_schema=vol.Schema({
                        vol.Required('host', default=device['localip']): str,
                        vol.Required('token', default=device['token']): str,
                        vol.Required('telnet_cmd', default=TELNET_CMD): str,
                    }),
                )

        actions = ACTIONS.copy()

        if Gateway3.ble_known:
            actions['ble'] = "Add BLE Device"

        if DOMAIN in self.hass.data and 'devices' in self.hass.data[DOMAIN]:
            for device in self.hass.data[DOMAIN]['devices']:
                if (device['model'] == 'lumi.gateway.mgl03' and
                        device['did'] not in actions):
                    name = f"Add {device['name']} ({device['localip']})"
                    actions[device['did']] = name

        return self.async_show_form(
            step_id='user',
            data_schema=vol.Schema({
                vol.Required('action', default='cloud'): vol.In(actions)
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
            })
        )

    async def async_step_cloud(self, user_input=None, error=None):
        if user_input:
<<<<<<< HEAD
            if not user_input["servers"]:
                return await self.async_step_cloud(error="no_servers")

            session = async_create_clientsession(self.hass)
            cloud = MiCloud(session)
            if await cloud.login(
                    user_input["username"], user_input["password"]
            ):
                user_input.update(cloud.auth)
                return self.async_create_entry(
                    title=user_input["username"], data=user_input
                )

            else:
                return await self.async_step_cloud(error="cant_login")

        return self.async_show_form(
            step_id="cloud",
            data_schema=vol.Schema({
                vol.Required("username"): str,
                vol.Required("password"): str,
                vol.Required("servers", default=["cn"]):
                    cv.multi_select(SERVERS)
            }),
            errors={"base": error} if error else None
=======
            if not user_input['servers']:
                return await self.async_step_cloud(error='no_servers')

            session = async_create_clientsession(self.hass)
            cloud = MiCloud(session)
            if await cloud.login(user_input['username'],
                                 user_input['password']):
                user_input.update(cloud.auth)
                return self.async_create_entry(title=user_input['username'],
                                               data=user_input)

            else:
                return await self.async_step_cloud(error='cant_login')

        return self.async_show_form(
            step_id='cloud',
            data_schema=vol.Schema({
                vol.Required('username'): str,
                vol.Required('password'): str,
                vol.Required('servers', default=['cn']):
                    cv.multi_select(SERVERS)
            }),
            errors={'base': error} if error else None
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        )

    async def async_step_token(self, user_input=None, error=None):
        """GUI > Configuration > Integrations > Plus > Xiaomi Gateway 3"""
        if user_input is not None:
<<<<<<< HEAD
            error = await utils.check_gateway(**user_input)
            if error:
                return await self.async_step_token(error=error)

            return self.async_create_entry(
                title=user_input["host"], data=user_input
            )

        return self.async_show_form(
            step_id="token",
            data_schema=vol.Schema({
                vol.Required("host"): str,
                vol.Required("token"): str,
                vol.Required("telnet_cmd"): str,
            }),
            errors={"base": error} if error else None
=======
            error = utils.check_mgl03(**user_input)
            if error:
                return await self.async_step_token(error=error)

            return self.async_create_entry(title=user_input['host'],
                                           data=user_input)

        return self.async_show_form(
            step_id='token',
            data_schema=vol.Schema({
                vol.Required('host'): str,
                vol.Required('token'): str,
                vol.Required('telnet_cmd', default=TELNET_CMD): str,
            }),
            errors={'base': error} if error else None
        )

    async def async_step_ble(self, user_input=None):
        if user_input:
            mac = user_input['mac']
            Gateway3.defaults.setdefault(mac, {})
            Gateway3.ble_known.pop(mac)

            # reconnect all MQTT for receive device/info topic
            utils.reconnect_all_gateways(self.hass)

        return self.async_show_form(
            step_id="ble",
            data_schema=vol.Schema({
                vol.Required('mac'): vol.In(Gateway3.ble_known)
            })
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        )

    @staticmethod
    @callback
    def async_get_options_flow(entry: ConfigEntry):
        return OptionsFlowHandler(entry)


TITLE = "Xiaomi Gateway 3"

<<<<<<< HEAD
ZHA_NOTIFICATION = """For **ZHA**, goto:

Configuration > Integrations > Add Integration > Zigbee Home Automation:

- Radio Type: **EZSP**
- Path: `socket://{0}:8888`

For **zigbee2mqtt**, goto:

Supervisor > Zigbee2mqtt > Configuration:

```
serial:
  port: 'tcp://{0}:8888'
=======
ZHA_NOTIFICATION = """Please create manually

Integration: **Zigbee Home Automation**
Radio Type: **EZSP**
Path: `socket://%s:8888`
Speed: `115200`"""

Z2M_NOTIFICATION = """Add to your zigbee2mqtt config

```
serial:
  port: 'tcp://%s:8888'
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
  adapter: ezsp
```
"""


<<<<<<< HEAD
# noinspection PyUnusedLocal
=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
class OptionsFlowHandler(OptionsFlow):
    def __init__(self, entry: ConfigEntry):
        self.entry = entry

    async def async_step_init(self, user_input=None):
<<<<<<< HEAD
        if "servers" in self.entry.data:
=======
        if 'servers' in self.entry.data:
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
            return await self.async_step_cloud()
        else:
            return await self.async_step_user()

    async def async_step_cloud(self, user_input=None):
        if user_input is not None:
<<<<<<< HEAD
            did = user_input["did"]
            device = next(
                device for device in self.hass.data[DOMAIN]["devices"]
                if device["did"] == did
            )

            if device["pid"] != "6":
=======
            did = user_input['did']
            device = next(d for d in self.hass.data[DOMAIN]['devices']
                          if d['did'] == did)

            if device['pid'] != '6':
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
                device_info = (
                    f"Name: {device['name']}\n"
                    f"Model: {device['model']}\n"
                    f"IP: {device['localip']}\n"
                    f"MAC: {device['mac']}\n"
                    f"Token: {device['token']}"
                )
            else:
                bindkey = await utils.get_bindkey(
<<<<<<< HEAD
                    self.hass.data[DOMAIN]["cloud"], did
=======
                    self.hass.data[DOMAIN]['cloud'], did
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
                )
                device_info = (
                    f"Name: {device['name']}\n"
                    f"Model: {device['model']}\n"
                    f"MAC: {device['mac']}\n"
                    f"Bindkey: {bindkey}\n"
                )

<<<<<<< HEAD
            if device["model"] == "lumi.gateway.v3":
                device_info += "\nLAN key: " + await utils.get_lan_key(
                    device["localip"], device["token"]
                )
            elif ".vacuum." in device["model"]:
                device_info += "\nRooms: " + await utils.get_room_mapping(
                    self.hass.data[DOMAIN]["cloud"],
                    device["localip"], device["token"],
                )

        elif not self.hass.data[DOMAIN].get("devices"):
=======
            if device['model'] == 'lumi.gateway.v3':
                device_info += "\nLAN key: " + utils.get_lan_key(
                    device['localip'], device['token']
                )
            elif '.vacuum.' in device['model']:
                device_info += "\nRooms: " + await utils.get_room_mapping(
                    self.hass.data[DOMAIN]['cloud'],
                    device['localip'], device['token'],
                )

        elif not self.hass.data[DOMAIN].get('devices'):
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
            device_info = "No devices in account"
        else:
            device_info = "Choose a device from the list"

        devices = {}
<<<<<<< HEAD
        for device in self.hass.data[DOMAIN].get("devices", []):
            # 0 - wifi, 6 - ble, 8 - wifi+ble
            if device["pid"] in ("0", "8"):
                info = device["localip"]
            elif device["pid"] == "6":
                info = "BLE"
            else:
                continue
            devices[device["did"]] = f"{device['name']} ({info})"
=======
        for device in self.hass.data[DOMAIN].get('devices', []):
            # 0 - wifi, 6 - ble, 8 - wifi+ble
            if device['pid'] in ('0', '8'):
                info = device['localip']
            elif device['pid'] == '6':
                info = 'BLE'
            else:
                continue
            devices[device['did']] = f"{device['name']} ({info})"
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

        return self.async_show_form(
            step_id="cloud",
            data_schema=vol.Schema({
<<<<<<< HEAD
                vol.Required("did"): vol.In(devices)
            }),
            description_placeholders={
                "device_info": device_info
=======
                vol.Required('did'): vol.In(devices)
            }),
            description_placeholders={
                'device_info': device_info
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
            }
        )

    async def async_step_user(self, user_input=None):
        if user_input:
<<<<<<< HEAD
            old_mode = self.entry.options.get("zha", False)
            new_mode = user_input["zha"]
            if new_mode != old_mode:
                host = user_input["host"]

                # change zigbee firmware if needed
                if not await utils.update_zigbee_firmware(
                        self.hass, host, new_mode
                ):
                    raise Exception("Can't update zigbee firmware")

                if new_mode is True:
                    self.hass.components.persistent_notification.async_create(
                        ZHA_NOTIFICATION.format(host), TITLE
=======
            old_mode = self.entry.options.get('zha', False)
            new_mode = user_input['zha']
            if new_mode != old_mode:
                host = user_input['host']

                # change zigbee firmware if needed
                if new_mode in (False, 'z2m'):
                    ezsp_version = 8 if new_mode else 7
                    if not await utils.update_zigbee_firmware(
                            self.hass, host, ezsp_version
                    ):
                        raise Exception("Can't update zigbee firmware")

                if new_mode is True:
                    self.hass.components.persistent_notification.async_create(
                        ZHA_NOTIFICATION % host, TITLE
                    )
                elif new_mode == 'z2m':
                    self.hass.components.persistent_notification.async_create(
                        Z2M_NOTIFICATION % host, TITLE
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
                    )

            return self.async_create_entry(title='', data=user_input)

<<<<<<< HEAD
        host = self.entry.options["host"]
        token = self.entry.options["token"]
        telnet_cmd = self.entry.options.get("telnet_cmd", "")
        ble = self.entry.options.get("ble", True)
        stats = self.entry.options.get("stats", False)
        debug = self.entry.options.get("debug", [])
        buzzer = self.entry.options.get("buzzer", False)
        memory = self.entry.options.get("memory", False)
        zha = self.entry.options.get("zha", False)

        # filter only supported items
        debug = [k for k in debug if k in OPT_DEBUG]
=======
        host = self.entry.options['host']
        token = self.entry.options['token']
        telnet_cmd = self.entry.options.get('telnet_cmd', '')
        ble = self.entry.options.get('ble', True)
        stats = self.entry.options.get('stats', False)
        debug = self.entry.options.get('debug', [])
        buzzer = self.entry.options.get('buzzer', False)
        parent = self.entry.options.get('parent', -1)
        zha = self.entry.options.get('zha', False)
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
<<<<<<< HEAD
                vol.Required("host", default=host): str,
                vol.Required("token", default=token): str,
                vol.Optional("telnet_cmd", default=telnet_cmd): str,
                vol.Required("ble", default=ble): bool,
                vol.Optional("stats", default=stats): bool,
                vol.Optional("debug", default=debug):
                    cv.multi_select(OPT_DEBUG),
                vol.Optional("buzzer", default=buzzer): bool,
                vol.Optional("memory", default=memory): bool,
                vol.Optional("zha", default=zha): bool,
=======
                vol.Required('host', default=host): str,
                vol.Required('token', default=token): str,
                vol.Optional('telnet_cmd', default=telnet_cmd): str,
                vol.Required('ble', default=ble): bool,
                vol.Required('stats', default=stats): bool,
                vol.Optional('debug', default=debug):
                    cv.multi_select(OPT_DEBUG),
                vol.Optional('buzzer', default=buzzer): bool,
                vol.Optional('parent', default=parent): vol.In(OPT_PARENT),
                vol.Required('zha', default=zha): vol.In(OPT_MODE),
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
            }),
        )
