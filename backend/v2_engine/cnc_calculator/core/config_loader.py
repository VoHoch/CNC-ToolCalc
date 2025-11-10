"""Configuration loader for JSON config files."""

import json
from pathlib import Path
from typing import Dict
from ..models import MaterialConfig, OperationConfig


class ConfigLoader:
    """Loads configuration from JSON files."""

    def __init__(self, config_dir: Path):
        """Initialize config loader.

        Args:
            config_dir: Path to config directory
        """
        self.config_dir = config_dir

    def load_materials(self) -> Dict[str, MaterialConfig]:
        """Load material configurations.

        Returns:
            Dictionary mapping material ID to MaterialConfig
        """
        config_path = self.config_dir / "materials.json"
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        materials = {}
        for mat_id, mat_data in data.items():
            materials[mat_id] = MaterialConfig(**mat_data)

        return materials

    def load_operations(self) -> Dict[str, OperationConfig]:
        """Load operation configurations.

        Returns:
            Dictionary mapping operation name to OperationConfig
        """
        config_path = self.config_dir / "operations.json"
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        operations = {}
        for op_name, op_data in data.items():
            operations[op_name] = OperationConfig(**op_data)

        return operations

    def load_tool_types(self) -> Dict[str, dict]:
        """Load tool type factors.

        Returns:
            Dictionary mapping tool type to factor dict
        """
        config_path = self.config_dir / "tool_types.json"
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_spindle_config(self) -> dict:
        """Load spindle configuration.

        Returns:
            Spindle configuration dictionary
        """
        config_path = self.config_dir / "spindle_config.json"
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_calculation_params(self) -> dict:
        """Load calculation parameters.

        Returns:
            Calculation parameters dictionary
        """
        config_path = self.config_dir / "calculation_params.json"
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_sorotec_reference(self) -> dict:
        """Load Sorotec reference data.

        Returns:
            Sorotec reference data dictionary
        """
        config_path = self.config_dir / "sorotec_reference.json"
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
