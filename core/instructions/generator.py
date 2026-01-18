"""Generator for categorized Copilot instruction files."""
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

from core.best_practices.loader import BestPracticesLoader

logger = logging.getLogger(__name__)

class InstructionGenerator:
    """Generates categorized Copilot instruction files."""
    
    # Category mapping - maps our categories to best practices categories
    CATEGORY_MAPPING = {
        "design": ["architecture", "code_quality"],
        "api": ["architecture"],
        "security": ["security"],
        "data-access": ["architecture", "security"],
        "caching": ["performance"],
        "testing": ["code_quality"],
        "logging": ["code_quality"],
    }
    
    def __init__(self, language: str, practices_loader: Optional[BestPracticesLoader] = None):
        """Initialize instruction generator.
        
        Args:
            language: Programming language identifier
            practices_loader: Optional best practices loader
        """
        self.language = language.lower()
        self.loader = practices_loader or BestPracticesLoader()
        self.practices = self.loader.load_practices(self.language)
        logger.debug(f"Initialized instruction generator for {self.language}")
    
    def generate_all_instructions(
        self, 
        stack: Dict[str, Any], 
        findings: List[Dict[str, Any]], 
        rules: List[str]
    ) -> Dict[str, str]:
        """Generate all categorized instruction files.
        
        Args:
            stack: Detected stack information
            findings: List of findings from analysis
            rules: List of rules/constraints
        
        Returns:
            Dictionary mapping category names to instruction content
        """
        instructions = {}
        
        # Check if caching is present in the codebase
        has_caching = self._detect_caching(findings, rules, stack)
        
        # Generate instructions for each category
        categories = ["design", "api", "security", "data-access", "testing", "logging"]
        
        # Only add caching if detected
        if has_caching:
            categories.append("caching")
        
        for category in categories:
            try:
                content = self._generate_category_instructions(category, stack, findings, rules)
                if content:
                    instructions[category] = content
                    logger.debug(f"Generated {category} instructions")
            except Exception as e:
                logger.warning(f"Failed to generate {category} instructions: {e}")
                continue
        
        return instructions
    
    def _detect_caching(self, findings: List[Dict[str, Any]], rules: List[str], stack: Dict[str, Any]) -> bool:
        """Detect if caching is used in the codebase."""
        # Check findings for caching-related patterns
        caching_keywords = ["cache", "redis", "memorycache", "distributedcache", "caching"]
        for finding in findings:
            pattern = finding.get("pattern", "").lower()
            if any(keyword in pattern for keyword in caching_keywords):
                return True
        
        # Check rules for caching mentions
        for rule in rules:
            if any(keyword in rule.lower() for keyword in caching_keywords):
                return True
        
        # Check stack for caching frameworks
        frameworks = stack.get("frameworks", [])
        caching_frameworks = ["redis", "memorycache", "distributedcache"]
        if any(fw.lower() in [f.lower() for f in frameworks] for fw in caching_frameworks):
            return True
        
        return False
    
    def _generate_category_instructions(
        self,
        category: str,
        stack: Dict[str, Any],
        findings: List[Dict[str, Any]],
        rules: List[str]
    ) -> str:
        """Generate instructions for a specific category.
        
        Args:
            category: Category name (design, api, security, etc.)
            stack: Stack information
            findings: Analysis findings
            rules: General rules
        
        Returns:
            Markdown content for the category
        """
        # Get relevant findings for this category
        category_findings = self._filter_findings_by_category(findings, category)
        
        # Get relevant best practices
        category_practices = self._get_category_practices(category)
        
        # Get relevant rules
        category_rules = self._filter_rules_by_category(rules, category)
        
        # Build the instruction content
        content = self._build_category_content(
            category, stack, category_findings, category_practices, category_rules
        )
        
        return content
    
    def _filter_findings_by_category(self, findings: List[Dict[str, Any]], category: str) -> List[Dict[str, Any]]:
        """Filter findings relevant to a category."""
        category_map = {
            "design": ["Architecture", "Code Quality"],
            "api": ["Architecture", "Security"],
            "security": ["Security"],
            "data-access": ["Architecture", "Security"],
            "caching": ["Performance"],
            "testing": ["Code Quality"],
            "logging": ["Code Quality"],
        }
        
        relevant_categories = category_map.get(category, [])
        return [
            f for f in findings 
            if f.get("category") in relevant_categories
        ]
    
    def _get_category_practices(self, category: str) -> Dict[str, Any]:
        """Get best practices for a category."""
        practices_categories = self.CATEGORY_MAPPING.get(category, [])
        result = {
            "patterns": [],
            "rules": [],
            "constraints": [],
            "practices": [],
        }
        
        # Get patterns from best practices
        all_patterns = self.practices.get("patterns", [])
        for pattern in all_patterns:
            pattern_category = pattern.get("category", "").lower()
            if any(cat in pattern_category for cat in practices_categories):
                result["patterns"].append(pattern)
        
        # Get category-specific practices
        categories = self.practices.get("categories", {})
        for cat_name in practices_categories:
            if cat_name in categories:
                cat_info = categories[cat_name]
                result["practices"].extend(cat_info.get("practices", []))
                result["rules"].append(cat_info.get("description", ""))
        
        # Get general rules relevant to category
        all_rules = self.practices.get("rules", [])
        category_keywords = {
            "design": ["architecture", "design", "pattern", "structure"],
            "api": ["api", "endpoint", "controller", "route"],
            "security": ["security", "secure", "vulnerability", "injection", "authentication"],
            "data-access": ["database", "data", "repository", "query", "entity"],
            "caching": ["cache", "performance", "optimize"],
            "testing": ["test", "unit", "integration", "mock"],
            "logging": ["log", "logger", "trace", "debug"],
        }
        
        keywords = category_keywords.get(category, [])
        for rule in all_rules:
            if any(keyword in rule.lower() for keyword in keywords):
                result["rules"].append(rule)
        
        # Get constraints
        all_constraints = self.practices.get("constraints", [])
        for constraint in all_constraints:
            if any(keyword in constraint.lower() for keyword in keywords):
                result["constraints"].append(constraint)
        
        return result
    
    def _filter_rules_by_category(self, rules: List[str], category: str) -> List[str]:
        """Filter rules relevant to a category."""
        category_keywords = {
            "design": ["architecture", "design", "pattern", "controller", "service", "layer"],
            "api": ["api", "endpoint", "controller", "route", "http", "request", "response"],
            "security": ["security", "secure", "vulnerability", "injection", "authentication", "authorization", "input", "validate"],
            "data-access": ["database", "data", "repository", "query", "entity", "dbcontext", "async"],
            "caching": ["cache", "performance", "optimize"],
            "testing": ["test", "unit", "integration", "mock"],
            "logging": ["log", "logger", "trace", "debug", "error"],
        }
        
        keywords = category_keywords.get(category, [])
        return [
            rule for rule in rules
            if any(keyword in rule.lower() for keyword in keywords)
        ]
    
    def _build_category_content(
        self,
        category: str,
        stack: Dict[str, Any],
        findings: List[Dict[str, Any]],
        practices: Dict[str, Any],
        rules: List[str]
    ) -> str:
        """Build markdown content for a category."""
        language = stack.get("language", "Unknown")
        
        # Category titles
        category_titles = {
            "design": "Design & Architecture",
            "api": "API Development",
            "security": "Security",
            "data-access": "Data Access",
            "caching": "Caching",
            "testing": "Testing",
            "logging": "Logging",
        }
        
        title = category_titles.get(category, category.title())
        
        content = f"# {title} Guidelines\n\n"
        content += f"*Generated by RepoSentinel for {language} projects*\n\n"
        
        # Add findings if any
        if findings:
            content += "## Issues Found\n\n"
            content += f"**{len(findings)} issue(s) detected in this codebase:**\n\n"
            for finding in findings[:10]:  # Limit to 10
                pattern = finding.get("pattern", "Unknown")
                severity = finding.get("severity", "UNKNOWN")
                content += f"- **{pattern}** ({severity})\n"
            content += "\n"
        
        # Add best practices
        if practices.get("practices"):
            content += "## Best Practices\n\n"
            for practice in practices["practices"]:
                content += f"- {practice}\n"
            content += "\n"
        
        # Add patterns and constraints
        if practices.get("patterns") or practices.get("constraints"):
            content += "## Rules & Constraints\n\n"
            
            # Add constraints from practices
            for constraint in practices.get("constraints", []):
                content += f"- {constraint}\n"
            
            # Add constraints from findings
            for rule in rules:
                content += f"- {rule}\n"
            
            content += "\n"
        
        # Add specific patterns
        if practices.get("patterns"):
            content += "## Anti-Patterns to Avoid\n\n"
            for pattern in practices["patterns"][:5]:  # Limit to 5
                name = pattern.get("name", "Unknown")
                description = pattern.get("description", "")
                constraint = pattern.get("constraint", "")
                
                content += f"### {name}\n\n"
                if description:
                    content += f"{description}\n\n"
                if constraint:
                    content += f"**Constraint:** {constraint}\n\n"
        
        # Add category-specific guidance
        content += self._get_category_specific_guidance(category, language)
        
        content += "\n---\n"
        content += f"*This file is automatically generated. Update as needed for your project.*\n"
        
        return content
    
    def _get_category_specific_guidance(self, category: str, language: str) -> str:
        """Get category-specific guidance based on language."""
        guidance = {
            "design": {
                "dotnet": """
## Architecture Patterns

- **Layered Architecture**: Use Controllers -> Services -> Repositories pattern
- **Dependency Injection**: Register all services in DI container
- **Separation of Concerns**: Keep controllers thin, move business logic to services
- **SOLID Principles**: Follow Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
""",
                "node": """
## Architecture Patterns

- **MVC/MVP Pattern**: Separate concerns between models, views, and controllers
- **Middleware Pattern**: Use middleware for cross-cutting concerns
- **Dependency Injection**: Use DI containers or manual injection
""",
                "python": """
## Architecture Patterns

- **Layered Architecture**: Separate presentation, business, and data layers
- **Dependency Injection**: Use dependency injection for better testability
- **SOLID Principles**: Follow design principles for maintainable code
""",
            },
            "api": {
                "dotnet": """
## API Best Practices

- **RESTful Design**: Follow REST conventions for endpoints
- **Input Validation**: Use data annotations or FluentValidation
- **Error Handling**: Return appropriate HTTP status codes
- **Async Operations**: Use async/await for all I/O operations
- **Versioning**: Implement API versioning strategy
""",
                "node": """
## API Best Practices

- **RESTful Design**: Follow REST conventions
- **Input Validation**: Validate all request parameters
- **Error Handling**: Use proper HTTP status codes
- **Middleware**: Use middleware for authentication, logging, error handling
""",
            },
            "security": {
                "dotnet": """
## Security Best Practices

- **Input Validation**: Always validate and sanitize user input
- **SQL Injection Prevention**: Use parameterized queries or Entity Framework
- **Authentication**: Implement proper authentication (JWT, OAuth, etc.)
- **Authorization**: Use role-based or policy-based authorization
- **Secrets Management**: Store secrets in configuration, never in code
- **HTTPS**: Always use HTTPS in production
""",
            },
            "data-access": {
                "dotnet": """
## Data Access Best Practices

- **Repository Pattern**: Use repository pattern to abstract data access
- **Async Operations**: Always use async/await for database operations
- **Connection Management**: Let Entity Framework manage connections
- **Query Optimization**: Use LINQ efficiently, avoid N+1 queries
- **Transactions**: Use transactions for multi-step operations
""",
            },
            "caching": {
                "dotnet": """
## Caching Best Practices

- **Cache Strategy**: Use appropriate caching strategy (memory, distributed)
- **Cache Invalidation**: Implement proper cache invalidation
- **Cache Keys**: Use consistent, unique cache keys
- **Cache Duration**: Set appropriate expiration times
""",
            },
            "testing": {
                "dotnet": """
## Testing Best Practices

- **Unit Tests**: Write unit tests for business logic
- **Integration Tests**: Test database and external service interactions
- **Test Coverage**: Aim for high code coverage
- **Test Naming**: Use descriptive test names (Given_When_Then)
- **Mocking**: Use mocks for external dependencies
""",
            },
            "logging": {
                "dotnet": """
## Logging Best Practices

- **Structured Logging**: Use structured logging (Serilog, NLog)
- **Log Levels**: Use appropriate log levels (Debug, Info, Warning, Error)
- **Sensitive Data**: Never log passwords, tokens, or sensitive information
- **Performance**: Use async logging for better performance
- **Context**: Include relevant context in log messages
""",
            },
        }
        
        category_guidance = guidance.get(category, {})
        return category_guidance.get(language, category_guidance.get("dotnet", ""))
