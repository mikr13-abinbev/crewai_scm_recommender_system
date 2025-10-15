from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Dict, Any, Type

class MetricsInput(BaseModel):
    sku_data: Dict[str, Any] = Field(..., description="SKU data")

class InventoryMetricsTool(BaseTool):
    name: str = "Inventory Metrics Calculator"
    description: str = "Calculate key inventory metrics"
    args_schema: Type[BaseModel] = MetricsInput
    
    def _run(self, sku_data: Dict[str, Any]) -> Dict[str, float]:
        turnover = sku_data['Number_of_products_sold'] / sku_data['Stock_levels']
        daily_demand = sku_data['Number_of_products_sold'] / 30
        reorder_point = sku_data['Lead_times'] * daily_demand
        safety_stock = 1.65 * daily_demand * 0.3 * (sku_data['Lead_times'] ** 0.5)
        
        return {
            'turnover_ratio': round(turnover, 2),
            'reorder_point': round(reorder_point, 2),
            'safety_stock': round(safety_stock, 2),
            'revenue_per_unit': sku_data['Revenue_generated'] / sku_data['Number_of_products_sold']
        }
