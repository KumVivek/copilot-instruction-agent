"""Best practices checker that validates code against practices."""
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

from core.best_practices.loader import BestPracticesLoader

logger = logging.getLogger(__name__)

class BestPracticesChecker:
    """Checks code against best practices for a language."""
    
    def __init__(self, language: str, practices_loader: Optional[BestPracticesLoader] = None):
        """Initialize the checker.
        
        Args:
            language: Language identifier
            practices_loader: Optional loader instance. Creates new one if not provided.
        """
        self.language = language.lower()
        self.loader = practices_loader or BestPracticesLoader()
        self.practices = self.loader.load_practices(self.language)
        logger.debug(f"Initialized best practices checker for {self.language}")
    
    def check_codebase(self, repo_path: str) -> List[Dict[str, Any]]:
        """Check entire codebase against best practices.
        
        Args:
            repo_path: Path to repository root
        
        Returns:
            List of findings with violations of best practices
        """
        findings = []
        repo = Path(repo_path)
        
        if not repo.exists():
            logger.warning(f"Repository path does not exist: {repo_path}")
            return findings
        
        # Get patterns to check
        patterns = self.practices.get("patterns", [])
        
        if not patterns:
            logger.info(f"No patterns defined for {self.language}")
            return findings
        
        # Get file extensions for this language
        extensions = self._get_file_extensions()
        
        # Find all relevant files
        files = self._find_files(repo, extensions)
        logger.info(f"Checking {len(files)} files against {len(patterns)} best practice patterns")
        
        # Check each pattern
        for pattern_def in patterns:
            pattern_findings = self._check_pattern(pattern_def, files)
            findings.extend(pattern_findings)
        
        logger.info(f"Found {len(findings)} best practice violations")
        return findings
    
    def _check_pattern(self, pattern_def: Dict[str, Any], files: List[Path]) -> List[Dict[str, Any]]:
        """Check a specific pattern against files.
        
        Args:
            pattern_def: Pattern definition dictionary
            files: List of files to check
        
        Returns:
            List of findings for this pattern
        """
        pattern_id = pattern_def.get("id", "UNKNOWN")
        pattern_name = pattern_def.get("name", "Unknown Pattern")
        pattern_regex = pattern_def.get("regex")
        pattern_type = pattern_def.get("type", "anti-pattern")  # anti-pattern or required-pattern
        severity = pattern_def.get("severity", "MEDIUM")
        category = pattern_def.get("category", "Code Quality")
        description = pattern_def.get("description", "")
        constraint = pattern_def.get("constraint", "")
        
        if not pattern_regex:
            return []
        
        violations = []
        
        try:
            compiled_regex = re.compile(pattern_regex, re.MULTILINE | re.DOTALL)
        except re.error as e:
            logger.warning(f"Invalid regex pattern {pattern_id}: {e}")
            return []
        
        for file_path in files:
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                
                matches = compiled_regex.finditer(content)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    violation = {
                        "file": str(file_path),
                        "line": line_num,
                        "match": match.group(0)[:100],  # Limit match length
                    }
                    violations.append(violation)
                    
            except Exception as e:
                logger.debug(f"Error checking {file_path} for pattern {pattern_id}: {e}")
                continue
        
        if violations:
            return [{
                "id": f"BP-{pattern_id}",
                "category": category,
                "severity": severity,
                "pattern": pattern_name,
                "description": description,
                "occurrences": len(violations),
                "evidence": [f"{v['file']}:{v['line']}" for v in violations[:10]],
                "suggested_constraints": [constraint] if constraint else [],
                "source": "best_practices",
            }]
        
        return []
    
    def _get_file_extensions(self) -> List[str]:
        """Get file extensions for the current language.
        
        Returns:
            List of file extensions (with dots)
        """
        extension_map = {
            "dotnet": [".cs", ".vb", ".fs"],
            "node": [".js", ".ts", ".jsx", ".tsx"],
            "python": [".py"],
            "java": [".java"],
            "go": [".go"],
            "rust": [".rs"],
        }
        return extension_map.get(self.language, [])
    
    def _find_files(self, repo: Path, extensions: List[str]) -> List[Path]:
        """Find all files with given extensions in repository.
        
        Args:
            repo: Repository root path
            extensions: List of file extensions
        
        Returns:
            List of matching file paths
        """
        files = []
        
        # Common directories to exclude
        exclude_dirs = {".git", "__pycache__", "node_modules", "bin", "obj", ".venv", "venv"}
        
        try:
            for ext in extensions:
                for file_path in repo.rglob(f"*{ext}"):
                    # Skip excluded directories
                    if any(excluded in file_path.parts for excluded in exclude_dirs):
                        continue
                    files.append(file_path)
        except Exception as e:
            logger.debug(f"Error finding files: {e}")
        
        return files
    
    def get_practices_summary(self) -> Dict[str, Any]:
        """Get a summary of loaded best practices.
        
        Returns:
            Dictionary with practice counts and categories
        """
        return {
            "language": self.language,
            "patterns_count": len(self.practices.get("patterns", [])),
            "rules_count": len(self.practices.get("rules", [])),
            "constraints_count": len(self.practices.get("constraints", [])),
            "categories": list(self.practices.get("categories", {}).keys()),
        }
