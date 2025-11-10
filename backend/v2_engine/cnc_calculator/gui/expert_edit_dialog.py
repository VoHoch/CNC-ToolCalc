"""Expert edit dialog for manual adjustment of cutting data."""

import logging
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QDoubleSpinBox,
    QPushButton,
    QGroupBox,
    QDialogButtonBox,
    QRadioButton,
    QButtonGroup,
)
from PySide6.QtCore import Qt
from ..models import Tool, Preset

logger = logging.getLogger(__name__)


class ExpertEditDialog(QDialog):
    """Dialog for expert editing of preset values.

    Features:
    - Quick presets (Conservative/Standard/Aggressive)
    - Manual value adjustment
    - Live calculation preview
    """

    def __init__(self, tool: Tool, preset: Preset, parent=None):
        """Initialize expert edit dialog.

        Args:
            tool: Tool object for context
            preset: Preset to edit (will be modified in-place if accepted)
            parent: Parent widget
        """
        super().__init__(parent)
        self.tool = tool
        self.preset = preset
        self.original_preset = preset.model_copy(deep=True)  # Backup

        self._init_ui()
        self._load_values()

    def _init_ui(self):
        """Initialize user interface."""
        self.setWindowTitle(f"Expert Edit - {self.preset.name}")
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)

        # Title
        title = QLabel(f"<h2>{self.preset.name}</h2>")
        layout.addWidget(title)

        tool_info = QLabel(
            f"{self.tool.tool_id}: {self.tool.description} "
            f"(Ø {self.tool.geometry.DC}mm, {self.tool.geometry.NOF} Schneiden)"
        )
        tool_info.setStyleSheet("color: #666;")
        layout.addWidget(tool_info)

        layout.addSpacing(10)

        # Quick presets
        preset_group = QGroupBox("Schnellauswahl")
        preset_layout = QHBoxLayout(preset_group)

        self.preset_buttons = QButtonGroup(self)

        self.radio_conservative = QRadioButton("Konservativ (-30%)")
        self.radio_standard = QRadioButton("Standard (berechnet)")
        self.radio_aggressive = QRadioButton("Aggressiv (+50%)")

        self.radio_standard.setChecked(True)

        self.preset_buttons.addButton(self.radio_conservative, 0)
        self.preset_buttons.addButton(self.radio_standard, 1)
        self.preset_buttons.addButton(self.radio_aggressive, 2)

        preset_layout.addWidget(self.radio_conservative)
        preset_layout.addWidget(self.radio_standard)
        preset_layout.addWidget(self.radio_aggressive)

        self.preset_buttons.buttonClicked.connect(self._apply_preset)

        layout.addWidget(preset_group)

        # Manual adjustment
        manual_group = QGroupBox("Manuelle Anpassung")
        form_layout = QFormLayout(manual_group)

        # vc
        self.vc_spin = QDoubleSpinBox()
        self.vc_spin.setRange(10, 1000)
        self.vc_spin.setDecimals(1)
        self.vc_spin.setSuffix(" m/min")
        self.vc_spin.valueChanged.connect(self._recalculate)
        form_layout.addRow("Schnittgeschwindigkeit (vc):", self.vc_spin)

        # fz
        self.fz_spin = QDoubleSpinBox()
        self.fz_spin.setRange(0.001, 1.0)
        self.fz_spin.setDecimals(4)
        self.fz_spin.setSuffix(" mm")
        self.fz_spin.setSingleStep(0.001)
        self.fz_spin.valueChanged.connect(self._recalculate)
        form_layout.addRow("Vorschub pro Zahn (fz):", self.fz_spin)

        # ae
        self.ae_spin = QDoubleSpinBox()
        self.ae_spin.setRange(0.1, 100)
        self.ae_spin.setDecimals(2)
        self.ae_spin.setSuffix(" mm")
        self.ae_spin.valueChanged.connect(self._recalculate)
        form_layout.addRow("Radiale Zustellung (ae):", self.ae_spin)

        # ap
        self.ap_spin = QDoubleSpinBox()
        self.ap_spin.setRange(0.1, 100)
        self.ap_spin.setDecimals(2)
        self.ap_spin.setSuffix(" mm")
        self.ap_spin.setMaximum(self.tool.geometry.LCF)  # Cannot exceed LCF
        self.ap_spin.valueChanged.connect(self._recalculate)
        form_layout.addRow("Axiale Zustellung (ap):", self.ap_spin)

        layout.addWidget(manual_group)

        # Calculated values (read-only)
        calc_group = QGroupBox("Berechnete Werte")
        calc_layout = QFormLayout(calc_group)

        self.rpm_label = QLabel()
        calc_layout.addRow("Drehzahl (n):", self.rpm_label)

        self.vf_label = QLabel()
        calc_layout.addRow("Vorschubgeschwindigkeit (vf):", self.vf_label)

        layout.addWidget(calc_group)

        # Reset button
        reset_button = QPushButton("↺ Zurücksetzen")
        reset_button.clicked.connect(self._reset)
        layout.addWidget(reset_button)

        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _load_values(self):
        """Load preset values into UI."""
        self.vc_spin.setValue(self.preset.vc_final)
        self.fz_spin.setValue(self.preset.fz_final)
        self.ae_spin.setValue(self.preset.ae_mm)
        self.ap_spin.setValue(self.preset.ap_mm)
        self._update_calculated_values()

    def _apply_preset(self, button: QRadioButton):
        """Apply quick preset.

        Args:
            button: Selected radio button
        """
        button_id = self.preset_buttons.id(button)

        if button_id == 0:  # Conservative
            factor = 0.70
        elif button_id == 1:  # Standard
            factor = 1.00
        elif button_id == 2:  # Aggressive
            factor = 1.50
        else:
            return

        # Apply factor to original values
        self.vc_spin.setValue(self.original_preset.vc_final * factor)
        self.fz_spin.setValue(self.original_preset.fz_final * factor)
        self.ae_spin.setValue(self.original_preset.ae_mm * factor)
        self.ap_spin.setValue(min(
            self.original_preset.ap_mm * factor,
            self.tool.geometry.LCF
        ))

    def _recalculate(self):
        """Recalculate dependent values."""
        self._update_calculated_values()

    def _update_calculated_values(self):
        """Update calculated RPM and vf display."""
        import math

        # Get current values
        vc = self.vc_spin.value()
        fz = self.fz_spin.value()
        dc = self.tool.geometry.DC
        nof = self.tool.geometry.NOF

        # Calculate RPM
        n_rpm = (vc * 1000) / (math.pi * dc)

        # Clamp to limits
        n_rpm = max(2000, min(24000, n_rpm))

        # Calculate vf
        vf = fz * nof * n_rpm

        # Update labels
        self.rpm_label.setText(f"{n_rpm:.0f} rpm")
        self.vf_label.setText(f"{vf:.0f} mm/min")

    def _reset(self):
        """Reset to original values."""
        self.vc_spin.setValue(self.original_preset.vc_final)
        self.fz_spin.setValue(self.original_preset.fz_final)
        self.ae_spin.setValue(self.original_preset.ae_mm)
        self.ap_spin.setValue(self.original_preset.ap_mm)
        self.radio_standard.setChecked(True)

    def accept(self):
        """Apply changes and close dialog."""
        import math

        # Update preset with new values
        vc = self.vc_spin.value()
        fz = self.fz_spin.value()
        ae = self.ae_spin.value()
        ap = self.ap_spin.value()

        # Calculate dependent values
        n_rpm = (vc * 1000) / (math.pi * self.tool.geometry.DC)
        n_rpm = max(2000, min(24000, n_rpm))
        vf = fz * self.tool.geometry.NOF * n_rpm

        # Update preset
        self.preset.vc_final = vc
        self.preset.fz_final = fz
        self.preset.ae_mm = ae
        self.preset.ap_mm = ap
        self.preset.n_rpm = n_rpm
        self.preset.vf_mm_per_min = vf
        self.preset.manually_edited = True

        # Note: Expression regeneration would happen here in full implementation

        logger.info(f"Preset manually edited: {self.preset.name}")

        super().accept()

    def reject(self):
        """Cancel changes and close dialog."""
        logger.info(f"Edit cancelled: {self.preset.name}")
        super().reject()
