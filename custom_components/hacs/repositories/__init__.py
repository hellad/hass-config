"""Initialize repositories."""
<<<<<<< HEAD
from __future__ import annotations

from ..enums import HacsCategory
from .appdaemon import HacsAppdaemonRepository
from .base import HacsRepository
from .integration import HacsIntegrationRepository
from .netdaemon import HacsNetdaemonRepository
from .plugin import HacsPluginRepository
from .python_script import HacsPythonScriptRepository
from .theme import HacsThemeRepository

RERPOSITORY_CLASSES: dict[HacsCategory, HacsRepository] = {
    HacsCategory.THEME: HacsThemeRepository,
    HacsCategory.INTEGRATION: HacsIntegrationRepository,
    HacsCategory.PYTHON_SCRIPT: HacsPythonScriptRepository,
    HacsCategory.APPDAEMON: HacsAppdaemonRepository,
    HacsCategory.NETDAEMON: HacsNetdaemonRepository,
    HacsCategory.PLUGIN: HacsPluginRepository,
=======
from custom_components.hacs.repositories.appdaemon import HacsAppdaemonRepository
from custom_components.hacs.repositories.integration import HacsIntegrationRepository
from custom_components.hacs.repositories.netdaemon import HacsNetdaemonRepository
from custom_components.hacs.repositories.plugin import HacsPluginRepository
from custom_components.hacs.repositories.python_script import HacsPythonScriptRepository
from custom_components.hacs.repositories.theme import HacsThemeRepository

RERPOSITORY_CLASSES = {
    "theme": HacsThemeRepository,
    "integration": HacsIntegrationRepository,
    "python_script": HacsPythonScriptRepository,
    "appdaemon": HacsAppdaemonRepository,
    "netdaemon": HacsNetdaemonRepository,
    "plugin": HacsPluginRepository,
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
}
