"""
CNC-ToolCalc Backend - Main Calculation Service
Version: 0.0.1-alpha
Implementation: 10-Phase Calculation from V4 Architecture
"""

import math
from typing import Tuple
from backend.models.schemas import (
    Tool, CalculationRequest, CalculationResults,
    CoatingType, SurfaceQuality, CoolantType, OperationType
)
from backend.models.constants import (
    MATERIALS_MAP, OPERATIONS_MAP, COATING_FACTORS, SURFACE_QUALITY_FACTORS
)


class CalculationService:
    """
    10-Phase Calculation Engine (100% Cleanroom Implementation)

    Phase 1: Input Parameters (validation)
    Phase 2: vc + Coating Factor
    Phase 3: Spindle Speed (n)
    Phase 4: Chip Load (fz) + Dry Correction
    Phase 5: Feed Rate (vf)
    Phase 6: Engagement (ae, ap) + Surface Quality
    Phase 7: Power & Torque
    Phase 8: Thermal Analysis
    Phase 9: Chip Formation Prediction
    Phase 10: L/D Stability Check
    """

    def calculate(self, request: CalculationRequest, tool: Tool) -> CalculationResults:
        """Execute 10-phase calculation"""

        material = MATERIALS_MAP[request.material]
        operation = OPERATIONS_MAP[request.operation]

        # Phase 2: vc + Coating Factor
        vc_base = material.vc_base
        coating_factor = self._get_coating_factor(request.coating, request.material)
        vc_final = vc_base * coating_factor

        # Phase 3: Spindle Speed
        n_rpm = self._calculate_spindle_speed(vc_final, tool.geometry.DC)

        # Phase 4: Chip Load + Dry Correction
        fz_base = self._calculate_base_chipload(tool.geometry.DC, request.material, request.operation)
        dry_factor = material.dry_factor if request.coolant == CoolantType.DRY else 1.0
        fz_final = fz_base * dry_factor

        # Phase 5: Feed Rate
        vf_mm_min = n_rpm * fz_final * tool.geometry.NOF
        vf_entry = vf_mm_min * 0.5
        vf_ramp = vf_mm_min * 0.5
        vf_plunge = vf_mm_min / tool.geometry.NOF

        # Apply surface quality adjustment to vf
        sq_factors = SURFACE_QUALITY_FACTORS[request.surface_quality.value]
        vf_mm_min *= sq_factors["vf"]
        vf_entry *= sq_factors["vf"]
        vf_ramp *= sq_factors["vf"]
        vf_plunge *= sq_factors["vf"]

        # Phase 6: Engagement (ae, ap)
        ae_mm = self._calculate_ae(tool, operation, request.surface_quality)
        ap_mm, ap_reference = self._calculate_ap(tool, operation, request.surface_quality)

        # Phase 7: Power & Torque
        mrr = (ae_mm * ap_mm * vf_mm_min) / 1000  # cm³/min
        power_kw = (material.kc * ae_mm * ap_mm * vf_mm_min) / (60 * 1_000_000)
        torque_nm = (power_kw * 9550) / n_rpm if n_rpm > 0 else 0

        # Phase 8: Thermal Analysis
        chip_temp = self._calculate_chip_temperature(
            material, vc_final, fz_final, request.coolant
        )

        # Phase 9: Chip Formation
        chip_formation = self._predict_chip_formation(material, vc_final, fz_final)

        # Phase 10: L/D Stability
        ld_ratio = tool.ld_ratio
        ld_classification = tool.ld_classification
        stability_warnings = self._check_ld_stability(ld_ratio, ap_mm, tool.geometry.DC)

        return CalculationResults(
            tool=tool,
            material=request.material,
            operation=request.operation,
            vc_base=vc_base,
            coating_factor=coating_factor,
            vc_final=vc_final,
            n_rpm=n_rpm,
            fz_base=fz_base,
            dry_factor=dry_factor,
            fz_final=fz_final,
            vf_mm_min=vf_mm_min,
            vf_entry=vf_entry,
            vf_ramp=vf_ramp,
            vf_plunge=vf_plunge,
            ae_mm=ae_mm,
            ap_mm=ap_mm,
            ap_reference=ap_reference,
            mrr=mrr,
            power_kw=power_kw,
            torque_nm=torque_nm,
            chip_temperature_c=chip_temp,
            chip_formation=chip_formation,
            ld_ratio=ld_ratio,
            ld_classification=ld_classification,
            stability_warnings=stability_warnings,
        )

    def _get_coating_factor(self, coating: CoatingType, material) -> float:
        """Phase 2: Get coating multiplication factor"""
        factor = COATING_FACTORS[coating.value]

        # Diamond coating validation (non-ferrous only)
        if coating == CoatingType.DIAMOND:
            ferrous_materials = ["steel_mild", "steel_stainless"]
            if material.value in ferrous_materials:
                raise ValueError(
                    "Diamond coating can only be used with non-ferrous materials "
                    "(Wood, Plastic, Aluminium, Brass, Copper)"
                )

        return factor

    def _calculate_spindle_speed(self, vc: float, dc: float) -> int:
        """Phase 3: Calculate spindle speed (RPM)"""
        # n = (vc × 1000) / (π × DC)
        n = (vc * 1000) / (math.pi * dc)
        return int(round(n))

    def _calculate_base_chipload(self, dc: float, material, operation) -> float:
        """
        Phase 4: Calculate base chip load (fz)
        Simplified formula based on tool diameter and material
        """
        # Base fz depends on DC and material hardness
        # Softer materials allow higher fz

        # Base formula: fz = k × √DC where k depends on material
        material_k_factors = {
            "softwood": 0.15,
            "hardwood": 0.12,
            "acrylic": 0.10,
            "aluminium": 0.08,
            "brass": 0.07,
            "copper": 0.07,
            "steel_mild": 0.05,
            "steel_stainless": 0.04,
        }

        k = material_k_factors.get(material.value, 0.08)
        fz = k * math.sqrt(dc)

        # Clamp to reasonable values
        fz = max(0.01, min(fz, 0.5))

        return fz

    def _calculate_ae(self, tool: Tool, operation, surface_quality: SurfaceQuality) -> float:
        """Phase 6a: Calculate radial engagement (ae)"""
        ae_factor = operation.ae_factor
        ae_base = tool.geometry.DC * ae_factor

        # Apply surface quality adjustment
        sq_factors = SURFACE_QUALITY_FACTORS[surface_quality.value]
        ae_final = ae_base * sq_factors["ae"]

        return round(ae_final, 3)

    def _calculate_ap(
        self, tool: Tool, operation, surface_quality: SurfaceQuality
    ) -> Tuple[float, str]:
        """
        Phase 6b: Calculate axial depth (ap) with dynamic reference logic

        Returns: (ap_value, ap_reference)
        """
        ld_ratio = tool.ld_ratio

        # Determine ap reference (DC or LCF)
        if operation.ap_reference == "DC":
            ap_reference = "DC"
            ap_base = tool.geometry.DC * operation.ap_factor
        elif operation.ap_reference == "LCF":
            ap_reference = "LCF"
            ap_base = tool.geometry.LCF * operation.ap_factor
        else:  # "dynamic"
            # Dynamic logic based on L/D ratio
            if ld_ratio < 1.0:
                ap_reference = "DC"
                ap_base = tool.geometry.DC * 0.1875  # 18.75% of DC
            else:
                ap_reference = "LCF"
                ap_base = tool.geometry.LCF * 0.1875  # 18.75% of LCF

        # Apply surface quality adjustment
        sq_factors = SURFACE_QUALITY_FACTORS[surface_quality.value]
        ap_final = ap_base * sq_factors["ap"]

        return round(ap_final, 3), ap_reference

    def _calculate_chip_temperature(
        self, material, vc: float, fz: float, coolant: CoolantType
    ) -> float:
        """Phase 8: Calculate chip temperature"""
        # Base temperature from material max temp
        base_temp = material.max_temp * 0.4  # Start at 40% of max

        # vc influence (higher speed = higher temp)
        vc_factor = (vc / material.vc_base)
        temp = base_temp * (1 + 0.5 * vc_factor)

        # fz influence (higher chipload = slightly higher temp)
        fz_factor = fz / 0.1  # normalize to 0.1mm
        temp *= (1 + 0.1 * fz_factor)

        # Coolant reduction
        if coolant == CoolantType.WET:
            temp *= 0.7  # -30%
        elif coolant == CoolantType.MQL:
            temp *= 0.85  # -15%
        # DRY: no reduction

        return round(temp, 1)

    def _predict_chip_formation(self, material, vc: float, fz: float) -> str:
        """Phase 9: Predict chip formation type"""
        # Simplified chip formation prediction

        if material.category == "wood":
            return "dust" if fz < 0.05 else "segmented"

        if material.category == "plastic":
            return "continuous"

        # Metals
        if fz < 0.05:
            return "discontinuous"
        elif fz < 0.15:
            return "segmented"
        else:
            return "continuous"

    def _check_ld_stability(self, ld_ratio: float, ap: float, dc: float) -> list:
        """Phase 10: Check L/D stability and generate warnings"""
        warnings = []

        if ld_ratio > 6.0:
            warnings.append(
                f"Very long tool (L/D={ld_ratio:.2f} > 6.0): "
                "High risk of chatter and deflection. Consider reducing ap by 30-50%."
            )
        elif ld_ratio > 4.0:
            warnings.append(
                f"Long tool (L/D={ld_ratio:.2f} > 4.0): "
                "Increased risk of vibration. Consider reducing ap by 20%."
            )

        # Check if ap is too aggressive relative to DC
        if ap > dc * 0.75:
            warnings.append(
                f"Axial depth ({ap:.2f}mm) is very high relative to tool diameter ({dc:.2f}mm). "
                "Consider reducing to prevent tool breakage."
            )

        return warnings
