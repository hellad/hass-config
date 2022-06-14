"""Path utils"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
<<<<<<< HEAD
    from ..base import HacsBase


def is_safe(hacs: HacsBase, path: str | Path) -> bool:
    """Helper to check if path is safe to remove."""
    return Path(path).as_posix() not in (
        Path(f"{hacs.core.config_path}/{hacs.configuration.appdaemon_path}").as_posix(),
        Path(f"{hacs.core.config_path}/{hacs.configuration.netdaemon_path}").as_posix(),
        Path(f"{hacs.core.config_path}/{hacs.configuration.plugin_path}").as_posix(),
        Path(f"{hacs.core.config_path}/{hacs.configuration.python_script_path}").as_posix(),
        Path(f"{hacs.core.config_path}/{hacs.configuration.theme_path}").as_posix(),
        Path(f"{hacs.core.config_path}/custom_components/").as_posix(),
    )
=======
    from ..hacsbase.hacs import Hacs


def is_safe(hacs: Hacs, path: str | Path) -> bool:
    """Helper to check if path is safe to remove."""
    paths = [
        Path(f"{hacs.core.config_path}/{hacs.configuration.appdaemon_path}"),
        Path(f"{hacs.core.config_path}/{hacs.configuration.netdaemon_path}"),
        Path(f"{hacs.core.config_path}/{hacs.configuration.plugin_path}"),
        Path(f"{hacs.core.config_path}/{hacs.configuration.python_script_path}"),
        Path(f"{hacs.core.config_path}/{hacs.configuration.theme_path}"),
        Path(f"{hacs.core.config_path}/custom_components/"),
    ]
    return Path(path) not in paths
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
