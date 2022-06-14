""""Store HACS data."""
from __future__ import annotations

from homeassistant.const import EVENT_HOMEASSISTANT_FINAL_WRITE
from homeassistant.core import HomeAssistant

from ..base import HacsBase
from .base import HacsTask


async def async_setup_task(hacs: HacsBase, hass: HomeAssistant) -> Task:
    """Set up this task."""
    return Task(hacs=hacs, hass=hass)


class Task(HacsTask):
    """ "Hacs task base."""

    events = [EVENT_HOMEASSISTANT_FINAL_WRITE]
<<<<<<< HEAD
    _can_run_disabled = True

    async def async_execute(self) -> None:
        """Execute the task."""
        await self.hacs.data.async_write(force=True)
=======

    async def async_execute(self) -> None:
        await self.hacs.data.async_write()
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
