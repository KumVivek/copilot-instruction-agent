"""Risk scoring for findings."""
import logging
from typing import Dict, List, Any
from core.config import Config

logger = logging.getLogger(__name__)

def score(findings: List[Dict[str, Any]], config: Config) -> Dict[str, float]:
    """Calculate risk scores for findings by category.
    
    Args:
        findings: List of finding dictionaries with 'category' and 'severity' keys
        config: Configuration instance
    
    Returns:
        Dictionary mapping category names to risk scores (0-10, lower is riskier)
    """
    base_score = config.get("risk.base_score", 10)
    decrement = config.get("risk.decrement_per_finding", 1)
    
    risk: Dict[str, float] = {}
    
    # Severity multipliers
    severity_multipliers = {
        "CRITICAL": 3.0,
        "HIGH": 2.0,
        "MEDIUM": 1.5,
        "LOW": 1.0,
        "INFO": 0.5,
    }
    
    for finding in findings:
        category = finding.get("category", "Unknown")
        severity = finding.get("severity", "MEDIUM").upper()
        occurrences = finding.get("occurrences", 1)
        
        # Initialize category if not present
        if category not in risk:
            risk[category] = float(base_score)
        
        # Calculate penalty based on severity and occurrences
        multiplier = severity_multipliers.get(severity, 1.0)
        penalty = decrement * multiplier * occurrences
        
        risk[category] = max(0.0, risk[category] - penalty)
        
        logger.debug(
            f"Category '{category}': severity={severity}, occurrences={occurrences}, "
            f"penalty={penalty:.2f}, new_score={risk[category]:.2f}"
        )
    
    # Log final scores
    for category, score_value in risk.items():
        logger.info(f"Risk score for '{category}': {score_value:.2f}/10")
    
    return risk
