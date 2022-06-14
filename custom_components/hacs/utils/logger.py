"""Custom logger for HACS."""
<<<<<<< HEAD
import logging
=======
# pylint: disable=invalid-name
import logging
import os
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1

from ..const import PACKAGE_NAME

_HACSLogger: logging.Logger = logging.getLogger(PACKAGE_NAME)

<<<<<<< HEAD

def get_hacs_logger() -> logging.Logger:
=======
if "GITHUB_ACTION" in os.environ:
    logging.basicConfig(
        format="::%(levelname)s:: %(message)s",
        level="DEBUG",
    )


def getLogger(_name: str = None) -> logging.Logger:
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    """Return a Logger instance."""
    return _HACSLogger
