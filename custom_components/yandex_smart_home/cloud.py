"""Implement the Yandex Smart Home cloud connection manager."""
from __future__ import annotations

from asyncio import TimeoutError
from dataclasses import dataclass
<<<<<<< HEAD
from datetime import datetime, timedelta
=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
from http import HTTPStatus
import json
import logging
from typing import Any

from aiohttp import (
    ClientConnectorError,
    ClientResponseError,
    ClientSession,
    ClientWebSocketResponse,
    WSMessage,
    WSMsgType,
)
from homeassistant.config_entries import ConfigEntry
<<<<<<< HEAD
from homeassistant.core import HassJob, HomeAssistant
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.json import JSONEncoder
from homeassistant.util import dt

from . import const
from .const import CLOUD_BASE_URL, CONFIG, DOMAIN
=======
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.json import JSONEncoder

from . import const
from .const import CONFIG, DOMAIN
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
from .helpers import Config, RequestData
from .smart_home import async_handle_message

_LOGGER = logging.getLogger(__name__)

DEFAULT_RECONNECTION_DELAY = 2
MAX_RECONNECTION_DELAY = 180
<<<<<<< HEAD
FAST_RECONNECTION_TIME = timedelta(seconds=6)
FAST_RECONNECTION_THRESHOLD = 5
BASE_API_URL = f'{CLOUD_BASE_URL}/api/home_assistant/v1'
=======
BASE_API_URL = 'https://yaha-cloud.ru/api/home_assistant/v1'
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1


@dataclass
class CloudInstanceData:
    id: str
    password: str
    connection_token: str


@dataclass
class CloudRequest:
    request_id: str
    action: str
    message: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        if 'message' in data:
<<<<<<< HEAD
            if isinstance(data['message'], str):
                data['message'] = json.loads(data['message'])
=======
            data['message'] = json.loads(data['message'])
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        else:
            data['message'] = {}

        return cls(**data)


class CloudManager:
    def __init__(self, hass: HomeAssistant, config: Config, session: ClientSession):
        self._hass = hass
        self._instance_id = config.cloud_instance_id
        self._token = config.cloud_connection_token
        self._user_id = config.user_id
        self._session = session
<<<<<<< HEAD
        self._last_connection_at: datetime | None = None
        self._fast_reconnection_count = 0
=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        self._ws: ClientWebSocketResponse | None = None
        self._ws_reconnect_delay = DEFAULT_RECONNECTION_DELAY
        self._ws_active = True

        self._url = f'{BASE_API_URL}/connect'

    async def connect(self, *_):
        if not self._ws_active:
            return

        # noinspection PyBroadException
        try:
            _LOGGER.debug(f'Connecting to {self._url}')
<<<<<<< HEAD
            self._ws = await self._session.ws_connect(self._url, heartbeat=45, compress=15, headers={
=======
            self._ws = await self._session.ws_connect(self._url, heartbeat=45, headers={
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
                'Authorization': f'Bearer {self._token}'
            })

            _LOGGER.debug('Connection to Yandex Smart Home cloud established')
            self._ws_reconnect_delay = DEFAULT_RECONNECTION_DELAY
<<<<<<< HEAD
            self._last_connection_at = dt.utcnow()
=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

            async for msg in self._ws:  # type: WSMessage
                if msg.type == WSMsgType.TEXT:
                    await self._on_message(msg.json())

            _LOGGER.debug(f'Disconnected: {self._ws.close_code}')
            if self._ws.close_code is not None:
                self._try_reconnect()
        except (ClientConnectorError, ClientResponseError, TimeoutError):
            _LOGGER.exception('Failed to connect to Yandex Smart Home cloud')
            self._try_reconnect()
        except Exception:
            _LOGGER.exception('Unexpected exception')
            self._try_reconnect()

    async def disconnect(self, *_):
        self._ws_active = False

        if self._ws:
            await self._ws.close()

    async def _on_message(self, payload: dict[Any, Any]):
        request = CloudRequest.from_dict(payload)
        _LOGGER.debug('Request: %s (message: %s)' % (request.action, request.message))

        data = RequestData(
            config=self._hass.data[DOMAIN][CONFIG],
            request_user_id=self._instance_id,
            request_id=request.request_id,
            user_id=self._user_id
        )

        result = await async_handle_message(self._hass, data, request.action, request.message)
        response = json.dumps(result, cls=JSONEncoder)
        _LOGGER.debug(f'Response: {response}')

        await self._ws.send_str(response)

    def _try_reconnect(self):
        self._ws_reconnect_delay = min(2 * self._ws_reconnect_delay, MAX_RECONNECTION_DELAY)
<<<<<<< HEAD

        if self._last_connection_at and self._last_connection_at + FAST_RECONNECTION_TIME > dt.utcnow():
            self._fast_reconnection_count += 1
        else:
            self._fast_reconnection_count = 0

        if self._fast_reconnection_count >= FAST_RECONNECTION_THRESHOLD:
            self._ws_reconnect_delay = MAX_RECONNECTION_DELAY
            _LOGGER.warning(f'Reconnecting too fast, next reconnection in {self._ws_reconnect_delay} seconds')

        _LOGGER.debug(f'Trying to reconnect in {self._ws_reconnect_delay} seconds')
        async_call_later(self._hass, self._ws_reconnect_delay, HassJob(self.connect))
=======
        _LOGGER.debug(f'Trying to reconnect in {self._ws_reconnect_delay} seconds')
        async_call_later(self._hass, self._ws_reconnect_delay, self.connect)
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1


async def register_cloud_instance(hass: HomeAssistant) -> CloudInstanceData:
    session = async_create_clientsession(hass)

    response = await session.post(f'{BASE_API_URL}/instance/register')
    response.raise_for_status()

    return CloudInstanceData(**await response.json())


async def delete_cloud_instance(hass: HomeAssistant, entry: ConfigEntry):
    session = async_create_clientsession(hass)

    instance_id = entry.data[const.CONF_CLOUD_INSTANCE][const.CONF_CLOUD_INSTANCE_ID]
    token = entry.data[const.CONF_CLOUD_INSTANCE][const.CONF_CLOUD_INSTANCE_CONNECTION_TOKEN]

    response = await session.delete(f'{BASE_API_URL}/instance/{instance_id}', headers={
        'Authorization': f'Bearer {token}'
    })
    if response.status != HTTPStatus.OK:
        _LOGGER.error(f'Failed to delete cloud instance, status code: {response.status}')
