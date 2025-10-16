"""Mito Handler for data analysis and manipulation."""

import json
import logging
from pathlib import Path
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


class MitoHandler:
    """Handler for Mito-based data analysis operations.
    
    This class provides functionality to:
    - Load and analyze data from various sources
    - Generate Python code for data transformations
    - Create visualizations
    - Export analysis results
    """

    def __init__(self, workspace_dir: Optional[str] = None):
        """Initialize Mito Handler.
        
        Args:
            workspace_dir: Directory to store analysis files and exports
        """
        self.workspace_dir = Path(workspace_dir) if workspace_dir else Path("./mito_workspace")
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"MitoHandler initialized with workspace: {self.workspace_dir}")

    async def analyze_data_request(self, user_message: str, context: dict) -> dict:
        """Analyze user's data analysis request.
        
        Args:
            user_message: User's message describing the analysis needed
            context: Additional context (file paths, data sources, etc.)
            
        Returns:
            Dictionary containing analysis type, suggested actions, and data preview
        """
        analysis_result = {
            "request_type": self._classify_request(user_message),
            "suggested_actions": [],
            "requires_data": True,
            "data_preview": None,
        }

        # Check if user provided data file path
        if "file_path" in context:
            file_path = context["file_path"]
            analysis_result["data_preview"] = await self._load_and_preview_data(file_path)
            analysis_result["suggested_actions"] = self._suggest_actions(
                user_message, 
                analysis_result["data_preview"]
            )

        return analysis_result

    def _classify_request(self, message: str) -> str:
        """Classify the type of data analysis request.
        
        Args:
            message: User's message
            
        Returns:
            Request type (e.g., 'visualization', 'transformation', 'aggregation')
        """
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['plot', 'chart', 'graph', 'visualiz', 'show']):
            return "visualization"
        elif any(word in message_lower for word in ['filter', 'select', 'where', 'remove']):
            return "filtering"
        elif any(word in message_lower for word in ['group', 'aggregate', 'sum', 'average', 'count']):
            return "aggregation"
        elif any(word in message_lower for word in ['merge', 'join', 'combine']):
            return "merge"
        elif any(word in message_lower for word in ['pivot', 'reshape', 'transpose']):
            return "reshaping"
        elif any(word in message_lower for word in ['clean', 'fill', 'missing', 'null']):
            return "cleaning"
        else:
            return "general_analysis"

    async def _load_and_preview_data(self, file_path: str, rows: int = 5) -> dict:
        """Load data file and return preview.
        
        Args:
            file_path: Path to data file (CSV, Excel, etc.)
            rows: Number of rows to preview
            
        Returns:
            Dictionary with data info and preview
        """
        try:
            # Determine file type and load accordingly
            file_path_obj = Path(file_path)
            
            if file_path_obj.suffix.lower() == '.csv':
                df = pd.read_csv(file_path)
            elif file_path_obj.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            elif file_path_obj.suffix.lower() == '.json':
                df = pd.read_json(file_path)
            else:
                return {"error": f"Unsupported file type: {file_path_obj.suffix}"}

            preview = {
                "columns": df.columns.tolist(),
                "shape": df.shape,
                "dtypes": df.dtypes.astype(str).to_dict(),
                "preview": df.head(rows).to_dict('records'),
                "missing_values": df.isnull().sum().to_dict(),
                "file_path": str(file_path),
            }
            
            logger.info(f"Loaded data from {file_path}: shape {df.shape}")
            return preview

        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {e}")
            return {"error": str(e)}

    def _suggest_actions(self, user_message: str, data_preview: dict) -> list:
        """Suggest relevant Mito actions based on request and data.
        
        Args:
            user_message: User's message
            data_preview: Data preview from _load_and_preview_data
            
        Returns:
            List of suggested actions
        """
        if "error" in data_preview:
            return []

        suggestions = []
        columns = data_preview.get("columns", [])
        missing = data_preview.get("missing_values", {})

        # Suggest cleaning if there are missing values
        if any(count > 0 for count in missing.values()):
            suggestions.append({
                "action": "clean_missing_values",
                "description": f"Handle missing values in columns: {[col for col, count in missing.items() if count > 0]}",
                "priority": "high",
            })

        # Suggest specific operations based on request type
        request_type = self._classify_request(user_message)
        
        if request_type == "visualization":
            suggestions.append({
                "action": "create_chart",
                "description": "Create visualization using Mito's chart builder",
                "columns": columns,
            })
        elif request_type == "filtering":
            suggestions.append({
                "action": "filter_data",
                "description": "Apply filters to the dataset",
                "columns": columns,
            })
        elif request_type == "aggregation":
            suggestions.append({
                "action": "group_by",
                "description": "Group data and calculate aggregations",
                "columns": columns,
            })

        return suggestions

    async def generate_mito_code(self, operations: list) -> str:
        """Generate Python code for Mito operations.
        
        Args:
            operations: List of operations to perform
            
        Returns:
            Generated Python code
        """
        code_lines = [
            "import pandas as pd",
            "from mitosheet.public.v3 import *",
            "",
            "# Generated by AI Companion - Mito Integration",
            "",
        ]

        for op in operations:
            if op["type"] == "load":
                code_lines.append(f"df = pd.read_csv('{op['file_path']}')")
            elif op["type"] == "filter":
                code_lines.append(f"df = df[df['{op['column']}'] {op['operator']} {op['value']}]")
            elif op["type"] == "group_by":
                code_lines.append(
                    f"df_grouped = df.groupby('{op['group_column']}')['{op['agg_column']}'].{op['aggregation']}()"
                )

        return "\n".join(code_lines)

    async def save_analysis(self, df: pd.DataFrame, name: str, format: str = "csv") -> str:
        """Save analysis results to file.
        
        Args:
            df: DataFrame to save
            name: Name for the output file
            format: Output format ('csv', 'excel', 'json')
            
        Returns:
            Path to saved file
        """
        output_path = self.workspace_dir / f"{name}.{format}"
        
        if format == "csv":
            df.to_csv(output_path, index=False)
        elif format == "excel":
            df.to_excel(output_path, index=False)
        elif format == "json":
            df.to_json(output_path, orient='records', indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")

        logger.info(f"Analysis saved to: {output_path}")
        return str(output_path)

    def get_mito_notebook_link(self) -> str:
        """Generate link/instructions for opening Mito in Jupyter.
        
        Returns:
            Instructions for using Mito
        """
        return """
Para usar o Mito de forma interativa:

1. Abra o Jupyter Notebook ou JupyterLab
2. Execute em uma célula:
   ```python
   import mitosheet
   mitosheet.sheet()
   ```
3. Isso abrirá uma interface tipo Excel onde você pode:
   - Importar arquivos CSV/Excel
   - Fazer transformações visuais
   - Ver o código Python gerado automaticamente
   - Exportar os resultados

O Mito gera automaticamente o código pandas para todas as operações!
"""
