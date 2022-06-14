"""Class for python_scripts in HACS."""
<<<<<<< HEAD
from __future__ import annotations

from typing import TYPE_CHECKING

from ..enums import HacsCategory
from ..exceptions import HacsException
from ..utils.decorator import concurrent
from .base import HacsRepository

if TYPE_CHECKING:
    from ..base import HacsBase
=======
from custom_components.hacs.enums import HacsCategory
from custom_components.hacs.exceptions import HacsException
from custom_components.hacs.helpers.classes.repository import HacsRepository
from custom_components.hacs.helpers.functions.information import find_file_name
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1


class HacsPythonScriptRepository(HacsRepository):
    """python_scripts in HACS."""

    category = "python_script"

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
        self.data.category = HacsCategory.PYTHON_SCRIPT
        self.content.path.remote = "python_scripts"
        self.content.path.local = self.localpath
        self.content.single = True

    @property
    def localpath(self):
        """Return localpath."""
        return f"{self.hacs.core.config_path}/python_scripts"

    async def validate_repository(self):
        """Validate."""
        # Run common validation steps.
        await self.common_validate()

        # Custom step 1: Validate content.
        if self.data.content_in_root:
            self.content.path.remote = ""

        compliant = False
        for treefile in self.treefiles:
            if treefile.startswith(f"{self.content.path.remote}") and treefile.endswith(".py"):
                compliant = True
                break
        if not compliant:
            raise HacsException(
                f"Repository structure for {self.ref.replace('tags/','')} is not compliant"
            )

        # Handle potential errors
        if self.validate.errors:
            for error in self.validate.errors:
                if not self.hacs.status.startup:
<<<<<<< HEAD
                    self.logger.error("%s %s", self.string, error)
=======
                    self.logger.error("%s %s", self, error)
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        return self.validate.success

    async def async_post_registration(self):
        """Registration."""
        # Set name
<<<<<<< HEAD
        self.update_filenames()

    @concurrent(concurrenttasks=10, backoff_time=5)
    async def update_repository(self, ignore_issues=False, force=False):
        """Update."""
        if not await self.common_update(ignore_issues, force) and not force:
=======
        find_file_name(self)

    async def update_repository(self, ignore_issues=False, force=False):
        """Update."""
        if not await self.common_update(ignore_issues, force):
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
            return

        # Get python_script objects.
        if self.data.content_in_root:
            self.content.path.remote = ""

        compliant = False
        for treefile in self.treefiles:
            if treefile.startswith(f"{self.content.path.remote}") and treefile.endswith(".py"):
                compliant = True
                break
        if not compliant:
            raise HacsException(
                f"Repository structure for {self.ref.replace('tags/','')} is not compliant"
            )

        # Update name
<<<<<<< HEAD
        self.update_filenames()

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

    def update_filenames(self) -> None:
        """Get the filename to target."""
        for treefile in self.tree:
            if treefile.full_path.startswith(
                self.content.path.remote
            ) and treefile.full_path.endswith(".py"):
                self.data.file_name = treefile.filename
=======
        find_file_name(self)
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
