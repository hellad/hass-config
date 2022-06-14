"""Class for plugins in HACS."""
<<<<<<< HEAD
from __future__ import annotations

import json
from typing import TYPE_CHECKING

from ..exceptions import HacsException
from ..utils.decorator import concurrent
from .base import HacsRepository

if TYPE_CHECKING:
    from ..base import HacsBase
=======
import json

from custom_components.hacs.exceptions import HacsException
from custom_components.hacs.helpers.classes.repository import HacsRepository
from custom_components.hacs.helpers.functions.information import find_file_name
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1


class HacsPluginRepository(HacsRepository):
    """Plugins in HACS."""

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
        self.data.file_name = None
        self.data.category = "plugin"
<<<<<<< HEAD
=======
        self.information.javascript_type = None
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        self.content.path.local = self.localpath

    @property
    def localpath(self):
        """Return localpath."""
        return f"{self.hacs.core.config_path}/www/community/{self.data.full_name.split('/')[-1]}"

    async def validate_repository(self):
        """Validate."""
        # Run common validation steps.
        await self.common_validate()

        # Custom step 1: Validate content.
<<<<<<< HEAD
        self.update_filenames()

        if self.content.path.remote is None:
            raise HacsException(
                f"Repository structure for {self.ref.replace('tags/','')} is not compliant"
=======
        find_file_name(self)

        if self.content.path.remote is None:
            raise HacsException(
                f"Repostitory structure for {self.ref.replace('tags/','')} is not compliant"
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
            )

        if self.content.path.remote == "release":
            self.content.single = True

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
            return

        # Get plugin objects.
        self.update_filenames()

        if self.content.path.remote is None:
            self.validate.errors.append(
                f"Repository structure for {self.ref.replace('tags/','')} is not compliant"
=======
                    self.logger.error("%s %s", self, error)
        return self.validate.success

    async def update_repository(self, ignore_issues=False, force=False):
        """Update."""
        if not await self.common_update(ignore_issues, force):
            return

        # Get plugin objects.
        find_file_name(self)

        if self.content.path.remote is None:
            self.validate.errors.append(
                f"Repostitory structure for {self.ref.replace('tags/','')} is not compliant"
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
            )

        if self.content.path.remote == "release":
            self.content.single = True

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
    async def get_package_content(self):
        """Get package content."""
        try:
            package = await self.repository_object.get_contents("package.json", self.ref)
            package = json.loads(package.content)

            if package:
                self.data.authors = package["author"]
<<<<<<< HEAD
        except BaseException:  # lgtm [py/catch-base-exception] pylint: disable=broad-except
            pass

    def update_filenames(self) -> None:
        """Get the filename to target."""
        possible_locations = ("",) if self.data.content_in_root else ("release", "dist", "")

        # Handler for plug requirement 3
        if self.data.filename:
            valid_filenames = (self.data.filename,)
        else:
            valid_filenames = (
                f"{self.data.name.replace('lovelace-', '')}.js",
                f"{self.data.name}.js",
                f"{self.data.name}.umd.js",
                f"{self.data.name}-bundle.js",
            )

        for location in possible_locations:
            if location == "release":
                if not self.releases.objects:
                    continue
                release = self.releases.objects[0]
                if not release.assets:
                    continue
                asset = release.assets[0]
                for filename in valid_filenames:
                    if filename == asset.name:
                        self.data.file_name = filename
                        self.content.path.remote = "release"
                        break

            else:
                for filename in valid_filenames:
                    if f"{location+'/' if location else ''}{filename}" in [
                        x.full_path for x in self.tree
                    ]:
                        self.data.file_name = filename.split("/")[-1]
                        self.content.path.remote = location
                        break
=======
        except (Exception, BaseException):  # pylint: disable=broad-except
            pass
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
