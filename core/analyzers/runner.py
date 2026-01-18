"""Analyzer runner that executes all applicable analyzers."""
import logging
from typing import Dict, List, Any, Type
from pathlib import Path

# Import analyzers
from engines.dotnet.architecture import DotnetArchitectureAnalyzer
from core.analyzers.base import Analyzer
from core.best_practices.checker import BestPracticesChecker

logger = logging.getLogger(__name__)

# Registry of analyzers by language
_ANALYZER_REGISTRY: Dict[str, List[Type[Analyzer]]] = {
    "dotnet": [DotnetArchitectureAnalyzer],
    "node": [],  # Add Node.js analyzers here
    "python": [],  # Add Python analyzers here
    "java": [],  # Add Java analyzers here
    "go": [],  # Add Go analyzers here
    "rust": [],  # Add Rust analyzers here
}

def register_analyzer(language: str, analyzer_class: Type[Analyzer]) -> None:
    """Register an analyzer for a specific language.
    
    Args:
        language: Language identifier
        analyzer_class: Analyzer class to register
    """
    if language not in _ANALYZER_REGISTRY:
        _ANALYZER_REGISTRY[language] = []
    _ANALYZER_REGISTRY[language].append(analyzer_class)
    logger.debug(f"Registered analyzer {analyzer_class.__name__} for {language}")

def run_analyzers(repo: str, stack: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Run all applicable analyzers for the detected stack.
    
    Args:
        repo: Path to repository root
        stack: Detected stack information
    
    Returns:
        Combined list of findings from all analyzers
    """
    language = stack.get("language", "").lower()
    
    if not language:
        logger.warning("No language detected, skipping analyzers")
        return []
    
    if language not in _ANALYZER_REGISTRY:
        logger.warning(f"No analyzers registered for language: {language}")
        return []
    
    analyzers = _ANALYZER_REGISTRY[language]
    if not analyzers:
        logger.info(f"No analyzers available for language: {language}")
        return []
    
    logger.info(f"Running {len(analyzers)} analyzer(s) for {language}")
    
    all_findings = []
    
    # Run language-specific analyzers
    for analyzer_class in analyzers:
        try:
            analyzer = analyzer_class()
            logger.debug(f"Running analyzer: {analyzer_class.__name__}")
            findings = analyzer.run(repo)
            all_findings.extend(findings)
            logger.info(f"{analyzer_class.__name__} found {len(findings)} issue(s)")
        except Exception as e:
            logger.error(f"Analyzer {analyzer_class.__name__} failed: {e}", exc_info=True)
            continue
    
    # Run best practices checker
    try:
        logger.info("Checking code against best practices...")
        practices_checker = BestPracticesChecker(language)
        practices_findings = practices_checker.check_codebase(repo)
        all_findings.extend(practices_findings)
        
        summary = practices_checker.get_practices_summary()
        logger.info(
            f"Best practices check: {len(practices_findings)} violations found "
            f"({summary['patterns_count']} patterns checked)"
        )
    except Exception as e:
        logger.warning(f"Best practices check failed: {e}", exc_info=True)
        # Don't fail the entire analysis if best practices check fails
    
    logger.info(f"Total findings across all analyzers: {len(all_findings)}")
    return all_findings
