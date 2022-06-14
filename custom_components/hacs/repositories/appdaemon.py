"""Class for appdaemon apps in HACS."""
<<<<<<< HEAD
from __future__ import annotations

from typing import TYPE_CHECKING

from aiogithubapi import AIOGitHubAPIException

from ..enums import HacsCategory
from ..exceptions import HacsException
from ..utils.decorator import concurrent
from .base import HacsRepository

if TYPE_CHECKING:
    from ..base import HacsBase
=======
from aiogithubapi import AIOGitHubAPIException

from custom_components.hacs.enums import HacsCategory
from custom_components.hacs.exceptions import HacsException
from custom_components.hacs.helpers.classes.repository import HacsRepository
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1


class HacsAppdaemonRepository(HacsRepository):
    """Appdaemon apps in HACS."""

<<<<<<< HEAD
    def __init__(self, hacs: HacsBase, full_name: str):
        """Initialize."""
        super().__init__(hacs=hacs)
=======
    def __init__(self, full_name):
        """Initialize."""
        super().__init__()
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        self.data.full_name = full_name
        self.data.full_name_lower = full_name.lower()
        self.data.category = HacsCategory.APPDAEMON
        self.content.path.local = self.localpath
        self.content.path.remote = "apps"

    @property
    def localpath(self):
        """Return localpath."""
        return f"{self.hacs.core.config_path}/appdaemon/apps/{self.data.name}"

    async def validate_repository(self):
        """Validate."""
        await self.common_validate()

        # Custom step 1: Validate content.
        try:
            addir = await self.repository_object.get_contents("apps", self.ref)
        except AIOGitHubAPIException:
            raise HacsException(
<<<<<<< HEAD
                f"Repository structure for {self.ref.replace('tags/','')} is not compliant"
            ) from None

        if not isinstance(addir, list):
            self.validate.errors.append("Repository structure not compliant")
=======
                f"Repostitory structure for {self.ref.replace('tags/','')} is not compliant"
            ) from None

        if not isinstance(addir, list):
            self.validate.errors.append("Repostitory structure not compliant")
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

        self.content.path.remote = addir[0].path
        self.content.objects = await self.repository_object.get_contents(
            self.content.path.remote, self.ref
        )

        # Handle potential errors
        if self.validate.errors:
            for error in self.validate.errors:
                if not self.hacs.status.startup:
<<<<<<< HEAD
                    self.logger.error("%s %s", self.string, error)
        return self.validate.success

    @concurrent(concurrenttasks=10, backoff_time=5)
    async def update_repository(self, ignore_issues=False, force=False):
        """Update."""
        if not await self.common_update(ignore_issues, force) and not force:
=======
                    self.logger.error("%s %s", self, error)
        return self.validate.success

    async def update_repository(self, ignore_issues=False, force=False):
        """Update."""
        if not await self.common_update(ignore_issues, force):
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
            return

        # Get appdaemon objects.
        if self.repository_manifest:
            if self.data.content_in_root:
                self.content.path.remote = ""

        if self.content.path.remote == "apps":
            addir = await self.repository_object.get_contents(self.content.path.remote, self.ref)
            self.content.path.remote = addir[0].path
        self.content.objects = await self.repository_object.get_contents(
            self.content.path.remote, self.ref
        )

        # Set local path
        self.content.path.local = self.localpath
<<<<<<< HEAD

        # Signal entities to refresh
        if self.data.installed:
            self.hacs.hass.bus.async_fire(
                "hacs/repository",
                {
                    "id": 1337,
                    "action": "update",
                    "repository": self.data.full_name,
                    "repository_id": self.data.id,
                },
            )
=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
