<<<<<<< HEAD
"""Base class for validation."""
from __future__ import annotations

from time import monotonic
from typing import TYPE_CHECKING

from ..exceptions import HacsException

if TYPE_CHECKING:
    from ..repositories.base import HacsRepository


class ValidationException(HacsException):
    """Raise when there is a validation issue."""


class ValidationBase:
    """Base class for validation."""

    action_only: bool = False
    category: str = "common"

    def __init__(self, repository: HacsRepository) -> None:
        self.hacs = repository.hacs
        self.repository = repository
        self.failed = False

    @property
    def slug(self) -> str:
        """Return the check slug."""
        return self.__class__.__module__.rsplit(".", maxsplit=1)[-1]

    async def execute_validation(self, *_, **__) -> None:
        """Execute the task defined in subclass."""
        self.hacs.log.debug("Validation<%s> Starting validation", self.slug)

        start_time = monotonic()
        self.failed = False

        try:
            if task := getattr(self, "validate", None):
                await self.hacs.hass.async_add_executor_job(task)
            elif task := getattr(self, "async_validate", None):
                await task()  # pylint: disable=not-callable
        except ValidationException as exception:
            self.failed = True
            self.hacs.log.error("Validation<%s> failed:  %s", self.slug, exception)

        else:
            self.hacs.log.debug(
                "Validation<%s> took %.3f seconds to complete", self.slug, monotonic() - start_time
            )


class ActionValidationBase(ValidationBase):
    """Base class for action validation."""

    action_only = True
=======
from custom_components.hacs.share import SHARE, get_hacs


class ValidationException(Exception):
    pass


class ValidationBase:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.hacs = get_hacs()
        self.failed = False
        self.logger = repository.logger

    def __init_subclass__(cls, category="common", **kwargs) -> None:
        """Initialize a subclass, register if possible."""
        super().__init_subclass__(**kwargs)
        if SHARE["rules"].get(category) is None:
            SHARE["rules"][category] = []
        if cls not in SHARE["rules"][category]:
            SHARE["rules"][category].append(cls)

    @property
    def action_only(self):
        return False

    async def _async_run_check(self):
        """DO NOT OVERRIDE THIS IN SUBCLASSES!"""
        if self.hacs.system.action:
            self.logger.info(f"Running check '{self.__class__.__name__}'")
        try:
            await self.hacs.hass.async_add_executor_job(self.check)
            await self.async_check()
        except ValidationException as exception:
            self.failed = True
            self.logger.error(exception)

    def check(self):
        pass

    async def async_check(self):
        pass


class ActionValidationBase(ValidationBase):
    @property
    def action_only(self):
        return True
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
