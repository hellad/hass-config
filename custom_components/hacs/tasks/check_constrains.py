""""Starting setup task: Constrains"."""
from __future__ import annotations

import os

from homeassistant.core import HomeAssistant

from ..base import HacsBase
from ..const import MINIMUM_HA_VERSION
from ..enums import HacsDisabledReason, HacsStage
<<<<<<< HEAD
from ..utils.version import version_left_higher_or_equal_then_right
=======
from ..utils.version import version_left_higher_then_right
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
from .base import HacsTask


async def async_setup_task(hacs: HacsBase, hass: HomeAssistant) -> Task:
    """Set up this task."""
    return Task(hacs=hacs, hass=hass)


class Task(HacsTask):
    """Check env Constrains."""

    stages = [HacsStage.SETUP]

    def execute(self) -> None:
<<<<<<< HEAD
        """Execute the task."""
=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        for location in (
            self.hass.config.path("custom_components/custom_updater.py"),
            self.hass.config.path("custom_components/custom_updater/__init__.py"),
        ):
            if os.path.exists(location):
<<<<<<< HEAD
                self.task_logger(
                    self.hacs.log.critical,
                    "This cannot be used with custom_updater. "
                    f"To use this you need to remove custom_updater form {location}",
                )

                self.hacs.disable_hacs(HacsDisabledReason.CONSTRAINS)

        if not version_left_higher_or_equal_then_right(
            self.hacs.core.ha_version.string,
            MINIMUM_HA_VERSION,
        ):
            self.task_logger(
                self.hacs.log.critical,
                f"You need HA version {MINIMUM_HA_VERSION} or newer to use this integration.",
=======
                self.log.critical(
                    "This cannot be used with custom_updater. "
                    "To use this you need to remove custom_updater form %s",
                    location,
                )
                self.hacs.disable_hacs(HacsDisabledReason.CONSTRAINS)

        if not version_left_higher_then_right(self.hacs.core.ha_version, MINIMUM_HA_VERSION):
            self.log.critical(
                "You need HA version %s or newer to use this integration.",
                MINIMUM_HA_VERSION,
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
            )
            self.hacs.disable_hacs(HacsDisabledReason.CONSTRAINS)
