import platform
from typing import List, Literal
from pydantic import Field, validator
from pydantic.dataclasses import dataclass
from app.core.models.base_model import BaseModel
from pathlib import Path


@dataclass(config=dict(validate_assignment=True, frozen=True))
class SystemModel(BaseModel):
    """
    Data model for system variables and configurations.
    """

    # System section
    OS: str = str(platform.system())
    PYTHON_VERSION: str = str(platform.python_version())
    PLATFORM: str = str(platform.platform())

    # Logging section
    LOGGING_FREQUENCY: Literal["D", "H", "M", "S"] = "H"
    LOGGING_HANDLERS: List[str] = Field(default_factory=lambda: ["file", "stream"])
    LOGGING_ROLLING_CLOCK: bool = False
    LOGGING_VERBOSITY: int = 50  # 0 - Not set, 10 - Debug, 20 - Info, 30 - Warning, 40 - Error, 50 - Critical
    LOGGING_SUPPRESS: bool = False
    LOG_COLLECT: bool = True

    # Others
    TEST_MODE: bool = False
    DEBUG_MODE: bool = False

    # Paths
    HOME_DIRECTORY = Path.home()
    USER_DATA_DIRECTORY = HOME_DIRECTORY / "STOCKDB_USERDATA"

    @validator("LOGGING_HANDLERS", allow_reuse=True)
    @classmethod
    def validate_logging_handlers(cls, v):
        for value in v:
            if value not in ["noop", "file", "stream"]:
                raise ValueError("Invalid logging handler")
        return v
