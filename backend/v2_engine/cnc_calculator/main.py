"""Main entry point for CNC Calculator application."""

import sys
import logging
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# Import GUI components
from .gui.main_window_complete import MainWindowComplete

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for troubleshooting
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    """Main application entry point."""
    logger.info("Starting CNC Schnittwerte Calculator")

    # Enable High DPI support
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("CNC Schnittwerte Calculator")
    app.setOrganizationName("CNC Tools")

    # Create and show main window
    try:
        window = MainWindowComplete()
        window.show()
    except Exception as e:
        logger.error(f"Failed to create main window: {e}", exc_info=True)
        return 1

    # Run application
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
