"""Starting setup task: load HACS repository."""
from __future__ import annotations

from homeassistant.core import HomeAssistant

from ..base import HacsBase
<<<<<<< HEAD
from ..enums import HacsCategory, HacsDisabledReason, HacsGitHubRepo, HacsStage
from ..exceptions import HacsException
=======
from ..enums import HacsDisabledReason, HacsStage
from ..exceptions import HacsException
from ..helpers.functions.register_repository import register_repository
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
from .base import HacsTask


async def async_setup_task(hacs: HacsBase, hass: HomeAssistant) -> Task:
    """Set up this task."""
    return Task(hacs=hacs, hass=hass)


class Task(HacsTask):
    """Load HACS repositroy."""

    stages = [HacsStage.STARTUP]

    async def async_execute(self) -> None:
<<<<<<< HEAD
        """Execute the task."""
        try:
            repository = self.hacs.repositories.get_by_full_name(HacsGitHubRepo.INTEGRATION)
            if repository is None:
                await self.hacs.async_register_repository(
                    repository_full_name=HacsGitHubRepo.INTEGRATION,
                    category=HacsCategory.INTEGRATION,
                    default=True,
                )
                repository = self.hacs.repositories.get_by_full_name(HacsGitHubRepo.INTEGRATION)
            if repository is None:
                raise HacsException("Unknown error")

            repository.data.installed = True
            repository.data.installed_version = self.hacs.integration.version
            repository.data.new = False
            repository.data.releases = True

            self.hacs.repository = repository.repository_object
            self.hacs.repositories.mark_default(repository)
        except HacsException as exception:
            if "403" in f"{exception}":
                self.task_logger(
                    self.hacs.log.critical,
                    "GitHub API is ratelimited, or the token is wrong.",
                )
            else:
                self.task_logger(self.hacs.log.critical, f"[{exception}] - Could not load HACS!")
=======
        try:
            repository = self.hacs.get_by_name("hacs/integration")
            if repository is None:
                await register_repository("hacs/integration", "integration")
                repository = self.hacs.get_by_name("hacs/integration")
            if repository is None:
                raise HacsException("Unknown error")
            repository.data.installed = True
            repository.data.installed_version = self.hacs.integration.version
            repository.data.new = False
            self.hacs.repository = repository.repository_object
        except HacsException as exception:
            if "403" in f"{exception}":
                self.log.critical("GitHub API is ratelimited, or the token is wrong.")
            else:
                self.log.critical("[%s] - Could not load HACS!", exception)
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
            self.hacs.disable_hacs(HacsDisabledReason.LOAD_HACS)
