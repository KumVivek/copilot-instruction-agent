"""Best practices loader for different languages."""
import logging
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class BestPracticesLoader:
    """Loads and manages best practices for different programming languages."""
    
    def __init__(self, practices_dir: Optional[str] = None):
        """Initialize the best practices loader.
        
        Args:
            practices_dir: Optional directory containing practice files.
                          Defaults to practices/ directory relative to this file.
        """
        if practices_dir is None:
            # Default to practices/ directory in the same package
            self.practices_dir = Path(__file__).parent / "practices"
        else:
            self.practices_dir = Path(practices_dir)
        
        self._cache: Dict[str, Dict[str, Any]] = {}
        logger.debug(f"Best practices loader initialized with directory: {self.practices_dir}")
    
    def load_practices(self, language: str) -> Dict[str, Any]:
        """Load best practices for a specific language.
        
        Args:
            language: Language identifier (e.g., "dotnet", "node", "python")
        
        Returns:
            Dictionary containing best practices structure with:
            - patterns: List of patterns to check
            - rules: List of rules/guidelines
            - constraints: List of suggested constraints
            - categories: Practices organized by category
        """
        language = language.lower()
        
        # Check cache first
        if language in self._cache:
            return self._cache[language]
        
        # Try to load from file
        practice_file = self.practices_dir / f"{language}.yaml"
        
        if not practice_file.exists():
            logger.warning(f"No best practices file found for language: {language}")
            return self._get_default_practices()
        
        try:
            with open(practice_file, "r", encoding="utf-8") as f:
                practices = yaml.safe_load(f) or {}
            
            # Validate structure
            if not isinstance(practices, dict):
                logger.warning(f"Invalid practices file format for {language}")
                return self._get_default_practices()
            
            # Ensure required structure
            practices.setdefault("patterns", [])
            practices.setdefault("rules", [])
            practices.setdefault("constraints", [])
            practices.setdefault("categories", {})
            
            self._cache[language] = practices
            logger.info(f"Loaded {len(practices.get('patterns', []))} best practices for {language}")
            return practices
            
        except Exception as e:
            logger.error(f"Failed to load practices for {language}: {e}")
            return self._get_default_practices()
    
    def get_patterns(self, language: str) -> List[Dict[str, Any]]:
        """Get all patterns for a language.
        
        Args:
            language: Language identifier
        
        Returns:
            List of pattern dictionaries
        """
        practices = self.load_practices(language)
        return practices.get("patterns", [])
    
    def get_rules(self, language: str) -> List[str]:
        """Get all rules for a language.
        
        Args:
            language: Language identifier
        
        Returns:
            List of rule strings
        """
        practices = self.load_practices(language)
        return practices.get("rules", [])
    
    def get_constraints(self, language: str) -> List[str]:
        """Get all constraints for a language.
        
        Args:
            language: Language identifier
        
        Returns:
            List of constraint strings
        """
        practices = self.load_practices(language)
        return practices.get("constraints", [])
    
    def get_category_practices(self, language: str, category: str) -> Dict[str, Any]:
        """Get practices for a specific category.
        
        Args:
            language: Language identifier
            category: Category name (e.g., "architecture", "security")
        
        Returns:
            Dictionary of practices for the category
        """
        practices = self.load_practices(language)
        categories = practices.get("categories", {})
        return categories.get(category, {})
    
    @staticmethod
    def _get_default_practices() -> Dict[str, Any]:
        """Get default empty practices structure."""
        return {
            "patterns": [],
            "rules": [],
            "constraints": [],
            "categories": {},
        }
