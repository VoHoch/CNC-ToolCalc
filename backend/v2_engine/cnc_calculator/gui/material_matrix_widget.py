"""Material matrix widget for selecting material-tool combinations."""

import logging
from typing import List, Dict
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QCheckBox,
    QPushButton,
    QHeaderView,
)
from PySide6.QtCore import Qt, Signal
from ..models import Tool, MaterialConfig

logger = logging.getLogger(__name__)


class MaterialMatrixWidget(QWidget):
    """Widget for selecting material-tool combinations.

    Displays a matrix where:
    - Rows = Tools
    - Columns = Materials
    - Cells = Checkboxes for enabling combination
    """

    selectionChanged = Signal()

    def __init__(self, parent=None):
        """Initialize material matrix widget."""
        super().__init__(parent)
        self.tools: List[Tool] = []
        self.materials: Dict[str, MaterialConfig] = {}
        self.checkboxes: Dict[tuple, QCheckBox] = {}  # (tool_id, material_id) -> checkbox
        self._init_ui()

    def _init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout(self)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("Material-Werkzeug Kombinationen:")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Quick selection buttons
        select_all_btn = QPushButton("Alle auswählen")
        select_all_btn.clicked.connect(self._select_all)
        header_layout.addWidget(select_all_btn)

        select_none_btn = QPushButton("Keine auswählen")
        select_none_btn.clicked.connect(self._select_none)
        header_layout.addWidget(select_none_btn)

        layout.addLayout(header_layout)

        # Info text
        info = QLabel(
            "Wählen Sie für jedes Werkzeug die zu berechnenden Materialien. "
            "Nur aktivierte Kombinationen werden berechnet."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #666;")
        layout.addWidget(info)

        # Table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(True)
        self.table.horizontalHeader().setVisible(True)

        # FEATURE: Add grid lines
        self.table.setShowGrid(True)
        self.table.setGridStyle(Qt.SolidLine)

        # FEATURE: Enable cell clicking to toggle checkboxes
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setFocusPolicy(Qt.StrongFocus)
        self.table.cellClicked.connect(self._on_cell_clicked)

        # FEATURE: Increase text size
        self.table.setStyleSheet("""
            QTableWidget {
                font-size: 13px;
                gridline-color: #CCCCCC;
            }
            QHeaderView::section {
                font-size: 12px;
                font-weight: bold;
                padding: 6px;
            }
            QCheckBox {
                background: transparent;
                border: none;
                outline: none;
                spacing: 0px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #666;
                border-radius: 4px;
                background: white;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #2196F3;
            }
            QCheckBox::indicator:checked {
                background: #2196F3;
                border: 2px solid #2196F3;
            }
            QCheckBox::indicator:checked:hover {
                background: #1976D2;
                border: 2px solid #1976D2;
            }
        """)

        # Enable scrollbars when content exceeds size
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        layout.addWidget(self.table)

        # Info label
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("color: #888; font-style: italic;")
        layout.addWidget(self.info_label)

    def set_data(self, tools: List[Tool], materials: Dict[str, MaterialConfig]):
        """Set tools and materials for the matrix.

        Args:
            tools: List of selected Tool objects
            materials: Dictionary of material configurations
        """
        # Save current selections before rebuilding
        old_selections = {}
        for (tool_id, mat_id), checkbox in self.checkboxes.items():
            old_selections[(tool_id, mat_id)] = checkbox.isChecked()

        self.tools = tools
        self.materials = materials
        self.checkboxes = {}

        self._build_matrix()

        # Restore previous selections
        for (tool_id, mat_id), was_checked in old_selections.items():
            if (tool_id, mat_id) in self.checkboxes:
                self.checkboxes[(tool_id, mat_id)].setChecked(was_checked)

        self._update_info()

        logger.info(
            f"Built material matrix: {len(tools)} tools × {len(materials)} materials "
            f"(restored {len(old_selections)} previous selections)"
        )

    def _build_matrix(self):
        """Build the material matrix table."""
        if not self.tools or not self.materials:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        # Set dimensions
        self.table.setRowCount(len(self.tools))
        self.table.setColumnCount(len(self.materials))

        # Set headers
        material_ids = list(self.materials.keys())
        self.table.setHorizontalHeaderLabels(material_ids)
        self.table.setVerticalHeaderLabels([t.tool_id for t in self.tools])

        # Populate cells with checkboxes
        for row, tool in enumerate(self.tools):
            for col, mat_id in enumerate(material_ids):
                # Create centered checkbox widget
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.setAlignment(Qt.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)

                checkbox = QCheckBox()

                # Smart default: suggest materials based on tool
                should_suggest = self._should_suggest_material(tool, mat_id)
                checkbox.setChecked(should_suggest)

                # Visual hint for suggested materials
                if should_suggest:
                    checkbox.setStyleSheet("background-color: #e8f5e9;")  # Light green

                checkbox.stateChanged.connect(self._on_selection_changed)

                checkbox_layout.addWidget(checkbox)
                self.table.setCellWidget(row, col, checkbox_widget)

                # Store reference
                self.checkboxes[(tool.tool_id, mat_id)] = checkbox

        # Adjust column widths - use ResizeToContents for compact table
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Add material color indicators in header
        for col, mat_id in enumerate(material_ids):
            material = self.materials[mat_id]
            # Create colored header item
            header_item = QTableWidgetItem(mat_id)
            # material is dict, use display_name from dict
            header_item.setToolTip(material.get("display_name", mat_id))
            # Note: Header item color styling is limited in Qt
            self.table.setHorizontalHeaderItem(col, header_item)

    def _on_selection_changed(self):
        """Handle selection change."""
        self._update_info()
        self.selectionChanged.emit()

    def _select_all(self):
        """Select all combinations."""
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)

    def _select_none(self):
        """Deselect all combinations."""
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)

    def _update_info(self):
        """Update info label."""
        selected = self.get_selected_count()
        total = len(self.checkboxes)

        if total == 0:
            self.info_label.setText("Keine Daten geladen")
        else:
            self.info_label.setText(
                f"{selected} von {total} Kombinationen ausgewählt"
            )

    def get_selected_combinations(self) -> List[tuple]:
        """Get list of selected (tool, material) combinations.

        Returns:
            List of (Tool, material_id) tuples
        """
        combinations = []
        for (tool_id, mat_id), checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                # Find tool object
                tool = next((t for t in self.tools if t.tool_id == tool_id), None)
                if tool:
                    combinations.append((tool, mat_id))

        return combinations

    def get_selected_count(self) -> int:
        """Get count of selected combinations.

        Returns:
            Number of checked checkboxes
        """
        return sum(1 for cb in self.checkboxes.values() if cb.isChecked())

    def has_selection(self) -> bool:
        """Check if any combinations are selected.

        Returns:
            True if at least one combination is selected
        """
        return any(cb.isChecked() for cb in self.checkboxes.values())

    def _on_cell_clicked(self, row: int, col: int):
        """Handle cell click to toggle checkbox.

        Args:
            row: Row index
            col: Column index
        """
        # Get tool and material ID from row/col
        if row >= len(self.tools):
            return

        tool = self.tools[row]
        material_ids = list(self.materials.keys())
        if col >= len(material_ids):
            return

        mat_id = material_ids[col]

        # Toggle the checkbox
        checkbox = self.checkboxes.get((tool.tool_id, mat_id))
        if checkbox:
            checkbox.setChecked(not checkbox.isChecked())

    def _should_suggest_material(self, tool: Tool, material_id: str) -> bool:
        """
        Determine if a material should be suggested for this tool.

        Smart defaults based on:
        - Tool body material (HSS vs. VHM)
        - Tool type
        - Keywords in description
        - Best practices

        Args:
            tool: Tool object
            material_id: Material ID (e.g., "Aluminium")

        Returns:
            True if material should be pre-selected
        """

        tool_type = tool.type.value if hasattr(tool.type, 'value') else str(tool.type)
        desc_lower = tool.description.lower() if tool.description else ""

        # Rule 1: Check for material keywords in tool description
        if "wood" in desc_lower or "holz" in desc_lower:
            return material_id in ["Hardwood", "Softwood"]

        if "steel" in desc_lower or "stahl" in desc_lower:
            return material_id in ["Steel", "Stainless"]

        if "alu" in desc_lower:
            return material_id == "Aluminium"

        # Rule 2: Tool body material (if available)
        if hasattr(tool, 'body_material_code'):
            if tool.body_material_code == "hss":
                # HSS: Only soft materials
                return material_id in ["Aluminium", "Hardwood", "Softwood", "Plastic", "Brass"]

            elif tool.body_material_code == "carbide":
                # VHM/Carbide: All materials possible
                return True  # All materials

        # Rule 3: Tool type specific suggestions
        if tool_type == "thread_mill":
            # Threading: All materials
            return True

        if tool_type in ["drill", "spot_drill"]:
            # Drilling: Common materials
            return material_id in ["Aluminium", "Steel", "Plastic", "Brass", "Hardwood", "Softwood"]

        if tool_type == "ball_end_mill":
            # Ball end: Softer materials for 3D work
            return material_id in ["Aluminium", "Hardwood", "Softwood", "Plastic"]

        if tool_type == "face_mill":
            # Face mill: All except very hard
            return material_id != "Stainless"

        if tool_type in ["flat_end_mill", "bull_nose_end_mill"]:
            # Standard end mills: Most versatile - suggest common materials
            return material_id in ["Aluminium", "Hardwood", "Softwood", "Plastic", "Brass"]

        if tool_type == "chamfer_mill":
            # Chamfer: All materials
            return True

        if tool_type == "radius_mill":
            # Radius mill: Common materials
            return material_id in ["Aluminium", "Hardwood", "Softwood", "Plastic"]

        # Default: Suggest common, easy-to-machine materials
        return material_id in ["Aluminium", "Hardwood", "Softwood", "Plastic"]
