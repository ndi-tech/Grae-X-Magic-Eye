import os
from pathlib import Path

class Config:
    APP_NAME = "Grae-X Magic Eye Shield"
    APP_VERSION = "1.0.0"
    DOWNLOAD_FOLDER = str(Path.home() / "Downloads")
    MONITOR_FOLDERS = [DOWNLOAD_FOLDER, str(Path.home() / "Desktop")]
    IGNORE_EXTENSIONS = ['.tmp', '.temp', '.part', '.crdownload']
    POPUP_DURATION = 8000  # ms
    POPUP_WIDTH = 500
    POPUP_HEIGHT = 350