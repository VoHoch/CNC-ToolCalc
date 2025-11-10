"""Limit Manager - v2.0 3D-Matrix Limits System."""

import json
import logging
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class LimitManager:
    """Manage 3D-Matrix operation limits (Material × ToolType × Operation).

    Based on MASTER_SPECIFICATION v2.0 Section 5.

    Features:
    - Load operation limits from operation_limits.json
    - Apply L/D ratio adjustments for long tools
    - Handle missing combinations with fallback defaults
    """

    def __init__(self, config_dir: Path):
        """Initialize limit manager.

        Args:
            config_dir: Path to config directory containing operation_limits.json
        """
        self.config_dir = config_dir
        self.limits_data = self._load_limits()
        logger.debug("LimitManager initialized")

    def _load_limits(self) -> Dict:
        """Load operation limits from JSON file.

        Returns:
            Dict with structure: {Material: {ToolType: {Operation: limits}}}
        """
        limits_file = self.config_dir / "operation_limits.json"

        if not limits_file.exists():
            logger.error(f"operation_limits.json not found: {limits_file}")
            return {}

        try:
            with open(limits_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Remove comment fields
            data.pop("_comment", None)
            data.pop("_format", None)
            data.pop("_version", None)

            logger.info(f"Loaded limits for {len(data)} materials from {limits_file.name}")
            return data

        except Exception as e:
            logger.error(f"Failed to load operation_limits.json: {e}")
            return {}

    def get_limits(
        self,
        material_id: str,
        tool_type: str,
        operation_id: str
    ) -> Optional[Dict]:
        """Get operation limits for specific combination.

        Args:
            material_id: Material ID (e.g., "Aluminium")
            tool_type: Tool type (e.g., "end_mill", "ball_end_mill")
            operation_id: Operation ID (e.g., "PARTIAL_SLOT_OP")

        Returns:
            Dict with limits (ae_factor_max, ap_factor_max, mrr_max, etc.)
            None if combination not defined
        """
        try:
            limits = self.limits_data[material_id][tool_type][operation_id]
            logger.debug(
                f"Limits found: {material_id}/{tool_type}/{operation_id} → "
                f"ae_max={limits.get('ae_factor_max', 'N/A')}, "
                f"mrr_max={limits.get('mrr_max', 'N/A')}"
            )
            return limits.copy()  # Return copy to prevent modification

        except KeyError:
            logger.warning(
                f"No limits defined for {material_id}/{tool_type}/{operation_id}"
            )
            return None

    def apply_ld_ratio_adjustments(
        self,
        limits: Dict,
        ld_ratio: float
    ) -> Dict:
        """Apply L/D ratio adjustments to limits for long tools.

        Formula (MASTER_SPECIFICATION Section 5.5):
        - L/D ≤ 3.0: No adjustment (factor = 1.0)
        - L/D ≤ 4.0: Reduce by 10% (factor = 0.9)
        - L/D ≤ 5.0: Reduce by 20% (factor = 0.8)
        - L/D > 5.0:  Reduce by 30% (factor = 0.7)

        Applies to: ae_factor_max, ap_factor_max, vf_max_factor, mrr_max

        Args:
            limits: Original limits dict
            ld_ratio: L/D ratio of tool

        Returns:
            Adjusted limits dict
        """
        if ld_ratio <= 3.0:
            logger.debug(f"L/D={ld_ratio:.1f} ≤ 3.0 → No adjustment")
            return limits

        # Determine reduction factor
        if ld_ratio <= 4.0:
            factor = 0.9
        elif ld_ratio <= 5.0:
            factor = 0.8
        else:
            factor = 0.7

        logger.info(
            f"L/D={ld_ratio:.1f} > 3.0 → Reducing limits by {(1-factor)*100:.0f}% "
            f"(factor={factor})"
        )

        # Create adjusted copy
        adjusted = limits.copy()

        # Apply factor to key parameters
        ADJUSTABLE_PARAMS = [
            "ae_factor_max",
            "ae_factor_min",
            "ae_recommended",
            "ap_factor_max",
            "vf_max_factor",
            "mrr_max"
        ]

        for param in ADJUSTABLE_PARAMS:
            if param in adjusted:
                original = adjusted[param]
                adjusted[param] = original * factor
                logger.debug(f"  {param}: {original} → {adjusted[param]:.2f}")

        # DO NOT adjust fixed values (ap_fixed, ap_min_fixed)

        return adjusted

    def get_limits_with_ld_adjustment(
        self,
        material_id: str,
        tool_type: str,
        operation_id: str,
        ld_ratio: float
    ) -> Optional[Dict]:
        """Get limits with automatic L/D ratio adjustment.

        Convenience method combining get_limits() and apply_ld_ratio_adjustments().

        Args:
            material_id: Material ID
            tool_type: Tool type
            operation_id: Operation ID
            ld_ratio: L/D ratio of tool

        Returns:
            Adjusted limits dict or None if combination not defined
        """
        limits = self.get_limits(material_id, tool_type, operation_id)

        if limits is None:
            return None

        return self.apply_ld_ratio_adjustments(limits, ld_ratio)

    def get_default_limits(self, operation_id: str) -> Dict:
        """Get conservative default limits for undefined combinations.

        Used as fallback when specific Material×ToolType×Operation not defined.

        Args:
            operation_id: Operation ID

        Returns:
            Dict with conservative default limits
        """
        # Conservative defaults based on operation group
        FACE_OPS = ["ROUGH_FACE_OP", "FINISH_FACE_OP"]
        SLOT_OPS = ["PARTIAL_SLOT_OP", "FULL_SLOT_OP", "TROCHOIDAL_SLOT_OP", "FINISH_SLOT_OP"]
        FINISH_OPS = ["FINISH_SLOT_OP", "FINISH_FACE_OP"]

        if operation_id in FACE_OPS:
            defaults = {
                "ae_factor_max": 0.7,
                "ap_fixed": 1.0 if operation_id == "ROUGH_FACE_OP" else 0.2,
                "vf_max_factor": 1.0,
                "mrr_max": 200
            }
        elif operation_id in SLOT_OPS:
            defaults = {
                "ae_factor_max": 0.3,
                "ap_factor_max": 0.5,
                "ap_min_fixed": 0.5,
                "vf_max_factor": 1.0,
                "mrr_max": 200
            }
        elif operation_id in FINISH_OPS:
            defaults = {
                "ae_factor_max": 0.2,
                "ap_fixed": 0.2,
                "vf_max_factor": 1.0,
                "mrr_max": 50
            }
        else:
            # Ultra-conservative for unknown operations
            defaults = {
                "ae_factor_max": 0.2,
                "ap_factor_max": 0.3,
                "vf_max_factor": 0.8,
                "mrr_max": 100
            }

        logger.warning(
            f"Using default limits for {operation_id}: "
            f"ae_max={defaults.get('ae_factor_max')}, "
            f"mrr_max={defaults.get('mrr_max')}"
        )

        return defaults

    def get_mrr_max(
        self,
        material_id: str,
        tool_type: str,
        operation_id: str,
        ld_ratio: float = 1.0
    ) -> float:
        """Get maximum MRR for specific combination.

        Args:
            material_id: Material ID
            tool_type: Tool type
            operation_id: Operation ID
            ld_ratio: L/D ratio for adjustment (default: 1.0 = no adjustment)

        Returns:
            Maximum MRR in cm³/min
        """
        limits = self.get_limits_with_ld_adjustment(
            material_id, tool_type, operation_id, ld_ratio
        )

        if limits and "mrr_max" in limits:
            return limits["mrr_max"]

        # Fallback to default
        defaults = self.get_default_limits(operation_id)
        return defaults.get("mrr_max", 100)
