"""Starting setup task: clear storage."""
from __future__ import annotations

import os

from homeassistant.core import HomeAssistant

from ..base import HacsBase
from ..enums import HacsStage
from .base import HacsTask


async def async_setup_task(hacs: HacsBase, hass: HomeAssistant) -> Task:
    """Set up this task."""
    return Task(hacs=hacs, hass=hass)


class Task(HacsTask):
    """Clear old files from storage."""

    stages = [HacsStage.SETUP]

    def execute(self) -> None:
<<<<<<< HEAD
        """Execute the task."""
        for storage_file in ("hacs",):
            path = f"{self.hacs.core.config_path}/.storage/{storage_file}"
            if os.path.isfile(path):
                self.task_logger(self.hacs.log.info, f"Cleaning up old storage file: {path}")
=======
        for storage_file in ("hacs",):
            path = f"{self.hacs.core.config_path}/.storage/{storage_file}"
            if os.path.isfile(path):
                self.log.info("Cleaning up old storage file: %s", path)
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
                os.remove(path)
