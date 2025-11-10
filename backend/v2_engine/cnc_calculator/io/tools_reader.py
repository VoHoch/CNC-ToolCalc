"""Reader for Fusion 360 .tools files."""

import json
import zipfile
from pathlib import Path
from typing import List
import logging
from ..models import Tool, Geometry, Holder, PostProcess, ToolType

logger = logging.getLogger(__name__)


class ToolsReader:
    """Reads .tools files (Fusion 360 format).

    .tools files are ZIP archives containing:
    - tool library.json (main tool data)
    - Possibly other metadata files
    """

    def read_tools_file(self, file_path: Path) -> List[Tool]:
        """Read .tools file and extract tool data.

        Args:
            file_path: Path to .tools file

        Returns:
            List of Tool objects (geometry only, no cutting data yet)

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not file_path.suffix == ".tools":
            raise ValueError(f"Expected .tools file, got: {file_path.suffix}")

        logger.info(f"Reading .tools file: {file_path}")

        try:
            with zipfile.ZipFile(file_path, "r") as zf:
                # Read the main tool library JSON
                # Try both common filenames
                json_filename = None
                for name in zf.namelist():
                    if name.endswith('.json'):
                        json_filename = name
                        break

                if not json_filename:
                    raise ValueError("No JSON file found in .tools archive")

                logger.debug(f"Reading JSON file: {json_filename}")
                with zf.open(json_filename) as f:
                    data = json.load(f)

            tools = self._parse_tools_data(data)
            logger.info(f"Successfully loaded {len(tools)} tools")
            return tools

        except Exception as e:
            logger.error(f"Failed to read .tools file: {e}")
            raise

    def _parse_tools_data(self, data: dict) -> List[Tool]:
        """Parse tool data from JSON.

        Args:
            data: Tool library JSON data

        Returns:
            List of Tool objects (sorted by tool number)
        """
        tools = []
        tool_data_list = data.get("data", [])

        for idx, tool_data in enumerate(tool_data_list):
            try:
                # CRITICAL FIX: Extract actual tool number from post-process
                # Don't use array index, use the real tool number!
                actual_number = tool_data.get("post-process", {}).get("number", idx + 1)
                tool = self._parse_single_tool(tool_data, actual_number)
                tools.append(tool)
                logger.debug(f"Loaded tool #{actual_number}: {tool_data.get('description', 'N/A')[:50]}")
            except Exception as e:
                logger.warning(f"Skipping tool at index {idx}: {e}")

        # CRITICAL FIX: Sort tools by post-process number
        # This ensures that T2 in the UI actually refers to Tool #2, not array index 2
        tools.sort(key=lambda t: t.number)
        logger.info(f"Sorted {len(tools)} tools by tool number (1-{len(tools)})")

        return tools

    def _parse_single_tool(self, tool_data: dict, number: int) -> Tool:
        """Parse a single tool from JSON data.

        Args:
            tool_data: Tool JSON data
            number: Tool number (for fallback)

        Returns:
            Tool object
        """
        # Extract basic info
        guid = tool_data.get("guid", "")
        description = tool_data.get("description", f"Tool {number}")
        vendor = tool_data.get("vendor", "Generic")
        product_id = tool_data.get("product-id", "")
        product_link = tool_data.get("product-link", "")

        # Extract tool type
        tool_type_str = tool_data.get("type", "flat end mill")
        try:
            tool_type = ToolType(tool_type_str)
        except ValueError:
            logger.warning(f"Unknown tool type '{tool_type_str}', using flat end mill")
            tool_type = ToolType.FLAT_END_MILL

        # Parse geometry
        geometry = self._parse_geometry(tool_data.get("geometry", {}))

        # Parse holder
        holder = self._parse_holder(tool_data.get("holder", {}))

        # Parse post-process
        post_process = self._parse_post_process(
            tool_data.get("post-process", {}), number
        )

        # Create tool ID
        tool_id = f"T{number}"

        return Tool(
            guid=guid or None,  # Will generate new UUID if empty
            tool_id=tool_id,
            number=number,
            description=description,
            vendor=vendor,
            product_id=product_id,
            product_link=product_link,
            type=tool_type,
            unit=tool_data.get("unit", "millimeters"),
            body_material_code=tool_data.get("BMC", "carbide"),
            grade=tool_data.get("grade", "Mill Generic"),
            geometry=geometry,
            holder=holder,
            post_process=post_process,
            presets=[],  # Will be calculated later
            selected=False,
            # CRITICAL: Store complete raw tool data for 1:1 export
            raw_data=tool_data,
        )

    def _parse_geometry(self, geom_data: dict) -> Geometry:
        """Parse geometry data.

        Args:
            geom_data: Geometry JSON data

        Returns:
            Geometry object
        """
        return Geometry(
            DC=geom_data.get("DC", 6.0),
            DCX=geom_data.get("DCX", 6.0),
            NOF=geom_data.get("NOF", 2),
            LCF=geom_data.get("LCF", 20.0),
            shoulder_diameter=geom_data.get("shoulder-diameter", 6.0),
            shoulder_length=geom_data.get("shoulder-length", 20.0),
            OAL=geom_data.get("OAL"),
            LB=geom_data.get("LB"),
            SFDM=geom_data.get("SFDM"),
            RE=geom_data.get("RE", 0.0),
            TA=geom_data.get("TA", 0.0),
            tip_angle=geom_data.get("TA") if "TA" in geom_data else None,
        )

    def _parse_holder(self, holder_data: dict) -> Holder:
        """Parse holder data.

        Args:
            holder_data: Holder JSON data

        Returns:
            Holder object
        """
        # Extract diameter from segments if present (for Fusion 360 holders with segments)
        diameter = holder_data.get("diameter", 6.0)
        if "segments" in holder_data and holder_data["segments"]:
            # Use upper-diameter of first segment as representative diameter
            diameter = holder_data["segments"][0].get("upper-diameter", diameter)

        # Extract length from gaugeLength if present
        length = holder_data.get("gaugeLength", holder_data.get("length", 50.0))

        return Holder(
            description=holder_data.get("description", "Generic Holder"),
            vendor=holder_data.get("vendor", "Generic"),
            product_id=holder_data.get("product-id", ""),
            product_link=holder_data.get("product-link", ""),
            diameter=diameter,
            length=length,
            # CRITICAL: Store complete raw data for 1:1 export
            raw_data=holder_data if holder_data else None,
        )

    def _parse_post_process(self, pp_data: dict, number: int) -> PostProcess:
        """Parse post-process data.

        Args:
            pp_data: Post-process JSON data
            number: Tool number for defaults

        Returns:
            PostProcess object
        """
        return PostProcess(
            comment=pp_data.get("comment", ""),
            number=pp_data.get("number", number),
            diameter_offset=pp_data.get("diameter-offset", number),
            length_offset=pp_data.get("length-offset", number),
            manual_tool_change=pp_data.get("manual-tool-change", False),
            break_control=pp_data.get("break-control", False),
            clockwise=pp_data.get("clockwise", True),
        )
