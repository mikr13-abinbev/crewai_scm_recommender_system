from crewai.tools import BaseTool
from typing import Dict, Any

class PriorityScoringTool(BaseTool):
    name: str = "SKU Priority Scorer"
    description: str = "Calculate priority scores for SKUs"
    
    def _run(self, sku_metrics: Dict) -> Dict[str, Any]:
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
