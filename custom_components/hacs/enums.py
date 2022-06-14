"""Helper constants."""
# pylint: disable=missing-class-docstring
from enum import Enum


<<<<<<< HEAD
class HacsGitHubRepo(str, Enum):
    """HacsGitHubRepo."""

    DEFAULT = "hacs/default"
    INTEGRATION = "hacs/integration"


=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
class HacsCategory(str, Enum):
    APPDAEMON = "appdaemon"
    INTEGRATION = "integration"
    LOVELACE = "lovelace"
    PLUGIN = "plugin"  # Kept for legacy purposes
    NETDAEMON = "netdaemon"
    PYTHON_SCRIPT = "python_script"
    THEME = "theme"
    REMOVED = "removed"

    def __str__(self):
        return str(self.value)


<<<<<<< HEAD
class RepositoryFile(str, Enum):
    """Repository file names."""

    HACS_JSON = "hacs.json"
    MAINIFEST_JSON = "manifest.json"


=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
class ConfigurationType(str, Enum):
    YAML = "yaml"
    CONFIG_ENTRY = "config_entry"


class LovelaceMode(str, Enum):
    """Lovelace Modes."""

    STORAGE = "storage"
    AUTO = "auto"
    AUTO_GEN = "auto-gen"
    YAML = "yaml"


class HacsStage(str, Enum):
    SETUP = "setup"
    STARTUP = "startup"
    WAITING = "waiting"
    RUNNING = "running"
    BACKGROUND = "background"


<<<<<<< HEAD
=======
class HacsSetupTask(str, Enum):
    WEBSOCKET = "WebSocket API"
    FRONTEND = "Frontend"
    SENSOR = "Sensor"
    HACS_REPO = "Hacs Repository"
    CATEGORIES = "Additional categories"
    CLEAR_STORAGE = "Clear storage"


>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
class HacsDisabledReason(str, Enum):
    RATE_LIMIT = "rate_limit"
    REMOVED = "removed"
    INVALID_TOKEN = "invalid_token"
    CONSTRAINS = "constrains"
    LOAD_HACS = "load_hacs"
    RESTORE = "restore"
