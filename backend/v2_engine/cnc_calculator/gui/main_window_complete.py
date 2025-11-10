"""Complete main window with full workflow integration."""

import logging
from pathlib import Path
from datetime import datetime
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
    QProgressDialog,
)
from PySide6.QtCore import Qt
from ..core.calculation_engine import CalculationEngine
from ..io.tools_reader import ToolsReader
from ..io.tools_writer import ToolsWriter
from .tool_selector_widget import ToolSelectorWidget
from .material_matrix_widget import MaterialMatrixWidget
from .operation_matrix_widget import OperationMatrixWidget, OPERATIONS_CONFIG
from .results_viewer_widget import ResultsViewerWidget

logger = logging.getLogger(__name__)


class MainWindowComplete(QMainWindow):
    """Complete main window with full workflow."""

    def __init__(self):
        """Initialize main window."""
        super().__init__()

        self.tools = []
        self.current_step = 0

        # FEATURE: Track imported file for smart export naming
        self.last_imported_file = None

        # FEATURE: Setup default directories
        self.project_root = Path.cwd()
        self.import_dir = self.project_root / "import"
        self.export_dir = self.project_root / "export"

        # Create directories if they don't exist
        self.import_dir.mkdir(exist_ok=True)
        self.export_dir.mkdir(exist_ok=True)
        logger.info(f"Default import dir: {self.import_dir}")
        logger.info(f"Default export dir: {self.export_dir}")

        # Initialize components
        self._init_components()
        self._init_ui()
        self._connect_signals()

        logger.info("Main window initialized")

    def _init_components(self):
        """Initialize core components."""
        try:
            # Initialize calculation engine (NEW - loads configs internally)
            self.calc_engine = CalculationEngine()

            # Get materials and operations from engine
            self.materials = self.calc_engine.materials
            self.operations = self.calc_engine.operations

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
        self.setMinimumSize(1200, 800)

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

        layout.addSpacing(10)

        # Step indicator
        self.step_label = QLabel()
        self.step_label.setAlignment(Qt.AlignCenter)
        self.step_label.setStyleSheet("font-size: 12px; color: #666;")
        layout.addWidget(self.step_label)

        layout.addSpacing(10)

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

        self.calculate_button = QPushButton("🔄 Berechnen")
        self.calculate_button.setVisible(False)
        self.calculate_button.clicked.connect(self._calculate_presets)
        nav_layout.addWidget(self.calculate_button)

        self.next_button = QPushButton("Weiter →")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self._go_next)
        nav_layout.addWidget(self.next_button)

        layout.addLayout(nav_layout)

        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Bereit")

        self._update_step_label()

    def _create_wizard_pages(self):
        """Create wizard step pages."""
        # Step 0: Welcome & Import
        welcome_page = self._create_welcome_page()
        self.stacked_widget.addWidget(welcome_page)

        # Step 1: Tool Selection
        self.tool_selector = ToolSelectorWidget()
        self.stacked_widget.addWidget(self.tool_selector)

        # Step 2: Material Matrix
        self.material_matrix = MaterialMatrixWidget()
        self.stacked_widget.addWidget(self.material_matrix)

        # Step 3: Operation Matrix
        self.operation_matrix = OperationMatrixWidget()
        self.stacked_widget.addWidget(self.operation_matrix)

        # Step 4: Results
        self.results_viewer = ResultsViewerWidget()
        self.stacked_widget.addWidget(self.results_viewer)

    def _create_welcome_page(self) -> QWidget:
        """Create welcome page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        layout.addStretch()

        # Welcome message
        welcome_label = QLabel("Willkommen!")
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        layout.addSpacing(20)

        # Instructions
        instructions = QLabel(
            "Dieser Assistent führt Sie durch die Berechnung:\n\n"
            "1. Importieren Sie eine .tools Datei\n"
            "2. Wählen Sie Werkzeuge\n"
            "3. Wählen Sie Materialien\n"
            "4. Wählen Sie Operationen\n"
            "5. Überprüfen Sie die Ergebnisse\n"
            "6. Exportieren Sie für Fusion 360"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        layout.addSpacing(30)

        # Import button
        import_button = QPushButton("📁 .tools Datei importieren")
        import_button.setStyleSheet("padding: 10px; font-size: 14px;")
        import_button.setMinimumWidth(250)
        import_button.clicked.connect(self._import_tools)
        layout.addWidget(import_button, alignment=Qt.AlignCenter)

        layout.addStretch()

        return page

    def _connect_signals(self):
        """Connect signals and slots."""
        self.tool_selector.selectionChanged.connect(self._update_navigation)
        self.material_matrix.selectionChanged.connect(self._update_navigation)
        self.operation_matrix.selectionChanged.connect(self._update_navigation)

    def _import_tools(self):
        """Import .tools file."""
        # FEATURE: Use default import directory
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Importiere .tools Datei",
            str(self.import_dir),  # Start in import/ directory
            "Fusion 360 Tools (*.tools)"
        )

        if not file_path:
            return

        try:
            file_path = Path(file_path)
            self.statusBar.showMessage(f"Importiere {file_path.name}...")
            self.tools = self.tools_reader.read_tools_file(file_path)

            # FEATURE: Remember imported file for smart export naming
            self.last_imported_file = file_path
            logger.info(f"Imported {file_path.name}, stored for export naming")

            self.statusBar.showMessage(
                f"{len(self.tools)} Werkzeuge geladen - Werkzeugauswahl", 3000
            )

            # Automatically go to next step
            self._go_next()

        except Exception as e:
            logger.error(f"Import failed: {e}", exc_info=True)
            QMessageBox.critical(
                self, "Import fehlgeschlagen", f"Fehler:\n{str(e)}"
            )

    def _go_next(self):
        """Go to next wizard step."""
        logger.info(f"_go_next called, current_step={self.current_step}")

        if self.current_step == 0:  # Welcome → Tool Selection
            self.tool_selector.set_tools(self.tools)
            self.current_step = 1

        elif self.current_step == 1:  # Tool Selection → Material Matrix
            selected_tools = self.tool_selector.get_selected_tools()
            logger.info(f"Selected {len(selected_tools)} tools")
            self.material_matrix.set_data(selected_tools, self.materials)
            self.current_step = 2

        elif self.current_step == 2:  # Material Matrix → Operation Matrix
            combinations = self.material_matrix.get_selected_combinations()
            # Extract unique tools (not tool×material combinations)
            unique_tools = []
            seen_tool_ids = set()
            for tool, mat_id in combinations:
                if tool.tool_id not in seen_tool_ids:
                    unique_tools.append(tool)
                    seen_tool_ids.add(tool.tool_id)

            logger.info(f"Passing {len(unique_tools)} unique tools to operation matrix (from {len(combinations)} tool-material combos)")
            # Pass only unique tools to operation matrix
            self.operation_matrix.set_data(unique_tools)
            self.current_step = 3

        elif self.current_step == 3:  # Operation Matrix → Results
            # Show calculate button instead of next
            return

        elif self.current_step == 4:  # Results → Export
            self._export_tools()
            return

        self.stacked_widget.setCurrentIndex(self.current_step)
        self._update_navigation()
        self._update_step_label()

    def _go_back(self):
        """Go to previous wizard step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.stacked_widget.setCurrentIndex(self.current_step)

            # Restore previous state when going back
            if self.current_step == 1:  # Back to Tool Selection
                # Tool selection is preserved automatically
                pass

            elif self.current_step == 2:  # Back to Material Matrix
                # Restore material matrix with current selections
                selected_tools = self.tool_selector.get_selected_tools()
                if selected_tools:
                    self.material_matrix.set_data(selected_tools, self.materials)

            elif self.current_step == 3:  # Back to Operation Matrix
                # Restore operation matrix with current selections
                combinations = self.material_matrix.get_selected_combinations()
                unique_tools = []
                seen_tool_ids = set()
                for tool, mat_id in combinations:
                    if tool.tool_id not in seen_tool_ids:
                        unique_tools.append(tool)
                        seen_tool_ids.add(tool.tool_id)
                if unique_tools:
                    self.operation_matrix.set_data(unique_tools)

            self._update_navigation()
            self._update_step_label()

    def _calculate_presets(self):
        """Calculate presets for all selected combinations."""
        # Get selected tool-operation combinations
        tool_op_selections = self.operation_matrix.get_selected_operations()

        # Get selected tool-material combinations from material matrix
        tool_mat_combinations = self.material_matrix.get_selected_combinations()

        if not tool_op_selections:
            QMessageBox.warning(
                self,
                "Keine Auswahl",
                "Bitte wählen Sie mindestens eine Operation aus."
            )
            return

        # Expand to full (tool, material, operation) combinations
        # For each tool-operation, calculate for ALL selected materials for that tool
        full_selections = []
        for tool, op_id in tool_op_selections:
            # Find all materials selected for this tool
            materials_for_tool = [mat_id for t, mat_id in tool_mat_combinations if t.tool_id == tool.tool_id]
            # Create combinations
            for mat_id in materials_for_tool:
                full_selections.append((tool, mat_id, op_id))

        if not full_selections:
            QMessageBox.warning(
                self,
                "Keine Materialkombinationen",
                "Keine Materialien für die ausgewählten Werkzeuge gefunden."
            )
            return

        logger.info(f"Expanded {len(tool_op_selections)} tool-op selections to {len(full_selections)} full combinations")

        # Create progress dialog
        progress = QProgressDialog(
            "Berechne Schnittdaten...", "Abbrechen", 0, len(full_selections), self
        )
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)

        # CRITICAL FIX: Clear old presets and track which tools are being calculated
        # This ensures we only export the tools that were just calculated, not old ones
        tools_being_calculated = []  # Use list instead of set (Tool not hashable)
        tools_seen = set()  # Track tool IDs we've seen

        for tool, _, _ in full_selections:
            if tool.tool_id not in tools_seen:
                # Clear any old presets from previous calculations
                tool.presets.clear()
                tools_being_calculated.append(tool)
                tools_seen.add(tool.tool_id)
                logger.info(f"Cleared old presets from {tool.tool_id} (number={tool.number}, description={tool.description[:50]})")

        # Calculate all presets
        calculated_count = 0
        for idx, (tool, mat_id, op_id) in enumerate(full_selections):
            if progress.wasCanceled():
                break

            progress.setValue(idx)
            # Get operation display name for progress
            op_config = OPERATIONS_CONFIG.get(op_id, {})
            op_name = op_config.get('display_name_short', op_id)
            progress.setLabelText(
                f"Berechne {tool.tool_id} - {mat_id} - {op_name}..."
            )

            try:
                # Calculate preset
                preset = self.calc_engine.calculate_preset(tool, mat_id, op_id)

                # Validate (NEW - using engine's validate method)
                validation_result = self.calc_engine.validate_preset(
                    preset, tool, mat_id, op_id
                )
                preset.validation_result = validation_result

                # Add to tool
                tool.presets.append(preset)
                calculated_count += 1

            except Exception as e:
                logger.error(
                    f"Failed to calculate {tool.tool_id}-{mat_id}-{op_id}: {e}",
                    exc_info=True
                )

        progress.setValue(len(full_selections))

        # Show results
        if calculated_count > 0:
            # CRITICAL FIX: Only show tools that were just calculated, not all tools
            tools_with_presets = list(tools_being_calculated)
            logger.info(f"Calculated presets for {len(tools_with_presets)} tools: {[(t.tool_id, t.number, len(t.presets)) for t in tools_with_presets]}")
            self.results_viewer.set_tools(tools_with_presets)

            self.current_step = 4
            self.stacked_widget.setCurrentIndex(self.current_step)
            self._update_navigation()
            self._update_step_label()

            # NO POPUP - just status message
            self.statusBar.showMessage(f"{calculated_count} Presets erfolgreich berechnet!", 5000)
        else:
            QMessageBox.warning(
                self,
                "Berechnung fehlgeschlagen",
                "Keine Presets konnten berechnet werden."
            )

    def _export_tools(self):
        """Export tools to .tools file."""
        # FEATURE: Generate smart filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if self.last_imported_file:
            # Use imported filename + timestamp
            base_name = self.last_imported_file.stem  # filename without extension
            default_filename = f"{base_name}_{timestamp}.tools"
        else:
            # Fallback to generic name
            default_filename = f"calculated_tools_{timestamp}.tools"

        # FEATURE: Use default export directory
        default_path = self.export_dir / default_filename

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exportiere .tools Datei",
            str(default_path),  # Start in export/ with timestamped name
            "Fusion 360 Tools (*.tools)",
        )

        if not file_path:
            return

        try:
            self.statusBar.showMessage("Exportiere...")

            tools_to_export = self.results_viewer.get_all_tools()
            self.tools_writer.write_tools_file(tools_to_export, Path(file_path))

            # NO POPUP - just status message
            preset_count = sum(len(t.presets) for t in tools_to_export)
            self.statusBar.showMessage(
                f"Export erfolgreich: {len(tools_to_export)} Werkzeuge, {preset_count} Presets → {Path(file_path).name}",
                8000
            )

        except Exception as e:
            logger.error(f"Export failed: {e}", exc_info=True)
            QMessageBox.critical(
                self, "Export fehlgeschlagen", f"Fehler:\n{str(e)}"
            )

    def _update_navigation(self):
        """Update navigation button states."""
        self.back_button.setEnabled(self.current_step > 0)

        # Update next button based on current step
        if self.current_step == 0:
            self.next_button.setVisible(True)
            self.next_button.setEnabled(len(self.tools) > 0)
            self.next_button.setText("Weiter →")
            self.calculate_button.setVisible(False)

        elif self.current_step == 1:
            self.next_button.setVisible(True)
            has_sel = self.tool_selector.has_selection()
            logger.info(f"Step 1 navigation update: has_selection={has_sel}")
            self.next_button.setEnabled(has_sel)
            self.next_button.setText("Weiter →")
            self.calculate_button.setVisible(False)

        elif self.current_step == 2:
            self.next_button.setVisible(True)
            self.next_button.setEnabled(self.material_matrix.has_selection())
            self.next_button.setText("Weiter →")
            self.calculate_button.setVisible(False)

        elif self.current_step == 3:
            self.next_button.setVisible(False)
            self.calculate_button.setVisible(True)
            self.calculate_button.setEnabled(self.operation_matrix.has_selection())

        elif self.current_step == 4:
            self.next_button.setVisible(True)
            self.next_button.setText("📤 Exportieren")
            self.next_button.setEnabled(True)
            self.calculate_button.setVisible(False)

    def _update_step_label(self):
        """Update step indicator label."""
        steps = [
            "Schritt 1/5: Import",
            "Schritt 2/5: Werkzeugauswahl",
            "Schritt 3/5: Materialauswahl",
            "Schritt 4/5: Operationsauswahl",
            "Schritt 5/5: Ergebnisse & Export",
        ]

        if 0 <= self.current_step < len(steps):
            self.step_label.setText(steps[self.current_step])
