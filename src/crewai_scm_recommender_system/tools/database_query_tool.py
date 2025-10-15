from crewai.tools import BaseTool
import sqlite3
from typing import Type
from pydantic import BaseModel, Field


class DatabaseQueryInput(BaseModel):
    """Input schema for Database Query Tool."""

    query: str = Field(
        ...,
        description=(
            "SQL query to execute against the supply chain database. "
            "The database contains SKU data with columns: SKU, Product_type, Price, "
            "Availability, Number_of_products_sold, Revenue_generated, Customer_demographics, "
            "Stock_levels, Lead_times, Order_quantities, Shipping_times, Shipping_carriers, "
            "Shipping_costs, Supplier_name, Location, Lead_time, Production_volumes, "
            "Manufacturing_lead_time, Manufacturing_costs, Inspection_results, Defect_rates, "
            "Transportation_modes, Routes, Costs"
        ),
    )


class DatabaseQueryTool(BaseTool):
    name: str = "Database Query Tool"
    description: str = (
        "Query the supply chain SQLite database for SKU and product data. "
        "Use this tool to retrieve product information, inventory levels, sales data, "
        "supplier information, shipping details, and manufacturing metrics. "
        "Returns results as JSON-formatted string with column names and row data."
    )
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
