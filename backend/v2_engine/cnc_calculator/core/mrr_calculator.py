"""MRR (Material Removal Rate) and Power calculator - v2.0."""

import logging
from typing import Dict

logger = logging.getLogger(__name__)


class MRRCalculator:
    """Calculate Material Removal Rate and required spindle power.

    Based on MASTER_SPECIFICATION v2.0 Section 5.4.

    MRR = (ae * ap * vf) / 1000  [cm3/min]
    Power = (MRR * k_c) / 60     [kW]
    """

    def __init__(self, materials: Dict):
        """Initialize calculator with material properties.

        Args:
            materials: Material configuration dict with k_c values
        """
        self.materials = materials
        logger.debug("MRRCalculator initialized")

    def calculate_mrr(self, ae_mm: float, ap_mm: float, vf_mm_per_min: float) -> float:
        """Calculate Material Removal Rate.

        Formula: MRR = (ae * ap * vf) / 1000

        Args:
            ae_mm: Radial depth of cut [mm]
            ap_mm: Axial depth of cut [mm]
            vf_mm_per_min: Feed rate [mm/min]

        Returns:
            float: MRR in cm3/min
        """
        # MRR in cm3/min
        mrr = (ae_mm * ap_mm * vf_mm_per_min) / 1000

        logger.debug(
            f"MRR calculation: ae={ae_mm:.2f}mm * ap={ap_mm:.2f}mm * "
            f"vf={vf_mm_per_min:.0f}mm/min = {mrr:.0f} cm3/min"
        )

        return mrr

    def calculate_power(self, mrr: float, material_id: str) -> float:
        """Calculate required spindle power.

        Formula: Power = (MRR * k_c) / 60000

        Where:
        - MRR is in cm3/min
        - k_c is in N/mm2
        - Result is in kW

        The 60000 factor accounts for:
        - 60 (seconds per minute)
        - 1000 (mm3 per cm3)

        Args:
            mrr: Material Removal Rate [cm3/min]
            material_id: Material ID (e.g., "Aluminium")

        Returns:
            float: Required power in kW
        """
        # Get specific cutting force
        k_c = self.materials[material_id].get("k_c", 700)

        # Power in kW
        # Formula: P = (MRR [cm3/min] * k_c [N/mm2]) / 60000
        power = (mrr * k_c) / 60000

        logger.debug(
            f"Power calculation: MRR={mrr:.0f} cm3/min * k_c={k_c} N/mm2 "
            f"/ 60000 = {power:.2f} kW"
        )

        return power

    def get_mrr_max(self, material_id: str) -> float:
        """Get maximum MRR for material at 6kW spindle.

        Args:
            material_id: Material ID (e.g., "Aluminium")

        Returns:
            float: Maximum MRR in cm3/min
        """
        mrr_max = self.materials[material_id].get("MRR_max_6kW", 500)

        logger.debug(f"MRR max for {material_id}: {mrr_max} cm3/min")

        return mrr_max

    def check_limits(
        self,
        ae_mm: float,
        ap_mm: float,
        vf_mm_per_min: float,
        material_id: str,
        spindle_power_kw: float = 6.0
    ) -> tuple[bool, float, float, str]:
        """Check if MRR and Power are within limits.

        Args:
            ae_mm: Radial depth of cut [mm]
            ap_mm: Axial depth of cut [mm]
            vf_mm_per_min: Feed rate [mm/min]
            material_id: Material ID
            spindle_power_kw: Available spindle power [kW], default 6.0

        Returns:
            tuple: (is_safe, mrr, power, message)
                - is_safe: True if within limits
                - mrr: Calculated MRR [cm3/min]
                - power: Required power [kW]
                - message: Error/warning message or empty string
        """
        # Calculate MRR and Power
        mrr = self.calculate_mrr(ae_mm, ap_mm, vf_mm_per_min)
        power = self.calculate_power(mrr, material_id)

        # Get limits
        mrr_max = self.get_mrr_max(material_id)

        # Check MRR limit
        if mrr > mrr_max:
            vf_max_safe = (mrr_max * 1000) / (ae_mm * ap_mm)
            message = (
                f"WARNING: MRR {mrr:.0f} cm3/min exceeds limit {mrr_max} cm3/min! "
                f"Reduce vf to max {vf_max_safe:.0f} mm/min"
            )
            logger.warning(message)
            return False, mrr, power, message

        # Check Power limit
        if power > spindle_power_kw:
            message = (
                f"WARNING: Power {power:.1f}kW exceeds spindle {spindle_power_kw}kW! "
                f"Reduce MRR!"
            )
            logger.warning(message)
            return False, mrr, power, message

        # Warning if close to limit (>80%)
        if power > spindle_power_kw * 0.8:
            message = (
                f"CAUTION: Power {power:.1f}kW near spindle limit {spindle_power_kw}kW"
            )
            logger.info(message)
            return True, mrr, power, message

        # All good
        logger.debug(
            f"Limits OK: MRR={mrr:.0f}/{mrr_max} cm3/min, "
            f"Power={power:.1f}/{spindle_power_kw} kW"
        )
        return True, mrr, power, ""
