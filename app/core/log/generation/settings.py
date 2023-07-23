# IMPORTATION STANDARD
from copy import deepcopy
from pathlib import Path

# IMPORTATION THIRDPARTY
from typing import List

# IMPORTATION INTERNAL


class LogSettings:
    @property
    def directory(self) -> Path:
        return self.__directory

    @property
    def frequency(self) -> str:
        return self.__frequency

    @property
    def handler_list(self) -> List[str]:
        return self.__handler_list

    @property
    def rolling_clock(self) -> bool:
        return self.__rolling_clock

    @property
    def verbosity(self) -> int:
        return self.__verbosity

    def __init__(
        self,
        directory: Path,
        frequency: str,
        handler_list: List[str],
        rolling_clock: bool,
        verbosity: int,
    ):
        """
        Args:
            directory (Path): Directory used to store log files.
            frequency (str): Frequency of the log files rotation.
            handler_list (List[str]) : list of handlers : stdout,stderr,noop,file,posthog.
            rolling_clock (bool): Whether or not to start a Thread to rotate logs even when inactive.
            verbosity (str): Verbosity level as defined in Python `logging` module.
        """

        self.__directory = directory
        self.__frequency = frequency
        self.__handler_list = handler_list
        self.__rolling_clock = rolling_clock
        self.__verbosity = verbosity


class Settings:
    @property
    def log_settings(self) -> LogSettings:
        return deepcopy(self.__log_settings)
    
    def __init__(
        self,
        log_settings: LogSettings,
    ):
        """
        Args:
            log_settings (str): Instance of LogSettings.
        """

        self.__log_settings = log_settings
