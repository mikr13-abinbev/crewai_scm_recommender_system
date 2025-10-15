from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Dict, Any, Type


class InventoryMetricsInput(BaseModel):
    """Input schema for Inventory Metrics Calculator Tool."""

    number_of_products_sold: int | float = Field(
        ...,
        description="Total units sold for the SKU",
    )
    stock_levels: int | float = Field(
        ...,
        description="Current inventory level for the SKU",
    )
    lead_times: int | float = Field(
        ...,
        description="Number of days required to replenish the SKU",
    )
    revenue_generated: int | float = Field(
        ...,
        description="Total revenue generated from the SKU",
    )


class InventoryMetricsTool(BaseTool):
    name: str = "Inventory Metrics Calculator"
    description: str = (
        "Calculate key inventory management metrics for a SINGLE SKU. "
        "Call this tool separately for each SKU you want to analyze. "
        "Calculates: inventory turnover ratio (products sold / stock levels), "
        "reorder point (lead time × daily demand), "
        "safety stock (using 95% service level with 30% demand variability), "
        "and revenue per unit. These metrics are essential for inventory optimization "
        "and supply chain decision-making."
    )
    args_schema: Type[BaseModel] = InventoryMetricsInput

    def _run(
        self,
        number_of_products_sold: int | float,
        stock_levels: int | float,
        lead_times: int | float,
        revenue_generated: int | float,
    ) -> Dict[str, float]:
        turnover = number_of_products_sold / stock_levels
        daily_demand = number_of_products_sold / 30
        reorder_point = lead_times * daily_demand
        safety_stock = 1.65 * daily_demand * 0.3 * (lead_times**0.5)

        return {
            "turnover_ratio": round(turnover, 2),
            "reorder_point": round(reorder_point, 2),
            "safety_stock": round(safety_stock, 2),
            "revenue_per_unit": round(revenue_generated / number_of_products_sold, 2),
        }
