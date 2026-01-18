"""Base analyzer interface."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pathlib import Path

class Analyzer(ABC):
    """Base class for all code analyzers."""
    
    @abstractmethod
    def run(self, repo: str) -> List[Dict[str, Any]]:
        """Run the analyzer on a repository.
        
        Args:
            repo: Path to the repository root
        
        Returns:
            List of finding dictionaries with keys:
            - id: Unique identifier
            - category: Category name (e.g., "Architecture", "Security")
            - severity: Severity level (CRITICAL, HIGH, MEDIUM, LOW, INFO)
            - pattern: Description of the pattern found
            - occurrences: Number of times pattern was found
            - evidence: List of file paths or code snippets
            - suggested_constraints: List of suggested Copilot constraints
        """
        pass
    
    def get_supported_languages(self) -> List[str]:
        """Get list of languages this analyzer supports.
        
        Returns:
            List of language identifiers (e.g., ["dotnet", "node"])
        """
        return []
    
    def _find_files(self, repo: Path, extensions: List[str]) -> List[Path]:
        """Find files with given extensions in repository.
        
        Args:
            repo: Repository root path
            extensions: List of file extensions (with or without dot)
        
        Returns:
            List of matching file paths
        """
        files = []
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
        
        try:
            for ext in extensions:
                files.extend(repo.rglob(f'*{ext}'))
        except Exception:
            pass  # Handle permission errors gracefully
        
        return files