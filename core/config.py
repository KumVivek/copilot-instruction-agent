"""Configuration management for RepoSentinel."""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Configuration manager for RepoSentinel."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_path: Optional path to config file. If not provided, looks for
                        reposentinel.yaml in current directory or repo root.
        """
        self.config_path = config_path or self._find_config()
        self._config: Dict[str, Any] = self._load_config()
    
    def _find_config(self) -> Optional[str]:
        """Find configuration file in common locations."""
        current_dir = Path.cwd()
        possible_paths = [
            current_dir / "reposentinel.yaml",
            current_dir / "reposentinel.yml",
            current_dir / ".reposentinel.yaml",
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        return None
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        default_config = {
            "output": {
                "copilot_instructions_path": ".github/copilot-instructions.md",
                "report_path": "analysis-report.md",
            },
            "llm": {
                "model": "gpt-4o-mini",
                "temperature": 0.3,
                "max_tokens": 2000,
            },
            "risk": {
                "base_score": 10,
                "decrement_per_finding": 1,
                "critical_threshold": 5,
            },
            "analyzers": {
                "enabled": ["architecture", "security", "performance"],
            },
            "logging": {
                "level": os.getenv("LOG_LEVEL", "INFO"),
                "format": "rich",
            },
        }
        
        if self.config_path and Path(self.config_path).exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    file_config = yaml.safe_load(f) or {}
                    # Deep merge with defaults
                    return self._deep_merge(default_config, file_config)
            except Exception as e:
                # If config file exists but can't be loaded, use defaults
                # Log warning but don't fail - defaults are acceptable
                # Use basic print to avoid dependency on logging setup
                import warnings
                warnings.warn(f"Failed to load config file {self.config_path}: {e}. Using defaults.", UserWarning)
                return default_config
        
        return default_config
    
    @staticmethod
    def _deep_merge(base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = Config._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation."""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value
    
    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access."""
        return self.get(key)
