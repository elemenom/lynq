import atexit
import os
import logging

from lynq._backendutils.lynq.pycache_remover import remove_pycache_from
from lynq._backendutils.lynq.pycache_remover import PYCACHE_REMOVAL_LOCATIONS

import logging

from typing import Any

_warn: bool = False

try:
    from lynqconfig import LOGGER as logger # type: ignore
    from lynqconfig import LOGGINGCONFIG as additional # type: ignore
    from lynqconfig import LOGGINGLEVEL as level # type: ignore
    from lynqconfig import LOGGINGFORMAT as format_ # type: ignore
    from lynqconfig import CLEANPYCACHE as clean # type: ignore
except ModuleNotFoundError:
    logger, \
    additional, \
    level, \
    format_, \
    clean \
    = None, None, None, None, None

    _warn = True

logging.basicConfig(
    level = eval(f"logging.{level}") if level else logging.DEBUG,
    format = format_ or "%(asctime)s ~ %(levelname)s | %(message)s",
    **additional or {}
)

GLOBAL_LOGGER: Any = logger or logging.getLogger(__name__)
CLEAN_CACHE: bool = clean or False

if _warn:
    GLOBAL_LOGGER.warning("An error occured while parsing your lynqconfig.py file and all options have been \
returned to their default state/value.")

def _clean_up() -> None:
    handlers: list[logging.Handler] = GLOBAL_LOGGER.handlers

    logging.shutdown()

    if os.path.exists("throwaway.log"):
        os.remove("throwaway.log")

def _clean_up_cache() -> None:
    GLOBAL_LOGGER.debug("Commencing pycache clean up process.")

    for path in PYCACHE_REMOVAL_LOCATIONS:
        remove_pycache_from(f"./lynq/{path.replace(".", "/")}")

def _at_exit_func() -> None:

    GLOBAL_LOGGER.debug("Commencing logger deletion and clean up process.")
    
    if CLEAN_CACHE:
        _clean_up_cache()

    _clean_up()

    print(f"[Exiting...] Program ended successfully. All active servers terminated.")

atexit.register(_at_exit_func)