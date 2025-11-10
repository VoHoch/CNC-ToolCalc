"""Operation matrix widget for selecting operations per tool-material combination."""

import logging
import json
from typing import List, Dict, Tuple
from pathlib import Path
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
    QGroupBox,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from ..models import Tool

logger = logging.getLogger(__name__)

# Load operations config
OPERATIONS_CONFIG_PATH = Path(__file__).parent.parent / "config" / "operations.json"
with open(OPERATIONS_CONFIG_PATH, 'r', encoding='utf-8') as f:
    OPERATIONS_CONFIG = json.load(f)

# Ordered list of operation IDs (12 operations in user-requested order)
# Order: SLOT → FACE → CONTOUR → SPECIAL
OPERATION_IDS = [
    # SLOT (4) - Full → Partial → Trochoidal → Finish
    "FULL_SLOT_OP",
    "PARTIAL_SLOT_OP",
    "TROCHOIDAL_SLOT_OP",
    "FINISH_SLOT_OP",
    # FACE (2) - Rough → Finish
    "ROUGH_FACE_OP",
    "FINISH_FACE_OP",
    # CONTOUR (3) - Radius → Chamfer → Ball3D
    "RADIUS_CONTOUR_OP",
    "CHAMFER_CONTOUR_OP",
    "BALL_3D_OP",
    # SPECIAL (3) - Drilling → VGroove → Threading
    "DRILLING_OP",
    "VGROOVE_OP",
    "THREADING_OP",
]

# Category structure for headers
OPERATION_CATEGORIES = [
    ("SLOT", ["FULL_SLOT_OP", "PARTIAL_SLOT_OP", "TROCHOIDAL_SLOT_OP", "FINISH_SLOT_OP"]),
    ("FACE", ["ROUGH_FACE_OP", "FINISH_FACE_OP"]),
    ("CONTOUR", ["RADIUS_CONTOUR_OP", "CHAMFER_CONTOUR_OP", "BALL_3D_OP"]),
    ("SPECIAL", ["DRILLING_OP", "VGROOVE_OP", "THREADING_OP"]),
]


class OperationMatrixWidget(QWidget):
    """Widget for selecting operations per tool.

    Displays a table where:
    - Rows = Tools (e.g., "T1 - Sorotec Planfräser")
    - Columns = 12 Operations (e.g., "Contour: Finish")
    - Cells = Checkboxes for enabling each combination
    """

    selectionChanged = Signal()

    def __init__(self, parent=None):
        """Initialize operation matrix widget."""
        super().__init__(parent)
        self.tools: List[Tool] = []  # List of tools
        self.checkboxes: Dict[Tuple[str, str], QCheckBox] = {}  # (tool_id, operation_id) -> checkbox
        self._init_ui()

    def _init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout(self)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("Operationen auswählen:")
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
            "Wählen Sie für jedes Werkzeug die gewünschten Operationen. "
            "💡 Intelligente Vorschläge sind vorausgewählt basierend auf Werkzeugtyp."
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
                color: white;
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

    def set_data(self, tools: List[Tool]):
        """Set tools for the matrix.

        Args:
            tools: List of Tool objects
        """
        # Save current selections before rebuilding
        old_selections = {}
        for (tool_id, op_id), checkbox in self.checkboxes.items():
            old_selections[(tool_id, op_id)] = checkbox.isChecked()

        self.tools = tools
        self.checkboxes = {}

        self._build_matrix()

        # Restore previous selections
        for (tool_id, op_id), was_checked in old_selections.items():
            if (tool_id, op_id) in self.checkboxes:
                self.checkboxes[(tool_id, op_id)].setChecked(was_checked)

        self._update_info()

        logger.info(
            f"Built operation matrix: {len(tools)} tools × {len(OPERATION_IDS)} operations "
            f"(restored {len(old_selections)} previous selections)"
        )

    def _build_matrix(self):
        """Build the operation matrix table."""
        if not self.tools:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        # Set dimensions
        self.table.setRowCount(len(self.tools))
        self.table.setColumnCount(len(OPERATION_IDS))

        # FEATURE: Set column headers with category prefixes
        column_headers = []
        for op_id in OPERATION_IDS:
            op_config = OPERATIONS_CONFIG[op_id]
            # Find category for this operation
            category_name = ""
            for cat_name, cat_ops in OPERATION_CATEGORIES:
                if op_id in cat_ops:
                    category_name = cat_name
                    break

            # Format: "SLOT: Full" or "FACE: Rough"
            header_text = f"{category_name}:\n{op_config['display_name_short']}"
            column_headers.append(header_text)

        self.table.setHorizontalHeaderLabels(column_headers)

        # FEATURE: Style headers by category with background colors
        header = self.table.horizontalHeader()
        category_colors = {
            "SLOT": "#EF5350",      # Red - better contrast
            "FACE": "#42A5F5",      # Blue - better contrast
            "CONTOUR": "#66BB6A",   # Green - better contrast
            "SPECIAL": "#FFA726",   # Orange - better contrast
        }

        for col, op_id in enumerate(OPERATION_IDS):
            # Find category
            for cat_name, cat_ops in OPERATION_CATEGORIES:
                if op_id in cat_ops:
                    # Create header item with styling
                    header_item = QTableWidgetItem(column_headers[col])
                    header_item.setBackground(QColor(category_colors.get(cat_name, "#FFFFFF")))
                    header_item.setToolTip(f"{cat_name} Operations")
                    self.table.setHorizontalHeaderItem(col, header_item)
                    break

        # Set row headers (tools only, no materials)
        row_headers = []
        for tool in self.tools:
            row_headers.append(f"{tool.tool_id}")
        self.table.setVerticalHeaderLabels(row_headers)

        # Populate cells with checkboxes
        for row, tool in enumerate(self.tools):
            for col, op_id in enumerate(OPERATION_IDS):
                # Create centered checkbox widget
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.setAlignment(Qt.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)

                checkbox = QCheckBox()

                # Intelligent default selection based on tool type only (not material)
                should_select = self._should_suggest_operation_for_tool(tool, op_id)
                checkbox.setChecked(should_select)

                # Visual hint for suggested operations
                if should_select:
                    checkbox.setStyleSheet("background-color: #e8f5e9;")  # Light green

                checkbox.stateChanged.connect(self._on_selection_changed)

                checkbox_layout.addWidget(checkbox)
                self.table.setCellWidget(row, col, checkbox_widget)

                # Store reference (no material_id needed)
                self.checkboxes[(tool.tool_id, op_id)] = checkbox

        # Adjust column widths
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def _should_suggest_operation_for_tool(self, tool: Tool, operation_id: str) -> bool:
        """
        Determine if an operation should be suggested for this tool.

        Smart defaults based on tool type only.

        Args:
            tool: Tool object
            operation_id: Operation ID (e.g., "FINISH_SLOT_OP")

        Returns:
            True if operation should be pre-selected
        """

        tool_type = tool.type.value if hasattr(tool.type, 'value') else str(tool.type)

        # Special tool types with specific operations
        if tool_type == "thread_mill":
            return operation_id == "THREADING_OP"

        if tool_type == "drill" or tool_type == "spot_drill":
            return operation_id == "DRILLING_OP"

        if tool_type == "chamfer_mill":
            return operation_id in ["CHAMFER_CONTOUR_OP", "VGROOVE_OP"]

        if tool_type == "face_mill":
            return operation_id in ["ROUGH_FACE_OP", "FINISH_FACE_OP"]

        if tool_type == "ball_end_mill":
            return operation_id in ["BALL_3D_OP"]

        if tool_type == "radius_mill":
            return operation_id == "RADIUS_CONTOUR_OP"

        # Standard end mills - most versatile
        if tool_type in ["flat_end_mill", "bull_nose_end_mill"]:
            return operation_id in ["PARTIAL_SLOT_OP", "FINISH_SLOT_OP", "ROUGH_FACE_OP", "FINISH_FACE_OP", "TROCHOIDAL_SLOT_OP"]

        # Default: select common operations
        return operation_id in ["PARTIAL_SLOT_OP", "FINISH_SLOT_OP", "ROUGH_FACE_OP"]

    def _should_suggest_operation(self, tool: Tool, material_id: str, operation_id: str) -> bool:
        """
        Determine if an operation should be suggested for this tool-material combination.

        Smart defaults based on:
        - Tool type
        - Material properties
        - Best practices

        Args:
            tool: Tool object
            material_id: Material ID (e.g., "Aluminium")
            operation_id: Operation ID (e.g., "FINISH_SLOT_OP")

        Returns:
            True if operation should be pre-selected
        """

        tool_type = tool.type.value if hasattr(tool.type, 'value') else str(tool.type)

        # Special tool types with specific operations
        if tool_type == "thread_mill":
            return operation_id == "THREADING_OP"

        if tool_type == "drill" or tool_type == "spot_drill":
            return operation_id == "DRILLING_OP"

        if tool_type == "chamfer_mill":
            return operation_id in ["CHAMFER_CONTOUR_OP", "VGROOVE_OP"]

        if tool_type == "face_mill":
            return operation_id in ["ROUGH_FACE_OP", "FINISH_FACE_OP"]

        if tool_type == "ball_end_mill":
            return operation_id in ["BALL_3D_OP"]

        if tool_type == "radius_mill":
            return operation_id == "RADIUS_CONTOUR_OP"

        # Standard end mills - most versatile
        if tool_type in ["flat_end_mill", "bull_nose_end_mill"]:
            # Base suggestions
            suggestions = ["PARTIAL_SLOT_OP", "FINISH_SLOT_OP", "ROUGH_FACE_OP", "FINISH_FACE_OP"]

            # Material-specific additions
            if material_id in ["Hardwood", "Softwood", "Aluminium", "Plastic"]:
                # Softer materials: more aggressive operations OK
                suggestions.extend(["TROCHOIDAL_SLOT_OP"])
            elif material_id in ["Steel", "Stainless"]:
                # Harder materials: avoid full slot, prefer trochoidal
                suggestions.extend(["TROCHOIDAL_SLOT_OP"])
            else:
                # Brass, Copper: moderate
                suggestions.extend(["TROCHOIDAL_SLOT_OP"])

            return operation_id in suggestions

        # Default: select common operations
        return operation_id in ["PARTIAL_SLOT_OP", "FINISH_SLOT_OP", "ROUGH_FACE_OP"]

    def _on_selection_changed(self):
        """Handle selection change."""
        self._update_info()
        self.selectionChanged.emit()

    def _on_cell_clicked(self, row: int, col: int):
        """Handle cell click to toggle checkbox.

        Args:
            row: Row index
            col: Column index
        """
        # Get tool and operation ID from row/col
        if row >= len(self.tools):
            return

        tool = self.tools[row]
        if col >= len(OPERATION_IDS):
            return

        op_id = OPERATION_IDS[col]

        # Toggle the checkbox
        checkbox = self.checkboxes.get((tool.tool_id, op_id))
        if checkbox:
            checkbox.setChecked(not checkbox.isChecked())

    def _select_all(self):
        """Select all operations."""
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)

    def _select_none(self):
        """Deselect all operations."""
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
                f"{selected} von {total} Operationen ausgewählt"
            )

    def get_selected_operations(self) -> List[Tuple[Tool, str]]:
        """Get list of selected (tool, operation_id) combinations.

        Returns:
            List of (Tool, operation_id) tuples
        """
        selected = []
        for (tool_id, op_id), checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                # Find tool object
                tool = next((t for t in self.tools if t.tool_id == tool_id), None)
                if tool:
                    selected.append((tool, op_id))

        return selected

    def get_selected_count(self) -> int:
        """Get count of selected operations.

        Returns:
            Number of checked checkboxes
        """
        return sum(1 for cb in self.checkboxes.values() if cb.isChecked())

    def has_selection(self) -> bool:
        """Check if any operations are selected.

        Returns:
            True if at least one operation is selected
        """
        return any(cb.isChecked() for cb in self.checkboxes.values())
