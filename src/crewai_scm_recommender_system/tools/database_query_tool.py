from crewai.tools import BaseTool
import sqlite3
from typing import Type
from pydantic import BaseModel, Field

class DatabaseQueryInput(BaseModel):
    query: str = Field(..., description="SQL query to execute")

class DatabaseQueryTool(BaseTool):
    name: str = "Database Query Tool"
    description: str = "Query supply chain database for SKU data"
    args_schema: Type[BaseModel] = DatabaseQueryInput
    
    def _run(self, query: str) -> str:
        import json
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.abspath(os.path.join(base_dir, '../../../data/supply_chain_dataset.sqlite'))
        print(f"Database path: {db_path}")
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            return json.dumps(result)
        except Exception as e:
            return f"Database query failed: {str(e)}"
        finally:
            conn.close()
