import asyncio
import logging

from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import Event
from homeassistant.helpers import intent
from homeassistant.helpers.typing import HomeAssistantType

<<<<<<< HEAD
=======
from . import utils

>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
_LOGGER = logging.getLogger(__name__)

DOMAIN = 'yandex_dialogs'

CONF_USER_IDS = 'user_ids'


async def async_setup(hass: HomeAssistantType, hass_config: dict):
<<<<<<< HEAD
    if DOMAIN in hass_config and not hass.config_entries.async_entries(DOMAIN):
=======
    if DOMAIN in hass_config:
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        hass.async_create_task(hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_IMPORT}
        ))
    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    user_ids = entry.options.get(CONF_USER_IDS, [])

    if DOMAIN in hass.data:
        dialog: YandexDialog = hass.data[DOMAIN]
        dialog.user_ids = user_ids
        return True

    hass.data[DOMAIN] = dialog = YandexDialog(hass, user_ids)
    hass.http.register_view(dialog)

    async def listener(event: Event):
<<<<<<< HEAD
        dialog.response = event.data
=======
        dialog.response_text = event.data.get('text')
        dialog.response_end_session = event.data.get('end_session')
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        dialog.response_waiter.set()

    hass.bus.async_listen('yandex_intent_response', listener)

    # add options handler
    if not entry.update_listeners:
        entry.add_update_listener(async_update_options)

    return True


async def async_update_options(hass: HomeAssistantType, entry):
    await hass.config_entries.async_reload(entry.entry_id)


<<<<<<< HEAD
# noinspection PyUnusedLocal
=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
async def async_unload_entry(hass: HomeAssistantType, entry):
    return True


class YandexDialog(HomeAssistantView):
    url = '/api/yandex_dialogs'
    name = 'api:yandex_dialogs'
    requires_auth = False

<<<<<<< HEAD
    dialogs: dict = {}
    response: dict = {}
=======
    response_text = None
    response_end_session = None
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    response_waiter = asyncio.Event()

    def __init__(self, hass: HomeAssistantType, user_ids: list):
        self.hass = hass
        self.user_ids = user_ids

    @staticmethod
<<<<<<< HEAD
    def empty(text=""):
        return web.json_response({
            "response": {"text": text, "end_session": True},
            "version": "1.0"
        })

    @staticmethod
    def web_response(text="", end_session=True, **kwargs):
        data = {
            "response": {"text": text, "end_session": end_session},
            "version": "1.0"
        }

        if "tts" in kwargs:
            # text should be not empty of tts won't work
            if not text:
                data["response"]["text"] = "-"
            data["response"]["tts"] = kwargs["tts"]

        if "session" in kwargs:
            data["session_state"] = kwargs["session"]
        if "user" in kwargs:
            data["user_state_update"] = kwargs["user"]
        if "application" in kwargs:
            data["application_state"] = kwargs["application"]

        _LOGGER.debug(data)

        return web.json_response(data)

=======
    def empty(text='', end_session=False):
        return web.json_response({
            'response': {'text': text, 'end_session': end_session},
            'version': '1.0'
        })

>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    async def post(self, request: web.Request) -> web.Response:
        data = None

        try:
            data = await request.json()

            _LOGGER.debug(data)

<<<<<<< HEAD
            request = data["request"]
            command: str = request["command"]
            if command == "ping":
                return self.empty(text="pong")

            user_id = data["session"]["user"]["user_id"]
            if user_id not in self.user_ids:
                _LOGGER.debug("Unknown user: " + user_id)
                return self.empty()

            # sometimes we not exit from skill and receive new request
            if request["original_utterance"].startswith("СКАЖИ НАВЫКУ"):
                command = request["nlu"]["tokens"][-1]

            if command in self.dialogs:
                response = self.dialogs.pop(command)
                return self.web_response(**response)

            event_data = {
=======
            request = data['request']
            if request['command'] == 'ping':
                return self.empty(text='pong')

            if 'user' not in data['session']:
                return self.empty()

            user_id = data['session']['user']['user_id']
            if user_id not in self.user_ids:
                if request['command'] == 'привет':
                    self.hass.components.persistent_notification.async_create(
                        f"Новый пользователь: `{user_id}`",
                        title="Yandex Dialogs")
                    return self.empty(text="Умный дом на связи")

                else:
                    return self.empty(text="Я тебя не знаю")

            slots = {
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
                'text': request['original_utterance'],
                'command': request['command'],
            }

<<<<<<< HEAD
            if "state" in data:
                # skip empty state because compare any with empty is True
                for k in ("session", "user", "application"):
                    if data["state"][k]:
                        event_data[k] = data["state"][k]

            intents = request['nlu'].get('intents')
            if intents:
                event_data['intent'] = intent_type = next(iter(intents))
                for k, v in intents[intent_type]['slots'].items():
                    event_data[k] = v['value']
=======
            intents = data['request']['nlu'].get('intents')
            if intents:
                slots['intent'] = intent_type = next(iter(intents))
                for k, v in intents[intent_type]['slots'].items():
                    slots[k] = v['value']
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

            else:
                intent_type = 'yandex_default'

<<<<<<< HEAD
            _LOGGER.debug(f"Request: {event_data}")

            self.response.clear()

            # by default won't exit dialog on empty input
            if data["session"]["new"] and request["command"] == "":
                self.response["end_session"] = False

            try:
                if intent_type in self.hass.data.get('intent', ""):
                    # run intent if exists
                    slots = {k: {'value': v} for k, v in event_data.items()}
                    resp = await intent.async_handle(
                        self.hass, DOMAIN, intent_type, slots,
                        request['original_utterance']
                    )
                    if resp.speech:
                        self.response["text"] = resp.speech['plain']['speech']

                else:
                    self.response_waiter.clear()
                    self.hass.bus.async_fire('yandex_intent', event_data)
                    await asyncio.wait_for(self.response_waiter.wait(), 2.0)

            except:
                pass

            return self.web_response(**self.response)

        except:
            _LOGGER.exception(f"Yandex Dialog {data}")
            return self.empty()
=======
            _LOGGER.debug(f"Request: {slots}")

            self.response_text = None
            self.response_end_session = None

            try:
                if intent_type in self.hass.data.get('intent', {}):
                    # run intent if exists
                    slots = {k: {'value': v} for k, v in slots.items()}
                    response = await intent.async_handle(
                        self.hass, DOMAIN, intent_type, slots,
                        request['original_utterance'])
                    if self.response_text:
                        text = self.response_text
                    elif response.speech:
                        text = response.speech['plain']['speech']
                    else:
                        text = ''

                else:
                    self.response_waiter.clear()
                    self.hass.bus.async_fire('yandex_intent', slots)
                    await asyncio.wait_for(self.response_waiter.wait(), 2.0)
                    text = self.response_text

            except:
                text = ''

            if self.response_end_session is not None:
                end_session = self.response_end_session
            else:
                end_session = (data['session']['new'] and
                               request['command'] != '')

            _LOGGER.debug(f"Response: {text}, end_session: {end_session}")

            return web.json_response({
                'response': {
                    'text': text,
                    'end_session': end_session
                },
                'version': '1.0'
            })

        except:
            _LOGGER.exception(f"Yandex Dialog {data}")
            return self.empty(end_session=True)
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
