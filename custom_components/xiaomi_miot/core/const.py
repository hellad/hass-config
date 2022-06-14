<<<<<<< HEAD
from enum import Enum

=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
from .device_customizes import DEVICE_CUSTOMIZES
from .miot_local_devices import MIOT_LOCAL_MODELS  # noqa
from .translation_languages import TRANSLATION_LANGUAGES  # noqa

DOMAIN = 'xiaomi_miot'
DEFAULT_NAME = 'Xiaomi Miot'

CONF_MODEL = 'model'
CONF_XIAOMI_CLOUD = 'xiaomi_cloud'
CONF_SERVER_COUNTRY = 'server_country'
CONF_CONN_MODE = 'conn_mode'
CONF_CONFIG_VERSION = 'config_version'

DEFAULT_CONN_MODE = 'cloud'

SUPPORTED_DOMAINS = [
    'sensor',
    'binary_sensor',
    'switch',
    'light',
    'fan',
    'climate',
    'cover',
    'humidifier',
    'media_player',
    'camera',
    'vacuum',
    'water_heater',
    'device_tracker',
    'remote',
<<<<<<< HEAD
    'alarm_control_panel',
]

CLOUD_SERVERS = {
    'cn': '中国大陆',
    'tw': '中國台灣',
    'de': 'Europe',
    'i2': 'India',
    'ru': 'Russia',
    'sg': 'Singapore',
    'us': 'United States',
}

try:
    # hass 2020.12.2
    from homeassistant.components.number import DOMAIN as DOMAIN_NUMBER
    SUPPORTED_DOMAINS.append(DOMAIN_NUMBER)
except (ModuleNotFoundError, ImportError):
    DOMAIN_NUMBER = None

try:
    # hass 2021.6
=======
    'number',
    'alarm_control_panel',
]

try:
    # hass 2021.6.0b0+
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    from homeassistant.components.sensor import STATE_CLASS_MEASUREMENT
except (ModuleNotFoundError, ImportError):
    STATE_CLASS_MEASUREMENT = None

try:
<<<<<<< HEAD
    # hass 2021.7
=======
    # hass 2021.7.0b0+
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    from homeassistant.components.select import DOMAIN as DOMAIN_SELECT
    SUPPORTED_DOMAINS.append(DOMAIN_SELECT)
except (ModuleNotFoundError, ImportError):
    DOMAIN_SELECT = None

try:
<<<<<<< HEAD
    # hass 2021.9
=======
    # hass 2021.9.0b0+
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    from homeassistant.components.sensor import STATE_CLASS_TOTAL_INCREASING
except (ModuleNotFoundError, ImportError):
    STATE_CLASS_TOTAL_INCREASING = None

try:
<<<<<<< HEAD
    # hass 2021.12
    from homeassistant.components.button import DOMAIN as DOMAIN_BUTTON
    SUPPORTED_DOMAINS.append(DOMAIN_BUTTON)
except (ModuleNotFoundError, ImportError):
    DOMAIN_BUTTON = None

try:
    # hass 2022.12
    from homeassistant.helpers.entity import EntityCategory
    ENTITY_CATEGORY_VIA_ENUM = True
except (ModuleNotFoundError, ImportError):
    class EntityCategory(Enum):
        CONFIG = 'config'
        DIAGNOSTIC = 'diagnostic'
        SYSTEM = 'system'
    ENTITY_CATEGORY_VIA_ENUM = False
=======
    # hass 2021.11.0b0+
    from homeassistant.const import ENTITY_CATEGORY_CONFIG, ENTITY_CATEGORY_DIAGNOSTIC
except (ModuleNotFoundError, ImportError):
    ENTITY_CATEGORY_CONFIG = None
    ENTITY_CATEGORY_DIAGNOSTIC = None
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1


GLOBAL_CUSTOMIZES = {
    'models': DEVICE_CUSTOMIZES,
}
