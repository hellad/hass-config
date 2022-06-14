"""Hacs task manager."""
from __future__ import annotations

import asyncio
from importlib import import_module
from pathlib import Path

from homeassistant.core import HomeAssistant

from ..base import HacsBase
<<<<<<< HEAD
from .base import HacsTask


class HacsTaskManager:
=======
from ..mixin import LogMixin
from .base import HacsTask


class HacsTaskManager(LogMixin):
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    """Hacs task manager."""

    def __init__(self, hacs: HacsBase, hass: HomeAssistant) -> None:
        """Initialize the setup manager class."""
        self.hacs = hacs
        self.hass = hass
        self.__tasks: dict[str, HacsTask] = {}

    @property
    def tasks(self) -> list[HacsTask]:
        """Return all list of all tasks."""
        return list(self.__tasks.values())

    async def async_load(self) -> None:
        """Load all tasks."""
        task_files = Path(__file__).parent
        task_modules = (
            module.stem
            for module in task_files.glob("*.py")
            if module.name not in ("base.py", "__init__.py", "manager.py")
        )

        async def _load_module(module: str):
            task_module = import_module(f"{__package__}.{module}")
            if task := await task_module.async_setup_task(hacs=self.hacs, hass=self.hass):
                self.__tasks[task.slug] = task

        await asyncio.gather(*[_load_module(task) for task in task_modules])
<<<<<<< HEAD
        self.hacs.log.info("Loaded %s tasks", len(self.tasks))
=======
        self.log.info("Loaded %s tasks", len(self.tasks))
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

        schedule_tasks = len(self.hacs.recuring_tasks) == 0

        for task in self.tasks:
            if task.events is not None:
                for event in task.events:
                    self.hass.bus.async_listen_once(event, task.execute_task)

            if task.schedule is not None and schedule_tasks:
<<<<<<< HEAD
                self.hacs.log.debug(
                    "Scheduling <HacsTask %s> to run every %s", task.slug, task.schedule
                )
=======
                self.log.debug("Scheduling the %s task to run every %s", task.slug, task.schedule)
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
                self.hacs.recuring_tasks.append(
                    self.hacs.hass.helpers.event.async_track_time_interval(
                        task.execute_task, task.schedule
                    )
                )

    def get(self, slug: str) -> HacsTask | None:
        """Return a task."""
        return self.__tasks.get(slug)

    async def async_execute_runtume_tasks(self) -> None:
        """Execute the the execute methods of each runtime task if the stage matches."""
<<<<<<< HEAD
=======
        self.hacs.status.background_task = True
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        await asyncio.gather(
            *(
                task.execute_task()
                for task in self.tasks
                if task.stages is not None and self.hacs.stage in task.stages
            )
        )
<<<<<<< HEAD
=======
        self.hacs.status.background_task = False
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
