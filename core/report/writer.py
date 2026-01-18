"""Report writing functionality."""
import logging
from pathlib import Path
from typing import Dict, List, Any
from core.config import Config

logger = logging.getLogger(__name__)

def write_report(
    stack: Dict[str, Any],
    findings: List[Dict[str, Any]],
    risk: Dict[str, float],
    config: Config,
    repo_path: str = "."
) -> None:
    """Write analysis report to markdown file.
    
    Args:
        stack: Detected stack information
        findings: List of findings
        risk: Risk scores by category
        config: Configuration instance
        repo_path: Path to the repository being analyzed (default: current directory)
    
    Raises:
        IOError: If report file cannot be written
    """
    report_path = config.get("output.report_path", "analysis-report.md")
    # Resolve path relative to the repository being analyzed
    repo = Path(repo_path).resolve()
    report_file = repo / report_path
    
    try:
        logger.info(f"Writing analysis report to {report_file}")
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("# RepoSentinel Analysis Report\n\n")
            
            # Stack information
            f.write("## Detected Stack\n\n")
            f.write(f"- **Language**: {stack.get('language', 'Unknown')}\n")
            f.write(f"- **Confidence**: {stack.get('confidence', 0):.2%}\n")
            if stack.get('frameworks'):
                f.write(f"- **Frameworks**: {', '.join(stack['frameworks'])}\n")
            f.write("\n")
            
            # Risk scores
            f.write("## Risk Scores\n\n")
            if risk:
                f.write("| Category | Risk Score |\n")
                f.write("|----------|------------|\n")
                for category, score_value in sorted(risk.items()):
                    # Color coding in markdown
                    status = "🔴 Critical" if score_value <= 3 else "🟡 Warning" if score_value <= 5 else "🟢 Good"
                    f.write(f"| {category} | {score_value:.2f}/10 {status} |\n")
            else:
                f.write("No risk scores calculated.\n")
            f.write("\n")
            
            # Findings summary
            f.write("## Findings Summary\n\n")
            f.write(f"Total findings: {len(findings)}\n\n")
            
            # Group findings by category
            by_category: Dict[str, List[Dict[str, Any]]] = {}
            for finding in findings:
                category = finding.get("category", "Unknown")
                if category not in by_category:
                    by_category[category] = []
                by_category[category].append(finding)
            
            # Write findings by category
            for category, category_findings in sorted(by_category.items()):
                f.write(f"### {category}\n\n")
                for finding in category_findings:
                    pattern = finding.get("pattern", "Unknown pattern")
                    severity = finding.get("severity", "UNKNOWN")
                    occurrences = finding.get("occurrences", 1)
                    
                    f.write(f"- **{pattern}** ({severity})\n")
                    f.write(f"  - Occurrences: {occurrences}\n")
                    
                    if finding.get("evidence"):
                        f.write(f"  - Evidence: {', '.join(str(e) for e in finding['evidence'][:3])}\n")
                    if finding.get("suggested_constraints"):
                        f.write(f"  - Suggested constraints: {len(finding['suggested_constraints'])}\n")
                    f.write("\n")
            
            # Recommendations
            f.write("## Recommendations\n\n")
            critical_categories = [cat for cat, score in risk.items() if score <= 5]
            if critical_categories:
                f.write("The following categories require immediate attention:\n\n")
                for cat in critical_categories:
                    f.write(f"- {cat} (risk score: {risk[cat]:.2f}/10)\n")
            else:
                f.write("No critical issues detected. Continue monitoring code quality.\n")
        
        logger.info(f"Report written successfully to {report_file}")
        
    except IOError as e:
        logger.error(f"Failed to write report: {e}")
        raise
