"""Results viewer widget for displaying calculated presets."""

import logging
from typing import List, Dict
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QPushButton,
    QTextEdit,
    QSplitter,
)
from PySide6.QtCore import Qt, Signal
from ..models import Tool, Preset, ValidationStatus

logger = logging.getLogger(__name__)


class ResultsViewerWidget(QWidget):
    """Widget for viewing and reviewing calculated presets.

    Displays results in a tree structure with validation indicators.
    """

    editRequested = Signal(Tool, Preset)  # Emitted when user wants to edit a preset

    def __init__(self, parent=None):
        """Initialize results viewer widget."""
        super().__init__(parent)
        self.tools: List[Tool] = []
        self._init_ui()

    def _init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout(self)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("Berechnete Schnittdaten:")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Expand/collapse buttons
        expand_btn = QPushButton("Alle aufklappen")
        expand_btn.clicked.connect(self._expand_all)
        header_layout.addWidget(expand_btn)

        collapse_btn = QPushButton("Alle zuklappen")
        collapse_btn.clicked.connect(self._collapse_all)
        header_layout.addWidget(collapse_btn)

        layout.addLayout(header_layout)

        # Info text
        info = QLabel(
            "Überprüfen Sie die berechneten Werte. "
            "🟢 = SICHER (alle Grenzwerte OK), 🟡 = WARNUNG (nahe an Grenzen), "
            "🔴 = GEFAHR (Grenzwerte überschritten!)"
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #666;")
        layout.addWidget(info)

        # Splitter for tree and details
        splitter = QSplitter(Qt.Vertical)

        # Tree widget for results
        self.tree = QTreeWidget()
        # FEATURE: Show Fusion 360 field names in header with German labels
        # f_n removed as requested - it's redundant (calculated from f_z * NOF)
        self.tree.setHeaderLabels(
            [
                "Werkzeug / Preset",
                "v_c\n(m/min)",
                "n\n(rpm)",
                "f_z\nVorschub/Zahn\n(mm)",
                "v_f\nSchnitt\n(mm/min)",
                "Eintritt\n(× v_f)",
                "Austritt\n(× v_f)",
                "Einstechen\n(× v_f)",
                "Rampe\n(× v_f)",
                "Rampenwinkel\n(deg)",
                "ae\nQuer\n(mm)",
                "ap\nTiefe\n(mm)",
                "Kühlmittel",
                "Status"
            ]
        )
        self.tree.setAlternatingRowColors(True)
        self.tree.itemSelectionChanged.connect(self._on_selection_changed)

        # Enable scrollbars when content exceeds size
        self.tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tree.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        splitter.addWidget(self.tree)

        # Details panel
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)

        details_title = QLabel("Details:")
        details_title.setStyleSheet("font-weight: bold;")
        details_layout.addWidget(details_title)

        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMaximumHeight(150)
        details_layout.addWidget(self.details_text)

        splitter.addWidget(details_widget)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)

        # Info label
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("color: #888; font-style: italic;")
        layout.addWidget(self.info_label)

    def set_tools(self, tools: List[Tool]):
        """Set tools with calculated presets.

        Args:
            tools: List of Tool objects with presets
        """
        self.tools = tools
        self._build_tree()
        self._update_info()

        logger.info(f"Displaying results for {len(tools)} tools")

    def _build_tree(self):
        """Build the results tree."""
        self.tree.clear()

        if not self.tools:
            return

        for tool in self.tools:
            # Tool node
            tool_item = QTreeWidgetItem(self.tree)
            tool_item.setText(0, f"{tool.tool_id}: {tool.description}")
            tool_item.setText(
                1, f"Ø {tool.geometry.DC}mm"
            )
            tool_item.setExpanded(True)

            # Store tool reference
            tool_item.setData(0, Qt.UserRole, ("tool", tool))

            # Preset nodes - sorted alphabetically by name
            sorted_presets = sorted(tool.presets, key=lambda p: p.name)
            for preset in sorted_presets:
                preset_item = QTreeWidgetItem(tool_item)
                preset_item.setText(0, f"  {preset.name}")
                # FEATURE: Show values as exported to Fusion 360
                # f_n removed - redundant (calculated from f_z * NOF)
                preset_item.setText(1, f"{preset.vc_final:.1f}")  # v_c
                preset_item.setText(2, f"{preset.n_rpm:.0f}")  # n
                preset_item.setText(3, f"{preset.fz_final:.4f}")  # f_z
                preset_item.setText(4, f"{preset.vf_mm_per_min:.0f}")  # v_f
                # Vorschub-Faktoren (mit Bezugswert in Header: × v_f)
                preset_item.setText(5, f"{preset.feed_entry:.3f}")
                preset_item.setText(6, f"{preset.feed_exit:.3f}")
                preset_item.setText(7, f"{preset.feed_plunge:.3f}")
                preset_item.setText(8, f"{preset.feed_ramp:.3f}")
                # Rampenwinkel aus expressions extrahieren
                ramp_angle_str = preset.expressions.get("tool_rampAngle", "3.0 deg")
                ramp_angle = ramp_angle_str.split()[0]  # "3.0 deg" → "3.0"
                preset_item.setText(9, ramp_angle)
                # Zustellungen
                preset_item.setText(10, f"{preset.ae_mm:.2f}")  # ae
                preset_item.setText(11, f"{preset.ap_mm:.2f}")  # ap
                preset_item.setText(12, "disabled")  # Kühlmittel

                # Validation status
                if preset.validation_result:
                    status_icon = preset.validation_result.get_icon()
                    preset_item.setText(13, status_icon)
                    preset_item.setToolTip(13, preset.validation_result.get_summary())
                else:
                    preset_item.setText(13, "⚪")

                # Store preset reference
                preset_item.setData(0, Qt.UserRole, ("preset", tool, preset))

        # Adjust column widths
        for i in range(self.tree.columnCount()):
            self.tree.resizeColumnToContents(i)

    def _on_selection_changed(self):
        """Handle tree selection change."""
        selected_items = self.tree.selectedItems()
        if not selected_items:
            self.details_text.clear()
            return

        item = selected_items[0]
        data = item.data(0, Qt.UserRole)

        if not data:
            self.details_text.clear()
            return

        data_type = data[0]

        if data_type == "tool":
            tool = data[1]
            self._show_tool_details(tool)
        elif data_type == "preset":
            tool, preset = data[1], data[2]
            self._show_preset_details(tool, preset)

    def _show_tool_details(self, tool: Tool):
        """Show tool details.

        Args:
            tool: Tool object
        """
        # Format holder info if available
        holder_info = ""
        if tool.holder:
            holder_info = f"""
<b>Halter:</b><br>
• Typ: {tool.holder.product_id if hasattr(tool.holder, 'product_id') else 'N/A'}<br>
• Länge: {tool.holder.HL if hasattr(tool.holder, 'HL') else 'N/A'} mm<br>
"""

        details = f"""
<h3>{tool.tool_id}: {tool.description}</h3>

<b>Allgemein:</b><br>
• GUID: {tool.guid}<br>
• Typ: {tool.type.value}<br>
• Hersteller: {tool.vendor}<br>
• Werkzeugmaterial: {tool.body_material_code.upper()}<br>
• Einheit: {tool.unit}<br>

<b>Geometrie:</b><br>
• Durchmesser (DC): {tool.geometry.DC} mm<br>
• Schneidenlänge (LCF): {tool.geometry.LCF} mm<br>
• Gesamtlänge (OAL): {tool.geometry.OAL} mm<br>
• Schaftdurchmesser (SHAFT_DIAMETER): {tool.geometry.SHAFT_DIAMETER} mm<br>
• Anzahl Schneiden (NOF): {tool.geometry.NOF}<br>
• L/D Verhältnis: {tool.calculate_ld_ratio():.2f}<br>
• Eckenradius (RE): {tool.geometry.RE if tool.geometry.RE else '0'} mm<br>
• Spitzenwinkel (SIG): {tool.geometry.SIG if tool.geometry.SIG else 'N/A'}°<br>

{holder_info}

<b>Berechnete Presets:</b> {len(tool.presets)}<br>
<i>Klicken Sie auf ein Preset für Details</i>
"""
        self.details_text.setHtml(details)

    def _show_preset_details(self, tool: Tool, preset: Preset):
        """Show preset details.

        Args:
            tool: Tool object
            preset: Preset object
        """
        details = f"""
<h3>{preset.name}</h3>

<b>An Fusion 360 übergeben (Top-Level Werte):</b><br>
• v_c = {preset.vc_final:.1f} m/min<br>
• n = {preset.n_rpm:.0f} rpm<br>
• n_ramp = {preset.n_rpm:.0f} rpm<br>
• f_z = {preset.fz_final:.4f} mm<br>
• v_f = {preset.vf_mm_per_min:.0f} mm/min<br>
• v_f_leadIn = {preset.vf_mm_per_min * preset.feed_entry:.0f} mm/min<br>
• v_f_leadOut = {preset.vf_mm_per_min * preset.feed_exit:.0f} mm/min<br>
• v_f_plunge = {preset.vf_mm_per_min * preset.feed_plunge:.0f} mm/min<br>
• v_f_ramp = {preset.vf_mm_per_min * preset.feed_ramp:.0f} mm/min<br>
• v_f_transition = {preset.vf_mm_per_min * preset.feed_transition:.0f} mm/min<br>
• stepover = {preset.ae_mm:.2f} mm<br>
• stepdown = {preset.ap_mm:.2f} mm<br>
• tool-coolant = disabled<br>

<b>Fusion 360 Expressions (Parametrisch):</b><br>
"""
        # Add all expressions
        if preset.expressions:
            for key, value in sorted(preset.expressions.items()):
                details += f"• {key} = {value}<br>"
        else:
            details += "<i>Keine Expressions</i><br>"

        details += f"""
<br>
<b>Berechnungsgrundlage:</b><br>
• vc Basis: {preset.vc_base:.1f} m/min → Final: {preset.vc_final:.1f} m/min<br>
• fz Basis: {preset.fz_base:.4f} mm → Final: {preset.fz_final:.4f} mm<br>
• ae: {preset.ae_mm:.2f} mm ({preset.ae_mm/tool.geometry.DC*100:.0f}% von DC)<br>
• ap: {preset.ap_mm:.2f} mm ({preset.ap_mm/tool.geometry.LCF*100:.0f}% von LCF)<br>

<b>Vorschubfaktoren:</b><br>
• Eintritt: {preset.feed_entry:.3f}<br>
• Austritt: {preset.feed_exit:.3f}<br>
• Rampe: {preset.feed_ramp:.3f}<br>
• Einstechen: {preset.feed_plunge:.3f}<br>
• Übergang: {preset.feed_transition:.3f}<br>
"""

        # Add validation info if available
        if preset.validation_result:
            val = preset.validation_result
            details += f"""
<br>
<b>Validierung v2.0:</b> {val.get_icon()} {val.get_summary()}<br>
"""
            # v2.0: Show MRR and Power
            if val.mrr_calculated is not None:
                details += f"• MRR: {val.mrr_calculated:.1f} cm³/min<br>"
            if val.power_calculated is not None:
                details += f"• Leistung: {val.power_calculated:.2f} kW (Spindel: 6.0 kW)<br>"
            if val.ld_ratio is not None:
                details += f"• L/D Verhältnis: {val.ld_ratio:.1f}<br>"

            # v1.0: Sorotec reference (if available)
            if val.sorotec_ref_vc:
                details += f"• Sorotec Referenz vc: {val.sorotec_ref_vc} m/min (Abweichung: {val.vc_delta_pct:+.1f}%)<br>"
            if val.sorotec_ref_fz:
                details += f"• Sorotec Referenz fz: {val.sorotec_ref_fz} mm (Abweichung: {val.fz_delta_pct:+.1f}%)<br>"

            if val.errors:
                details += "<br><b>❌ Fehler (NICHT SICHER!):</b><br>"
                for error in val.errors:
                    details += f"• {error}<br>"

            if val.warnings:
                details += "<br><b>⚠️ Warnungen:</b><br>"
                for warning in val.warnings:
                    details += f"• {warning}<br>"

            if val.recommendations:
                details += "<br><b>💡 Empfehlungen:</b><br>"
                for rec in val.recommendations:
                    details += f"• {rec}<br>"

        # Add expressions info
        expr_count = len(preset.expressions)
        details += f"""
<br>
<b>Fusion 360 Expressions:</b> {expr_count}/13
"""
        if expr_count < 13:
            details += " ⚠️ <span style='color: red;'>UNVOLLSTÄNDIG!</span>"

        self.details_text.setHtml(details)

    def _expand_all(self):
        """Expand all tree items."""
        self.tree.expandAll()

    def _collapse_all(self):
        """Collapse all tree items."""
        self.tree.collapseAll()

    def _update_info(self):
        """Update info label."""
        total_presets = sum(len(tool.presets) for tool in self.tools)

        # Count by validation status
        green_count = 0
        yellow_count = 0
        red_count = 0
        pending_count = 0

        for tool in self.tools:
            for preset in tool.presets:
                if preset.validation_result:
                    status = preset.validation_result.status
                    if status == ValidationStatus.GREEN:
                        green_count += 1
                    elif status == ValidationStatus.YELLOW:
                        yellow_count += 1
                    elif status == ValidationStatus.RED:
                        red_count += 1
                    else:
                        pending_count += 1
                else:
                    pending_count += 1

        info_text = (
            f"{total_presets} Presets berechnet | "
            f"🟢 {green_count} | 🟡 {yellow_count} | 🔴 {red_count} | "
            f"⚪ {pending_count}"
        )

        self.info_label.setText(info_text)

    def get_all_tools(self) -> List[Tool]:
        """Get all tools with their presets.

        Returns:
            List of Tool objects
        """
        return self.tools
