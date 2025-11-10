"""Tool selector widget for choosing tools to calculate."""

import logging
from typing import List
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QCheckBox,
    QPushButton,
    QFrame,
    QGroupBox,
)
from PySide6.QtCore import Qt, Signal
from ..models import Tool

logger = logging.getLogger(__name__)


class ToolSelectorWidget(QWidget):
    """Widget for selecting tools to process.

    Displays a list of tools with checkboxes for selection.
    """

    selectionChanged = Signal()  # Emitted when selection changes

    def __init__(self, parent=None):
        """Initialize tool selector widget."""
        super().__init__(parent)
        self.tools: List[Tool] = []
        self.tool_checkboxes: List[QCheckBox] = []
        self._init_ui()

    def _init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout(self)

        # FEATURE: Checkbox styling for better visibility
        self.setStyleSheet("""
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

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("Wählen Sie die zu berechnenden Werkzeuge:")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Select all/none buttons
        select_all_btn = QPushButton("Alle auswählen")
        select_all_btn.clicked.connect(self._select_all)
        header_layout.addWidget(select_all_btn)

        select_none_btn = QPushButton("Keine auswählen")
        select_none_btn.clicked.connect(self._select_none)
        header_layout.addWidget(select_none_btn)

        layout.addLayout(header_layout)

        # Scroll area for tool list
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.StyledPanel)

        self.tools_container = QWidget()
        self.tools_layout = QVBoxLayout(self.tools_container)
        self.tools_layout.setAlignment(Qt.AlignTop)

        scroll_area.setWidget(self.tools_container)
        layout.addWidget(scroll_area)

        # Info label
        self.info_label = QLabel("Keine Werkzeuge geladen")
        self.info_label.setStyleSheet("color: #888; font-style: italic;")
        layout.addWidget(self.info_label)

    def set_tools(self, tools: List[Tool]):
        """Set the list of available tools.

        Args:
            tools: List of Tool objects
        """
        self.tools = tools
        self.tool_checkboxes = []

        # Clear existing widgets
        while self.tools_layout.count():
            item = self.tools_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Create checkbox for each tool
        for tool in tools:
            tool_widget = self._create_tool_widget(tool)
            self.tools_layout.addWidget(tool_widget)

        # Update info
        self._update_info()

        logger.info(f"Loaded {len(tools)} tools into selector")

    def _create_tool_widget(self, tool: Tool) -> QWidget:
        """Create widget for a single tool.

        Args:
            tool: Tool object

        Returns:
            Widget displaying tool information
        """
        group = QGroupBox()
        layout = QHBoxLayout(group)

        # FEATURE: Make entire row clickable
        group.setCursor(Qt.PointingHandCursor)
        group.mousePressEvent = lambda event, t=tool: self._on_row_clicked(t, event)

        # Checkbox
        checkbox = QCheckBox()
        checkbox.setChecked(tool.selected)
        checkbox.stateChanged.connect(lambda state, t=tool: self._on_tool_toggled(t, state))
        self.tool_checkboxes.append(checkbox)
        layout.addWidget(checkbox)

        # Store reference for toggling
        checkbox.tool_ref = tool

        # Tool info
        info_layout = QVBoxLayout()

        # Main description
        desc_label = QLabel(f"<b>{tool.tool_id}</b>: {tool.description}")
        info_layout.addWidget(desc_label)

        # Details
        details = (
            f"Typ: {tool.type.value} | "
            f"Ø {tool.geometry.DC}mm | "
            f"{tool.geometry.NOF} Schneiden | "
            f"Schnittlänge: {tool.geometry.LCF}mm | "
            f"L/D: {tool.calculate_ld_ratio():.1f}"
        )
        details_label = QLabel(details)
        details_label.setStyleSheet("color: #666; font-size: 11px;")
        info_layout.addWidget(details_label)

        # Vendor info if available
        if tool.vendor != "Generic":
            vendor_label = QLabel(f"Hersteller: {tool.vendor}")
            vendor_label.setStyleSheet("color: #888; font-size: 10px;")
            info_layout.addWidget(vendor_label)

        layout.addLayout(info_layout)
        layout.addStretch()

        return group

    def _on_row_clicked(self, tool: Tool, event):
        """Handle click anywhere on the row.

        Args:
            tool: Tool that was clicked
            event: Mouse event
        """
        # Find the checkbox for this tool and toggle it
        for checkbox in self.tool_checkboxes:
            if hasattr(checkbox, 'tool_ref') and checkbox.tool_ref == tool:
                checkbox.setChecked(not checkbox.isChecked())
                break

    def _on_tool_toggled(self, tool: Tool, state: int):
        """Handle tool checkbox toggle.

        Args:
            tool: Tool that was toggled
            state: New checkbox state
        """
        # Check if checkbox is checked (state == 2 for Qt.CheckState.Checked)
        tool.selected = bool(state)
        self._update_info()
        self.selectionChanged.emit()
        logger.debug(f"Tool {tool.tool_id} toggled: selected={tool.selected}")

    def _select_all(self):
        """Select all tools."""
        for checkbox in self.tool_checkboxes:
            checkbox.setChecked(True)

    def _select_none(self):
        """Deselect all tools."""
        for checkbox in self.tool_checkboxes:
            checkbox.setChecked(False)

    def _update_info(self):
        """Update info label."""
        selected_count = sum(1 for tool in self.tools if tool.selected)
        total_count = len(self.tools)

        if total_count == 0:
            self.info_label.setText("Keine Werkzeuge geladen")
        else:
            self.info_label.setText(
                f"{selected_count} von {total_count} Werkzeugen ausgewählt"
            )

    def get_selected_tools(self) -> List[Tool]:
        """Get list of selected tools.

        Returns:
            List of selected Tool objects
        """
        return [tool for tool in self.tools if tool.selected]

    def has_selection(self) -> bool:
        """Check if any tools are selected.

        Returns:
            True if at least one tool is selected
        """
        return any(tool.selected for tool in self.tools)
