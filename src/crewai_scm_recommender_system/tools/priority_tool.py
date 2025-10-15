from crewai.tools import BaseTool
from typing import Dict, Any, Type
from pydantic import BaseModel, Field


class PriorityScoringInput(BaseModel):
    """Input schema for Priority Scoring Tool."""

    revenue_per_unit: int | float = Field(
        ...,
        description="Revenue generated per unit sold for the SKU",
    )
    turnover_ratio: int | float = Field(
        ...,
        description="Inventory turnover ratio (products sold / stock levels)",
    )
    stock_levels: int | float = Field(
        ...,
        description="Current inventory level for the SKU",
    )
    reorder_point: int | float = Field(
        ...,
        description="Reorder point threshold for the SKU",
    )
    lead_times: int | float = Field(
        ...,
        description="Number of days required to replenish the SKU",
    )


class PriorityScoringTool(BaseTool):
    name: str = "SKU Priority Scorer"
    description: str = (
        "Calculate priority scores for a SINGLE SKU based on multiple weighted factors including "
        "revenue per unit (30%), inventory turnover ratio (25%), stock health status (25%), "
        "and lead time risk (20%). Call this tool separately for each SKU you want to analyze. "
        "Returns a priority score (0-100) and priority level "
        "(CRITICAL/HIGH/MEDIUM) to help prioritize inventory management decisions."
    )
    args_schema: Type[BaseModel] = PriorityScoringInput

    def _run(
        self,
        revenue_per_unit: int | float,
        turnover_ratio: int | float,
        stock_levels: int | float,
        reorder_point: int | float,
        lead_times: int | float,
    ) -> Dict[str, Any]:
        # Normalize and weight factors
        revenue_score = min(revenue_per_unit / 1000, 1) * 30
        turnover_score = min(turnover_ratio / 10, 1) * 25
        
        # Stock status (critical if below reorder point)
        stock_health = stock_levels / reorder_point
        stock_score = (2 - min(stock_health, 2)) * 25
        
        # Lead time risk
        lead_risk_score = min(lead_times / 30, 1) * 20
        
        priority_score = revenue_score + turnover_score + stock_score + lead_risk_score
        
        return {
            'priority_score': round(priority_score, 2),
            'priority_level': 'CRITICAL' if priority_score > 70 else 'HIGH' if priority_score > 50 else 'MEDIUM'
        }
