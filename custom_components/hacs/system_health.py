"""Provide info to system health."""
from aiogithubapi.common.const import BASE_API_URL
from homeassistant.components import system_health
from homeassistant.core import HomeAssistant, callback

from .base import HacsBase
from .const import DOMAIN

GITHUB_STATUS = "https://www.githubstatus.com/"


@callback
def async_register(hass: HomeAssistant, register: system_health.SystemHealthRegistration) -> None:
    """Register system health callbacks."""
    register.domain = "Home Assistant Community Store"
    register.async_register_info(system_health_info, "/hacs")


async def system_health_info(hass):
    """Get info for the info page."""
    hacs: HacsBase = hass.data[DOMAIN]
    response = await hacs.githubapi.rate_limit()

    data = {
        "GitHub API": system_health.async_check_can_reach_url(hass, BASE_API_URL, GITHUB_STATUS),
<<<<<<< HEAD
        "GitHub Content": system_health.async_check_can_reach_url(
            hass, "https://raw.githubusercontent.com/hacs/integration/main/hacs.json"
        ),
        "GitHub Web": system_health.async_check_can_reach_url(
            hass, "https://github.com/", GITHUB_STATUS
        ),
        "GitHub API Calls Remaining": response.data.resources.core.remaining,
        "Installed Version": hacs.version,
        "Stage": hacs.stage,
        "Available Repositories": len(hacs.repositories.list_all),
        "Downloaded Repositories": len(hacs.repositories.list_downloaded),
=======
        "Github API Calls Remaining": response.data.resources.core.remaining,
        "Installed Version": hacs.version,
        "Stage": hacs.stage,
        "Available Repositories": len(hacs.repositories),
        "Installed Repositories": len([repo for repo in hacs.repositories if repo.data.installed]),
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    }

    if hacs.system.disabled:
        data["Disabled"] = hacs.system.disabled_reason

    return data
