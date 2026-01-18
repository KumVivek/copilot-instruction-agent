"""Stack detection for repositories."""
import os
import logging
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def detect_stack(repo_path: str) -> Dict[str, Any]:
    """Detect the technology stack of a repository.
    
    Args:
        repo_path: Path to the repository root
    
    Returns:
        Dictionary with 'language' and 'confidence' keys
    
    Raises:
        ValueError: If repo_path doesn't exist
        RuntimeError: If stack cannot be detected
    """
    if not repo_path:
        raise ValueError("Repository path cannot be empty")
    
    repo = Path(repo_path)
    if not repo.exists():
        raise ValueError(f"Repository path does not exist: {repo_path}")
    
    if not repo.is_dir():
        raise ValueError(f"Repository path is not a directory: {repo_path}")
    
    logger.info(f"Detecting stack for repository: {repo_path}")
    
    # Collect all files and directories
    try:
        entries = list(repo.iterdir())
    except PermissionError as e:
        raise RuntimeError(f"Permission denied accessing repository: {e}") from e
    
    files = [e.name for e in entries if e.is_file()]
    dirs = [e.name for e in entries if e.is_dir()]
    
    # Detection patterns with confidence scores
    patterns: List[tuple] = [
        # .NET
        (lambda: any(f.endswith('.csproj') or f.endswith('.sln') for f in files),
         {"language": "dotnet", "confidence": 0.95, "frameworks": []}),
        
        # Node.js / JavaScript
        (lambda: "package.json" in files,
         {"language": "node", "confidence": 0.9, "frameworks": []}),
        
        # Python
        (lambda: any(f in files for f in ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile"]),
         {"language": "python", "confidence": 0.9, "frameworks": []}),
        
        # Java
        (lambda: any(f in files for f in ["pom.xml", "build.gradle", "build.gradle.kts"]),
         {"language": "java", "confidence": 0.9, "frameworks": []}),
        
        # Go
        (lambda: "go.mod" in files or "Gopkg.toml" in files,
         {"language": "go", "confidence": 0.9, "frameworks": []}),
        
        # Rust
        (lambda: "Cargo.toml" in files,
         {"language": "rust", "confidence": 0.95, "frameworks": []}),
    ]
    
    # Check patterns in order
    for check, result in patterns:
        try:
            if check():
                logger.info(f"Detected stack: {result['language']} (confidence: {result['confidence']})")
                return result
        except Exception as e:
            logger.warning(f"Error during stack detection check: {e}")
            continue
    
    # If no pattern matches, try to infer from file extensions
    extensions = {}
    for file in files:
        ext = Path(file).suffix
        if ext:
            extensions[ext] = extensions.get(ext, 0) + 1
    
    if extensions:
        # Common extension patterns
        if any(ext in extensions for ext in ['.cs', '.vb']):
            logger.warning("Found .NET files but no project file, using lower confidence")
            return {"language": "dotnet", "confidence": 0.6, "frameworks": []}
        if any(ext in extensions for ext in ['.js', '.ts', '.jsx', '.tsx']):
            logger.warning("Found JavaScript/TypeScript files but no package.json, using lower confidence")
            return {"language": "node", "confidence": 0.6, "frameworks": []}
        if any(ext in extensions for ext in ['.py']):
            logger.warning("Found Python files but no standard config, using lower confidence")
            return {"language": "python", "confidence": 0.6, "frameworks": []}
    
    raise RuntimeError(f"Unable to confidently detect stack for repository: {repo_path}")
