from pathlib import Path
from app.core.session.current_system import get_current_system


def get_log_dir() -> Path:
    """Retrieve application's log directory."""
    log_dir = get_current_system().USER_DATA_DIRECTORY.joinpath("logs").absolute()
    if not log_dir.is_dir():
        log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir
