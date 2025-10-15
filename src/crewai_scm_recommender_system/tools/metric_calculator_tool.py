from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Dict, Any, Type


class InventoryMetricsInput(BaseModel):
    """Input schema for Inventory Metrics Calculator Tool."""

    sku_data: Dict[str, Any] = Field(
        ...,
        description=(
            "Dictionary containing SKU data with required fields: "
            "Number_of_products_sold (total units sold), "
            "Stock_levels (current inventory level), "
            "Lead_times (days to replenish), "
            "Revenue_generated (total revenue from SKU). "
            "Used to calculate turnover ratio, reorder point, safety stock, and revenue per unit."
        ),
    )


class InventoryMetricsTool(BaseTool):
    name: str = "Inventory Metrics Calculator"
    description: str = (
        "Calculate key inventory management metrics for a given SKU including: "
        "inventory turnover ratio (products sold / stock levels), "
        "reorder point (lead time × daily demand), "
        "safety stock (using 95% service level with 30% demand variability), "
        "and revenue per unit. These metrics are essential for inventory optimization "
        "and supply chain decision-making."
    )
    args_schema: Type[BaseModel] = InventoryMetricsInput

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
