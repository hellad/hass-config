"""Register WS API endpoints for HACS."""
from __future__ import annotations

import sys

from aiogithubapi import AIOGitHubAPIException
from homeassistant.components import websocket_api
from homeassistant.components.websocket_api import async_register_command
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

<<<<<<< HEAD
from custom_components.hacs.const import DOMAIN

from ..base import HacsBase
from ..enums import HacsStage
from ..exceptions import HacsException
from ..utils import regex
from ..utils.store import async_load_from_store, async_save_to_store
=======
from ..base import HacsBase
from ..enums import HacsStage
from ..exceptions import HacsException
from ..helpers.functions.misc import extract_repository_from_url
from ..helpers.functions.register_repository import register_repository
from ..helpers.functions.store import async_load_from_store, async_save_to_store
from ..share import get_hacs, list_removed_repositories
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
from .base import HacsTask


async def async_setup_task(hacs: HacsBase, hass: HomeAssistant) -> Task:
    """Set up this task."""
    return Task(hacs=hacs, hass=hass)


class Task(HacsTask):
    """Setup the HACS websocket API."""

    stages = [HacsStage.SETUP]

    async def async_execute(self) -> None:
<<<<<<< HEAD
        """Execute the task."""
=======
        """Execute this task."""
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        async_register_command(self.hass, hacs_settings)
        async_register_command(self.hass, hacs_config)
        async_register_command(self.hass, hacs_repositories)
        async_register_command(self.hass, hacs_repository)
        async_register_command(self.hass, hacs_repository_data)
        async_register_command(self.hass, hacs_status)
        async_register_command(self.hass, hacs_removed)
        async_register_command(self.hass, acknowledge_critical_repository)
        async_register_command(self.hass, get_critical_repositories)
<<<<<<< HEAD
        async_register_command(self.hass, hacs_repository_ignore)
=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1


@websocket_api.websocket_command(
    {
        vol.Required("type"): "hacs/critical",
        vol.Optional("repository"): cv.string,
    }
)
@websocket_api.require_admin
@websocket_api.async_response
async def acknowledge_critical_repository(hass, connection, msg):
    """Handle get media player cover command."""
    repository = msg["repository"]

    critical = await async_load_from_store(hass, "critical")
    for repo in critical:
        if repository == repo["repository"]:
            repo["acknowledged"] = True
    await async_save_to_store(hass, "critical", critical)
    connection.send_message(websocket_api.result_message(msg["id"], critical))


@websocket_api.websocket_command(
    {
        vol.Required("type"): "hacs/get_critical",
    }
)
@websocket_api.require_admin
@websocket_api.async_response
async def get_critical_repositories(hass, connection, msg):
    """Handle get media player cover command."""
    critical = await async_load_from_store(hass, "critical")
    if not critical:
        critical = []
    connection.send_message(websocket_api.result_message(msg["id"], critical))


@websocket_api.websocket_command(
    {
        vol.Required("type"): "hacs/config",
    }
)
@websocket_api.require_admin
@websocket_api.async_response
<<<<<<< HEAD
async def hacs_config(hass, connection, msg):
    """Handle get media player cover command."""
    hacs: HacsBase = hass.data.get(DOMAIN)
=======
async def hacs_config(_hass, connection, msg):
    """Handle get media player cover command."""
    hacs = get_hacs()
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    connection.send_message(
        websocket_api.result_message(
            msg["id"],
            {
                "frontend_mode": hacs.configuration.frontend_mode,
                "frontend_compact": hacs.configuration.frontend_compact,
                "onboarding_done": hacs.configuration.onboarding_done,
                "version": hacs.version,
<<<<<<< HEAD
                "frontend_expected": hacs.frontend_version,
                "frontend_running": hacs.frontend_version,
=======
                "frontend_expected": hacs.frontend.version_expected,
                "frontend_running": hacs.frontend.version_running,
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
                "dev": hacs.configuration.dev,
                "debug": hacs.configuration.debug,
                "country": hacs.configuration.country,
                "experimental": hacs.configuration.experimental,
                "categories": hacs.common.categories,
            },
        )
    )


@websocket_api.websocket_command(
    {
        vol.Required("type"): "hacs/removed",
    }
)
@websocket_api.require_admin
@websocket_api.async_response
<<<<<<< HEAD
async def hacs_removed(hass, connection, msg):
    """Get information about removed repositories."""
    hacs: HacsBase = hass.data.get(DOMAIN)
    content = []
    for repo in hacs.repositories.list_removed:
        if repo.repository not in hacs.common.ignored_repositories:
            content.append(repo.to_json())
=======
async def hacs_removed(_hass, connection, msg):
    """Get information about removed repositories."""
    content = []
    for repo in list_removed_repositories():
        content.append(repo.to_json())
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    connection.send_message(websocket_api.result_message(msg["id"], content))


@websocket_api.websocket_command(
    {
        vol.Required("type"): "hacs/repositories",
        vol.Optional("categories"): [str],
    }
)
@websocket_api.require_admin
@websocket_api.async_response
<<<<<<< HEAD
async def hacs_repositories(hass, connection, msg):
    """Handle get media player cover command."""
    hacs: HacsBase = hass.data.get(DOMAIN)
=======
async def hacs_repositories(_hass, connection, msg):
    """Handle get media player cover command."""
    hacs = get_hacs()
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    connection.send_message(
        websocket_api.result_message(
            msg["id"],
            [
                {
<<<<<<< HEAD
                    "additional_info": repo.additional_info,
                    "authors": repo.data.authors,
                    "available_version": repo.display_available_version,
                    "beta": repo.data.show_beta,
                    "can_install": repo.can_download,
                    "category": repo.data.category,
                    "config_flow": repo.data.config_flow,
                    "country": repo.data.country,
                    "custom": not hacs.repositories.is_default(str(repo.data.id)),
=======
                    "additional_info": repo.information.additional_info,
                    "authors": repo.data.authors,
                    "available_version": repo.display_available_version,
                    "beta": repo.data.show_beta,
                    "can_install": repo.can_install,
                    "category": repo.data.category,
                    "config_flow": repo.data.config_flow,
                    "country": repo.data.country,
                    "custom": repo.custom,
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
                    "default_branch": repo.data.default_branch,
                    "description": repo.data.description,
                    "domain": repo.data.domain,
                    "downloads": repo.data.downloads,
                    "file_name": repo.data.file_name,
                    "first_install": repo.status.first_install,
                    "full_name": repo.data.full_name,
                    "hide_default_branch": repo.data.hide_default_branch,
                    "hide": repo.data.hide,
                    "homeassistant": repo.data.homeassistant,
                    "id": repo.data.id,
<<<<<<< HEAD
                    "info": None,
                    "installed_version": repo.display_installed_version,
                    "installed": repo.data.installed,
                    "issues": repo.data.open_issues,
                    "javascript_type": None,
=======
                    "info": repo.information.info,
                    "installed_version": repo.display_installed_version,
                    "installed": repo.data.installed,
                    "issues": repo.data.open_issues,
                    "javascript_type": repo.information.javascript_type,
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
                    "last_updated": repo.data.last_updated,
                    "local_path": repo.content.path.local,
                    "main_action": repo.main_action,
                    "name": repo.display_name,
                    "new": repo.data.new,
<<<<<<< HEAD
                    "pending_upgrade": repo.pending_update,
=======
                    "pending_upgrade": repo.pending_upgrade,
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
                    "releases": repo.data.published_tags,
                    "selected_tag": repo.data.selected_tag,
                    "stars": repo.data.stargazers_count,
                    "state": repo.state,
                    "status_description": repo.display_status_description,
                    "status": repo.display_status,
                    "topics": repo.data.topics,
                    "updated_info": repo.status.updated_info,
                    "version_or_commit": repo.display_version_or_commit,
                }
<<<<<<< HEAD
                for repo in hacs.repositories.list_all
=======
                for repo in hacs.repositories
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
                if repo.data.category in (msg.get("categories") or hacs.common.categories)
                and not repo.ignored_by_country_configuration
            ],
        )
    )


@websocket_api.websocket_command(
    {
        vol.Required("type"): "hacs/repository/data",
        vol.Optional("action"): cv.string,
        vol.Optional("repository"): cv.string,
        vol.Optional("data"): cv.string,
    }
)
@websocket_api.require_admin
@websocket_api.async_response
async def hacs_repository_data(hass, connection, msg):
    """Handle get media player cover command."""
<<<<<<< HEAD
    hacs: HacsBase = hass.data.get(DOMAIN)
=======
    hacs = get_hacs()
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    repo_id = msg.get("repository")
    action = msg.get("action")
    data = msg.get("data")

    if repo_id is None:
        return

    if action == "add":
<<<<<<< HEAD
        repo_id = regex.extract_repository_from_url(repo_id)
=======
        repo_id = extract_repository_from_url(repo_id)
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        if repo_id is None:
            return

        if repo_id in hacs.common.skip:
            hacs.common.skip.remove(repo_id)

        if hacs.common.renamed_repositories.get(repo_id):
            repo_id = hacs.common.renamed_repositories[repo_id]

<<<<<<< HEAD
        if not hacs.repositories.get_by_full_name(repo_id):
            try:
                registration = await hacs.async_register_repository(
                    repository_full_name=repo_id, category=data.lower()
                )
                if registration is not None:
                    raise HacsException(registration)
            except BaseException as exception:  # lgtm [py/catch-base-exception] pylint: disable=broad-except
=======
        if not hacs.get_by_name(repo_id):
            try:
                registration = await register_repository(repo_id, data.lower())
                if registration is not None:
                    raise HacsException(registration)
            except (
                Exception,
                BaseException,
            ) as exception:  # pylint: disable=broad-except
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
                hass.bus.async_fire(
                    "hacs/error",
                    {
                        "action": "add_repository",
                        "exception": str(sys.exc_info()[0].__name__),
                        "message": str(exception),
                    },
                )
        else:
            hass.bus.async_fire(
                "hacs/error",
                {
                    "action": "add_repository",
                    "message": f"Repository '{repo_id}' exists in the store.",
                },
            )

<<<<<<< HEAD
        repository = hacs.repositories.get_by_full_name(repo_id)
    else:
        repository = hacs.repositories.get_by_id(repo_id)
=======
        repository = hacs.get_by_name(repo_id)
    else:
        repository = hacs.get_by_id(repo_id)
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

    if repository is None:
        hass.bus.async_fire("hacs/repository", {})
        return

    hacs.log.debug("Running %s for %s", action, repository.data.full_name)
    try:
        if action == "set_state":
            repository.state = data

        elif action == "set_version":
            repository.data.selected_tag = data
<<<<<<< HEAD
            await repository.update_repository(force=True)
=======
            await repository.update_repository()
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

            repository.state = None

        elif action == "install":
            was_installed = repository.data.installed
            repository.data.selected_tag = data
<<<<<<< HEAD
            await repository.update_repository(force=True)
=======
            await repository.update_repository()
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
            await repository.async_install()
            repository.state = None
            if not was_installed:
                hass.bus.async_fire("hacs/reload", {"force": True})
<<<<<<< HEAD
                await hacs.async_recreate_entities()
=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

        elif action == "add":
            repository.state = None

        else:
            repository.state = None
            hacs.log.error("WS action '%s' is not valid", action)

        message = None
    except AIOGitHubAPIException as exception:
        message = exception
    except AttributeError as exception:
        message = f"Could not use repository with ID {repo_id} ({exception})"
<<<<<<< HEAD
    except BaseException as exception:  # lgtm [py/catch-base-exception] pylint: disable=broad-except
=======
    except (Exception, BaseException) as exception:  # pylint: disable=broad-except
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        message = exception

    if message is not None:
        hacs.log.error(message)
        hass.bus.async_fire("hacs/error", {"message": str(message)})

    await hacs.data.async_write()
    connection.send_message(websocket_api.result_message(msg["id"], {}))


@websocket_api.websocket_command(
    {
        vol.Required("type"): "hacs/repository",
        vol.Optional("action"): cv.string,
        vol.Optional("repository"): cv.string,
    }
)
@websocket_api.require_admin
@websocket_api.async_response
async def hacs_repository(hass, connection, msg):
    """Handle get media player cover command."""
<<<<<<< HEAD
    hacs: HacsBase = hass.data.get(DOMAIN)
=======
    hacs = get_hacs()
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    data = {}
    repository = None

    repo_id = msg.get("repository")
    action = msg.get("action")
    if repo_id is None or action is None:
        return

    try:
<<<<<<< HEAD
        repository = hacs.repositories.get_by_id(repo_id)
=======
        repository = hacs.get_by_id(repo_id)
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        hacs.log.debug(f"Running {action} for {repository.data.full_name}")

        if action == "update":
            await repository.update_repository(ignore_issues=True, force=True)
            repository.status.updated_info = True

        elif action == "install":
            repository.data.new = False
            was_installed = repository.data.installed
            await repository.async_install()
            if not was_installed:
                hass.bus.async_fire("hacs/reload", {"force": True})
<<<<<<< HEAD
                await hacs.async_recreate_entities()
=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

        elif action == "not_new":
            repository.data.new = False

        elif action == "uninstall":
            repository.data.new = False
<<<<<<< HEAD
            await repository.update_repository(ignore_issues=True, force=True)
=======
            await repository.update_repository(True)
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
            await repository.uninstall()

        elif action == "hide":
            repository.data.hide = True

        elif action == "unhide":
            repository.data.hide = False

        elif action == "show_beta":
            repository.data.show_beta = True
<<<<<<< HEAD
            await repository.update_repository(force=True)

        elif action == "hide_beta":
            repository.data.show_beta = False
            await repository.update_repository(force=True)

        elif action == "toggle_beta":
            repository.data.show_beta = not repository.data.show_beta
            await repository.update_repository(force=True)
=======
            await repository.update_repository()

        elif action == "hide_beta":
            repository.data.show_beta = False
            await repository.update_repository()

        elif action == "toggle_beta":
            repository.data.show_beta = not repository.data.show_beta
            await repository.update_repository()
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

        elif action == "delete":
            repository.data.show_beta = False
            repository.remove()

        elif action == "release_notes":
            data = [
                {
<<<<<<< HEAD
                    "name": x.name,
                    "body": x.body,
                    "tag": x.tag_name,
=======
                    "name": x.attributes["name"],
                    "body": x.attributes["body"],
                    "tag": x.attributes["tag_name"],
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
                }
                for x in repository.releases.objects
            ]

        elif action == "set_version":
            if msg["version"] == repository.data.default_branch:
                repository.data.selected_tag = None
            else:
                repository.data.selected_tag = msg["version"]
<<<<<<< HEAD
            await repository.update_repository(force=True)
=======
            await repository.update_repository()
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

            hass.bus.async_fire("hacs/reload", {"force": True})

        else:
            hacs.log.error(f"WS action '{action}' is not valid")

        await hacs.data.async_write()
        message = None
    except AIOGitHubAPIException as exception:
        message = exception
    except AttributeError as exception:
        message = f"Could not use repository with ID {repo_id} ({exception})"
<<<<<<< HEAD
    except BaseException as exception:  # lgtm [py/catch-base-exception] pylint: disable=broad-except
=======
    except (Exception, BaseException) as exception:  # pylint: disable=broad-except
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
        message = exception

    if message is not None:
        hacs.log.error(message)
        hass.bus.async_fire("hacs/error", {"message": str(message)})

    if repository:
        repository.state = None
        connection.send_message(websocket_api.result_message(msg["id"], data))


@websocket_api.websocket_command(
    {
        vol.Required("type"): "hacs/settings",
        vol.Optional("action"): cv.string,
        vol.Optional("categories"): cv.ensure_list,
    }
)
@websocket_api.require_admin
@websocket_api.async_response
async def hacs_settings(hass, connection, msg):
    """Handle get media player cover command."""
<<<<<<< HEAD
    hacs: HacsBase = hass.data.get(DOMAIN)
=======
    hacs = get_hacs()
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

    action = msg["action"]
    hacs.log.debug("WS action '%s'", action)

    if action == "set_fe_grid":
        hacs.configuration.frontend_mode = "Grid"

    elif action == "onboarding_done":
        hacs.configuration.onboarding_done = True

    elif action == "set_fe_table":
        hacs.configuration.frontend_mode = "Table"

    elif action == "set_fe_compact_true":
        hacs.configuration.frontend_compact = False

    elif action == "set_fe_compact_false":
        hacs.configuration.frontend_compact = True

    elif action == "clear_new":
<<<<<<< HEAD
        for repo in hacs.repositories.list_all:
=======
        for repo in hacs.repositories:
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
            if repo.data.new and repo.data.category in msg.get("categories", []):
                hacs.log.debug(
                    "Clearing new flag from '%s'",
                    repo.data.full_name,
                )
                repo.data.new = False
    else:
        hacs.log.error("WS action '%s' is not valid", action)
    hass.bus.async_fire("hacs/config", {})
    await hacs.data.async_write()
    connection.send_message(websocket_api.result_message(msg["id"], {}))


@websocket_api.websocket_command({vol.Required("type"): "hacs/status"})
@websocket_api.require_admin
@websocket_api.async_response
<<<<<<< HEAD
async def hacs_status(hass, connection, msg):
    """Handle get media player cover command."""
    hacs: HacsBase = hass.data.get(DOMAIN)
=======
async def hacs_status(_hass, connection, msg):
    """Handle get media player cover command."""
    hacs = get_hacs()
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    connection.send_message(
        websocket_api.result_message(
            msg["id"],
            {
                "startup": hacs.status.startup,
<<<<<<< HEAD
                "background_task": False,
=======
                "background_task": hacs.status.background_task,
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
                "lovelace_mode": hacs.core.lovelace_mode,
                "reloading_data": hacs.status.reloading_data,
                "upgrading_all": hacs.status.upgrading_all,
                "disabled": hacs.system.disabled,
                "disabled_reason": hacs.system.disabled_reason,
                "has_pending_tasks": hacs.queue.has_pending_tasks,
                "stage": hacs.stage,
            },
        )
    )
<<<<<<< HEAD


@websocket_api.websocket_command(
    {
        vol.Required("type"): "hacs/repository/ignore",
        vol.Required("repository"): str,
    }
)
@websocket_api.require_admin
@websocket_api.async_response
async def hacs_repository_ignore(hass, connection, msg):
    """Ignore a repository."""
    hacs: HacsBase = hass.data.get(DOMAIN)
    hacs.common.ignored_repositories.append(msg["repository"])
    connection.send_message(websocket_api.result_message(msg["id"]))
=======
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
