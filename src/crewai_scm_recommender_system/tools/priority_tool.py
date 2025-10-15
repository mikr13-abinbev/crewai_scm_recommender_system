from crewai.tools import BaseTool
from typing import Dict, Any, Type
from pydantic import BaseModel, Field


class PriorityScoringInput(BaseModel):
    """Input schema for Priority Scoring Tool."""

    sku_metrics: Dict[str, Any] = Field(
        ...,
        description="Dictionary containing SKU metrics including revenue_per_unit, turnover_ratio, Stock_levels, reorder_point, and Lead_times",
    )


class PriorityScoringTool(BaseTool):
    name: str = "SKU Priority Scorer"
    description: str = (
        "Calculate priority scores for SKUs based on multiple weighted factors including "
        "revenue per unit (30%), inventory turnover ratio (25%), stock health status (25%), "
        "and lead time risk (20%). Returns a priority score (0-100) and priority level "
        "(CRITICAL/HIGH/MEDIUM) to help prioritize inventory management decisions."
    )
    args_schema: Type[BaseModel] = PriorityScoringInput

    def _run(self, sku_metrics: Dict[str, Any]) -> Dict[str, Any]:
        # Normalize and weight factors
        revenue_score = min(sku_metrics['revenue_per_unit'] / 1000, 1) * 30
        turnover_score = min(sku_metrics['turnover_ratio'] / 10, 1) * 25
        
        # Stock status (critical if below reorder point)
        stock_health = sku_metrics['Stock_levels'] / sku_metrics['reorder_point']
        stock_score = (2 - min(stock_health, 2)) * 25
        
        # Lead time risk
        lead_risk_score = min(sku_metrics['Lead_times'] / 30, 1) * 20
        
        priority_score = revenue_score + turnover_score + stock_score + lead_risk_score
        
        return {
            'priority_score': round(priority_score, 2),
            'priority_level': 'CRITICAL' if priority_score > 70 else 'HIGH' if priority_score > 50 else 'MEDIUM'
        }
