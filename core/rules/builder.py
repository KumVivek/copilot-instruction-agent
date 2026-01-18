"""Rules builder for generating constraints from findings."""
import logging
from typing import Dict, List, Any
from core.config import Config
from core.best_practices.loader import BestPracticesLoader

logger = logging.getLogger(__name__)

def build_rules(
    findings: List[Dict[str, Any]], 
    risk: Dict[str, float], 
    config: Config,
    language: str = ""
) -> List[str]:
    """Build rules from findings based on risk scores and best practices.
    
    Args:
        findings: List of finding dictionaries
        risk: Risk scores by category
        config: Configuration instance
        language: Language identifier for loading best practices
    
    Returns:
        Sorted list of unique rules/constraints
    """
    critical_threshold = config.get("risk.critical_threshold", 5)
    base_score = config.get("risk.base_score", 10)
    
    rules: List[str] = []
    
    # Add rules from findings
    for finding in findings:
        category = finding.get("category", "Unknown")
        category_risk = risk.get(category, base_score)
        
        # Include rules if category risk is below threshold
        if category_risk <= critical_threshold:
            suggested = finding.get("suggested_constraints", [])
            if suggested:
                rules.extend(suggested)
                logger.debug(
                    f"Including {len(suggested)} constraints from category '{category}' "
                    f"(risk: {category_risk:.2f})"
                )
    
    # Add best practices constraints
    if language:
        try:
            loader = BestPracticesLoader()
            practices = loader.load_practices(language)
            practices_constraints = practices.get("constraints", [])
            
            if practices_constraints:
                rules.extend(practices_constraints)
                logger.info(f"Added {len(practices_constraints)} constraints from best practices")
        except Exception as e:
            logger.warning(f"Failed to load best practices for {language}: {e}")
    
    # Remove duplicates and sort
    unique_rules = sorted(set(rules))
    logger.info(f"Generated {len(unique_rules)} unique rules (from findings + best practices)")
    
    return unique_rules
