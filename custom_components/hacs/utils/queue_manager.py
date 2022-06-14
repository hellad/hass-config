"""The QueueManager class."""
<<<<<<< HEAD
from __future__ import annotations

import asyncio
import time
from typing import Coroutine

from homeassistant.core import HomeAssistant

from ..exceptions import HacsExecutionStillInProgress
from .logger import get_hacs_logger

_LOGGER = get_hacs_logger()
=======

import asyncio
import time

from ..exceptions import HacsExecutionStillInProgress
from .logger import getLogger

_LOGGER = getLogger()
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1


class QueueManager:
    """The QueueManager class."""

<<<<<<< HEAD
    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self.queue: list[Coroutine] = []
        self.running = False
=======
    running = False
    queue = []
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

    @property
    def pending_tasks(self) -> int:
        """Return a count of pending tasks in the queue."""
        return len(self.queue)

    @property
    def has_pending_tasks(self) -> bool:
        """Return a count of pending tasks in the queue."""
        return self.pending_tasks != 0

    def clear(self) -> None:
        """Clear the queue."""
        self.queue = []

<<<<<<< HEAD
    def add(self, task: Coroutine) -> None:
        """Add a task to the queue."""
        self.queue.append(task)

    async def execute(self, number_of_tasks: int | None = None) -> None:
        """Execute the tasks in the queue."""
        if self.running:
            _LOGGER.debug("<QueueManager> Execution is allreay running")
            raise HacsExecutionStillInProgress
        if len(self.queue) == 0:
            _LOGGER.debug("<QueueManager> The queue is empty")
=======
    def add(self, task) -> None:
        """Add a task to the queue."""
        self.queue.append(task)

    async def execute(self, number_of_tasks=None) -> None:
        """Execute the tasks in the queue."""
        if self.running:
            _LOGGER.debug("Execution is allreay running")
            raise HacsExecutionStillInProgress
        if len(self.queue) == 0:
            _LOGGER.debug("The queue is empty")
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
            return

        self.running = True

<<<<<<< HEAD
        _LOGGER.debug("<QueueManager> Checking out tasks to execute")
=======
        _LOGGER.debug("Checking out tasks to execute")
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        local_queue = []

        if number_of_tasks:
            for task in self.queue[:number_of_tasks]:
                local_queue.append(task)
        else:
            for task in self.queue:
                local_queue.append(task)

        for task in local_queue:
            self.queue.remove(task)

<<<<<<< HEAD
        _LOGGER.debug("<QueueManager> Starting queue execution for %s tasks", len(local_queue))
=======
        _LOGGER.debug("Starting queue execution for %s tasks", len(local_queue))
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        start = time.time()
        await asyncio.gather(*local_queue)
        end = time.time() - start

        _LOGGER.debug(
<<<<<<< HEAD
            "<QueueManager> Queue execution finished for %s tasks finished in %.2f seconds",
=======
            "Queue execution finished for %s tasks finished in %.2f seconds",
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
            len(local_queue),
            end,
        )
        if self.has_pending_tasks:
<<<<<<< HEAD
            _LOGGER.debug("<QueueManager> %s tasks remaining in the queue", len(self.queue))
=======
            _LOGGER.debug("%s tasks remaining in the queue", len(self.queue))
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        self.running = False
