"""Architecture analyzer for .NET codebases."""
import logging
import re
from pathlib import Path
from typing import List, Dict, Any

from core.analyzers.base import Analyzer

logger = logging.getLogger(__name__)

class DotnetArchitectureAnalyzer(Analyzer):
    """Analyzer for .NET architectural patterns and violations."""
    
    def get_supported_languages(self) -> List[str]:
        """Return supported languages."""
        return ["dotnet"]
    
    def run(self, repo: str) -> List[Dict[str, Any]]:
        """Analyze .NET repository for architectural issues.
        
        Args:
            repo: Path to repository root
        
        Returns:
            List of findings
        """
        repo_path = Path(repo)
        if not repo_path.exists():
            logger.error(f"Repository path does not exist: {repo}")
            return []
        
        findings = []
        
        # Find all C# files
        cs_files = self._find_files(repo_path, [".cs"])
        logger.info(f"Found {len(cs_files)} C# files to analyze")
        
        if not cs_files:
            logger.warning("No C# files found in repository")
            return []
        
        # Analyze for architectural patterns
        findings.extend(self._check_controller_dbcontext_access(cs_files))
        findings.extend(self._check_service_layer_usage(cs_files))
        findings.extend(self._check_dependency_injection(cs_files))
        findings.extend(self._check_static_dependencies(cs_files))
        
        return findings
    
    def _check_controller_dbcontext_access(self, files: List[Path]) -> List[Dict[str, Any]]:
        """Check if controllers directly access DbContext."""
        violations = []
        
        for file_path in files:
            if not self._is_controller_file(file_path):
                continue
            
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                
                # Check for DbContext usage in controller
                if self._is_controller_class(content):
                    # Look for DbContext field/property
                    dbcontext_pattern = r'\b(DbContext|ApplicationDbContext|.*DbContext)\s+\w+'
                    if re.search(dbcontext_pattern, content):
                        violations.append(str(file_path))
            except Exception as e:
                logger.debug(f"Error reading {file_path}: {e}")
                continue
        
        if violations:
            return [{
                "id": "ARCH-001",
                "category": "Architecture",
                "severity": "HIGH",
                "pattern": "Controller accessing DbContext directly",
                "occurrences": len(violations),
                "evidence": violations[:10],  # Limit evidence
                "suggested_constraints": [
                    "Controllers must not access DbContext directly",
                    "Use repository pattern or service layer for data access",
                    "Inject services through constructor, not DbContext"
                ]
            }]
        return []
    
    def _check_service_layer_usage(self, files: List[Path]) -> List[Dict[str, Any]]:
        """Check if business logic is in controllers instead of services."""
        controller_files = [f for f in files if self._is_controller_file(f)]
        
        if not controller_files:
            return []
        
        violations = []
        
        for file_path in controller_files:
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                
                if not self._is_controller_class(content):
                    continue
                
                # Check for business logic patterns in controllers
                # Look for complex conditionals, calculations, etc.
                business_logic_indicators = [
                    r'if\s*\([^)]{50,}\)',  # Complex conditionals
                    r'foreach\s*\([^)]+\)\s*\{[^}]{200,}\}',  # Complex loops
                    r'\.(Sum|Average|Count|Where|Select|GroupBy)\(',  # LINQ in controllers
                ]
                
                has_business_logic = any(re.search(pattern, content, re.DOTALL) 
                                       for pattern in business_logic_indicators)
                
                if has_business_logic:
                    violations.append(str(file_path))
            except Exception as e:
                logger.debug(f"Error analyzing {file_path}: {e}")
                continue
        
        if violations:
            return [{
                "id": "ARCH-002",
                "category": "Architecture",
                "severity": "MEDIUM",
                "pattern": "Business logic in controllers",
                "occurrences": len(violations),
                "evidence": violations[:10],
                "suggested_constraints": [
                    "Move business logic from controllers to service classes",
                    "Keep controllers thin - only handle HTTP concerns",
                    "Use service layer for data processing and business rules"
                ]
            }]
        return []
    
    def _check_dependency_injection(self, files: List[Path]) -> List[Dict[str, Any]]:
        """Check for proper dependency injection usage."""
        violations = []
        
        for file_path in files:
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                
                # Check for 'new' keyword creating dependencies (anti-pattern)
                # Look for: new ServiceClass(), new Repository(), etc.
                # But ignore: new List<>(), new Dictionary<>(), etc.
                new_pattern = r'new\s+([A-Z][a-zA-Z0-9]*)\s*\('
                matches = re.finditer(new_pattern, content)
                
                for match in matches:
                    class_name = match.group(1)
                    # Common exceptions (value types, collections)
                    if class_name in ['List', 'Dictionary', 'HashSet', 'Array', 'String', 
                                     'StringBuilder', 'DateTime', 'Guid', 'Exception']:
                        continue
                    
                    # Check if it's likely a service/repository
                    if any(keyword in class_name.lower() for keyword in 
                          ['service', 'repository', 'manager', 'handler', 'factory']):
                        violations.append(f"{file_path}:{self._get_line_number(content, match.start())}")
            except Exception as e:
                logger.debug(f"Error checking DI in {file_path}: {e}")
                continue
        
        if violations:
            return [{
                "id": "ARCH-003",
                "category": "Architecture",
                "severity": "MEDIUM",
                "pattern": "Direct instantiation instead of dependency injection",
                "occurrences": len(violations),
                "evidence": violations[:10],
                "suggested_constraints": [
                    "Use dependency injection instead of 'new' keyword for services",
                    "Register services in DI container and inject via constructor",
                    "Avoid creating service instances directly in classes"
                ]
            }]
        return []
    
    def _check_static_dependencies(self, files: List[Path]) -> List[Dict[str, Any]]:
        """Check for problematic static dependencies."""
        violations = []
        
        for file_path in files:
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                
                # Check for static service access (anti-pattern)
                static_patterns = [
                    r'ServiceLocator\.',
                    r'DependencyResolver\.',
                    r'HttpContext\.Current\.',
                ]
                
                for pattern in static_patterns:
                    if re.search(pattern, content):
                        violations.append(str(file_path))
                        break
            except Exception as e:
                logger.debug(f"Error checking static deps in {file_path}: {e}")
                continue
        
        if violations:
            return [{
                "id": "ARCH-004",
                "category": "Architecture",
                "severity": "HIGH",
                "pattern": "Static service location anti-pattern",
                "occurrences": len(violations),
                "evidence": violations[:10],
                "suggested_constraints": [
                    "Avoid ServiceLocator and static dependency resolution",
                    "Use constructor injection for all dependencies",
                    "Do not use HttpContext.Current or similar static accessors"
                ]
            }]
        return []
    
    def _is_controller_file(self, file_path: Path) -> bool:
        """Check if file is likely a controller."""
        return "Controller" in file_path.name or "controller" in str(file_path).lower()
    
    def _is_controller_class(self, content: str) -> bool:
        """Check if content contains a controller class."""
        return bool(re.search(r'class\s+\w+Controller\s*[:{]', content))
    
    def _get_line_number(self, content: str, position: int) -> int:
        """Get line number for a character position."""
        return content[:position].count('\n') + 1
