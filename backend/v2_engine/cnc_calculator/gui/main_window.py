"""Main window for CNC Calculator application."""

import logging
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QFileDialog,
    QMessageBox,
    QStatusBar,
)
from PySide6.QtCore import Qt
from ..core.config_loader import ConfigLoader
from ..core.calculation_engine import CalculationEngine
from ..core.validator import Validator
from ..io.tools_reader import ToolsReader
from ..io.tools_writer import ToolsWriter

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, config_dir: Path):
        """Initialize main window.

        Args:
            config_dir: Path to configuration directory
        """
        super().__init__()

        self.config_dir = config_dir
        self.tools = []
        self.current_step = 0

        # Initialize components
        self._init_components()
        self._init_ui()
        self._connect_signals()

        logger.info("Main window initialized")

    def _init_components(self):
        """Initialize core components."""
        try:
            # Load configuration
            self.config_loader = ConfigLoader(self.config_dir)
            self.materials = self.config_loader.load_materials()
            self.operations = self.config_loader.load_operations()

            # Initialize calculation engine
            self.calc_engine = CalculationEngine(self.config_loader)

            # Initialize validator
            sorotec_ref = self.config_loader.load_sorotec_reference()
            self.validator = Validator(sorotec_ref)

            # Initialize I/O
            self.tools_reader = ToolsReader()
            self.tools_writer = ToolsWriter()

            logger.info(
                f"Loaded {len(self.materials)} materials, "
                f"{len(self.operations)} operations"
            )

        except Exception as e:
            logger.error(f"Failed to initialize components: {e}", exc_info=True)
            raise

    def _init_ui(self):
        """Initialize user interface."""
        self.setWindowTitle("CNC Schnittwerte Calculator v1.0")
        self.setMinimumSize(1000, 700)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)

        # Title
        title_label = QLabel("CNC Schnittwerte Calculator")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Subtitle
        subtitle = QLabel(
            "Wissenschaftlich fundierte Berechnung von CNC-Schnittdaten für Trockenbearbeitung"
        )
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        # Create stacked widget for wizard steps
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Add wizard pages
        self._create_wizard_pages()

        # Navigation buttons
        nav_layout = QHBoxLayout()

        self.back_button = QPushButton("← Zurück")
        self.back_button.setEnabled(False)
        self.back_button.clicked.connect(self._go_back)
        nav_layout.addWidget(self.back_button)

        nav_layout.addStretch()

        self.next_button = QPushButton("Weiter →")
        self.next_button.clicked.connect(self._go_next)
        nav_layout.addWidget(self.next_button)

        layout.addLayout(nav_layout)

        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Bereit")

    def _create_wizard_pages(self):
        """Create wizard step pages."""
        # Step 0: Welcome & Import
        welcome_page = self._create_welcome_page()
        self.stacked_widget.addWidget(welcome_page)

        # Step 1: Tool Selection (placeholder)
        tool_selection_page = self._create_placeholder_page(
            "Schritt 1: Werkzeuge auswählen",
            "Hier können Sie die zu berechnenden Werkzeuge auswählen.",
        )
        self.stacked_widget.addWidget(tool_selection_page)

        # Step 2: Material Matrix (placeholder)
        material_page = self._create_placeholder_page(
            "Schritt 2: Material-Werkzeug Matrix",
            "Wählen Sie für jedes Werkzeug die zu berechnenden Materialien.",
        )
        self.stacked_widget.addWidget(material_page)

        # Step 3: Operation Matrix (placeholder)
        operation_page = self._create_placeholder_page(
            "Schritt 3: Operations-Matrix",
            "Wählen Sie für jede Kombination die Operationen.",
        )
        self.stacked_widget.addWidget(operation_page)

        # Step 4: Results (placeholder)
        results_page = self._create_placeholder_page(
            "Schritt 4: Ergebnisse überprüfen", "Überprüfen und exportieren Sie die berechneten Werte."
        )
        self.stacked_widget.addWidget(results_page)

    def _create_welcome_page(self) -> QWidget:
        """Create welcome page with import button.

        Returns:
            Welcome page widget
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        layout.addStretch()

        # Welcome message
        welcome_label = QLabel("Willkommen beim CNC Schnittwerte Calculator!")
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        layout.addSpacing(20)

        # Instructions
        instructions = QLabel(
            "Dieser Assistent führt Sie durch die Berechnung von Schnittdaten:\n\n"
            "1. Importieren Sie eine .tools Datei mit Werkzeuggeometrien\n"
            "2. Wählen Sie die zu berechnenden Werkzeuge\n"
            "3. Wählen Sie Materialien und Operationen\n"
            "4. Überprüfen Sie die berechneten Werte\n"
            "5. Exportieren Sie die .tools Datei für Fusion 360\n\n"
            "Zum Starten klicken Sie auf 'Importieren'."
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        layout.addSpacing(30)

        # Import button
        import_button = QPushButton("📁 .tools Datei importieren")
        import_button.setStyleSheet("padding: 10px; font-size: 14px;")
        import_button.clicked.connect(self._import_tools)
        layout.addWidget(import_button, alignment=Qt.AlignCenter)

        layout.addStretch()

        return page

    def _create_placeholder_page(self, title: str, description: str) -> QWidget:
        """Create a placeholder page for future implementation.

        Args:
            title: Page title
            description: Page description

        Returns:
            Placeholder widget
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        layout.addStretch()

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        layout.addSpacing(10)

        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)

        layout.addSpacing(10)

        placeholder = QLabel("🚧 In Entwicklung 🚧")
        placeholder.setStyleSheet("font-size: 14px; color: #888;")
        placeholder.setAlignment(Qt.AlignCenter)
        layout.addWidget(placeholder)

        layout.addStretch()

        return page

    def _connect_signals(self):
        """Connect signals and slots."""
        pass  # Add signal connections as needed

    def _import_tools(self):
        """Import .tools file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Importiere .tools Datei", "", "Fusion 360 Tools (*.tools)"
        )

        if not file_path:
            return

        try:
            self.statusBar.showMessage(f"Importiere {Path(file_path).name}...")
            self.tools = self.tools_reader.read_tools_file(Path(file_path))

            QMessageBox.information(
                self,
                "Import erfolgreich",
                f"Es wurden {len(self.tools)} Werkzeuge importiert.\n\n"
                f"Klicken Sie auf 'Weiter', um mit der Auswahl fortzufahren.",
            )

            self.statusBar.showMessage(
                f"{len(self.tools)} Werkzeuge geladen", 5000
            )
            self.next_button.setEnabled(True)

        except Exception as e:
            logger.error(f"Import failed: {e}", exc_info=True)
            QMessageBox.critical(
                self, "Import fehlgeschlagen", f"Fehler beim Importieren:\n{str(e)}"
            )
            self.statusBar.showMessage("Import fehlgeschlagen")

    def _go_next(self):
        """Go to next wizard step."""
        if self.current_step < self.stacked_widget.count() - 1:
            self.current_step += 1
            self.stacked_widget.setCurrentIndex(self.current_step)
            self.back_button.setEnabled(True)

            if self.current_step == self.stacked_widget.count() - 1:
                self.next_button.setText("Exportieren")

    def _go_back(self):
        """Go to previous wizard step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.stacked_widget.setCurrentIndex(self.current_step)

            if self.current_step == 0:
                self.back_button.setEnabled(False)

            self.next_button.setText("Weiter →")
