"""HACS Decorators."""
<<<<<<< HEAD
from __future__ import annotations

import asyncio
from functools import wraps
from typing import TYPE_CHECKING, Any, Coroutine

from ..const import DEFAULT_CONCURRENT_BACKOFF_TIME, DEFAULT_CONCURRENT_TASKS

if TYPE_CHECKING:
    from ..base import HacsBase


def concurrent(
    concurrenttasks: int = DEFAULT_CONCURRENT_TASKS,
    backoff_time=DEFAULT_CONCURRENT_BACKOFF_TIME,
) -> Coroutine[Any, Any, None]:
=======
import asyncio
from functools import wraps
from typing import Any, Coroutine


def concurrent(concurrenttasks=15, sleepafter=0) -> Coroutine[Any, Any, None]:
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    """Return a modified function."""

    max_concurrent = asyncio.Semaphore(concurrenttasks)

    def inner_function(function) -> Coroutine[Any, Any, None]:
<<<<<<< HEAD
        @wraps(function)
        async def wrapper(*args, **kwargs) -> None:
            hacs: HacsBase = getattr(args[0], "hacs", None)

            async with max_concurrent:
                result = await function(*args, **kwargs)
                if (
                    hacs is None
                    or hacs.queue is None
                    or hacs.queue.has_pending_tasks
                    or "update" not in function.__name__
                ):
                    await asyncio.sleep(backoff_time)

                return result
=======
        if not asyncio.iscoroutinefunction(function):
            print("Is not a coroutine")
            return function

        @wraps(function)
        async def wrapper(*args) -> None:

            async with max_concurrent:
                await function(*args)
                await asyncio.sleep(sleepafter)
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

        return wrapper

    return inner_function
