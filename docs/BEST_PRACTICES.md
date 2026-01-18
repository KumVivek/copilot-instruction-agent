# Best Practices System

RepoSentinel includes a comprehensive best practices system that evaluates your code against industry-standard practices for each programming language.

## Overview

The best practices system works in three stages:

1. **Loading**: Loads language-specific best practices from YAML files
2. **Checking**: Validates your codebase against these practices using pattern matching
3. **Integration**: Combines practice violations with code analysis findings to generate comprehensive guardrails

## How It Works

### 1. Practice Files

Best practices are stored in YAML files under `core/best_practices/practices/`:

- `dotnet.yaml` - .NET/C# best practices
- `node.yaml` - Node.js/JavaScript/TypeScript practices
- `python.yaml` - Python practices
- Additional languages can be added

### 2. Practice Structure

Each practice file contains:

```yaml
patterns:
  - id: "ARCH-001"
    name: "Controller accessing DbContext"
    type: "anti-pattern"
    severity: "HIGH"
    category: "Architecture"
    description: "Controllers should not directly access DbContext"
    regex: "(class\\s+\\w+Controller[^{]*\\{[^}]*DbContext)"
    constraint: "Controllers must not access DbContext directly"

rules:
  - "Follow SOLID principles"
  - "Use dependency injection"

constraints:
  - "Controllers must not contain business logic"
  - "Use async/await for I/O operations"

categories:
  architecture:
    description: "Architectural patterns"
    practices:
      - "Use layered architecture"
      - "Implement repository pattern"
```

### 3. Pattern Matching

The system uses regex patterns to identify violations:

- **Anti-patterns**: Code that should NOT be present (e.g., SQL injection vulnerabilities)
- **Required patterns**: Code that SHOULD be present (e.g., input validation)

### 4. Integration with Analysis

Best practices are integrated into the analysis flow:

1. **During Analysis**: Best practices checker runs alongside code analyzers
2. **In Rules Building**: Best practices constraints are added to findings
3. **In LLM Generation**: Best practices context is included in the prompt

## Adding Best Practices

### For a New Language

1. Create a new YAML file in `core/best_practices/practices/`:
   ```bash
   cp core/best_practices/practices/dotnet.yaml core/best_practices/practices/yourlang.yaml
   ```

2. Define patterns, rules, and constraints for your language

3. The system will automatically load it when that language is detected

### For Existing Languages

Edit the corresponding YAML file to add new patterns:

```yaml
patterns:
  - id: "NEW-001"
    name: "Your pattern name"
    type: "anti-pattern"
    severity: "HIGH"
    category: "Security"
    description: "Description of the issue"
    regex: "your-regex-pattern"
    constraint: "Suggested constraint for guardrails"
```

## Pattern Types

### Anti-patterns

Code that should be avoided:

```yaml
- id: "SEC-001"
  name: "SQL injection vulnerability"
  type: "anti-pattern"
  severity: "CRITICAL"
  regex: "(query|execute).*\\+.*['\"]"
```

### Required Patterns

Code that should be present (future enhancement):

```yaml
- id: "QUAL-001"
  name: "Input validation"
  type: "required-pattern"
  severity: "MEDIUM"
  regex: "ValidateInput|DataAnnotations"
```

## Severity Levels

- **CRITICAL**: Security vulnerabilities, data loss risks
- **HIGH**: Architectural violations, major design issues
- **MEDIUM**: Code quality issues, maintainability concerns
- **LOW**: Style issues, minor improvements
- **INFO**: Suggestions, recommendations

## Categories

Practices are organized by category:

- **Architecture**: Design patterns, structure
- **Security**: Vulnerabilities, secure coding
- **Performance**: Optimization, efficiency
- **Code Quality**: Maintainability, readability

## Example: .NET Best Practices

The .NET practices file includes:

- **10 patterns** covering architecture, security, and code quality
- **10 rules** for general .NET development
- **10 constraints** for Copilot guardrails
- **4 categories** with detailed practices

Key patterns include:
- Controller-DbContext violations
- Business logic in controllers
- Direct service instantiation
- SQL injection vulnerabilities
- Hardcoded secrets
- Missing input validation

## Usage in Guardrails

Best practices automatically influence guardrail generation:

1. **Pattern violations** become findings with suggested constraints
2. **Rules** are included in the LLM prompt context
3. **Constraints** are added to the rules list
4. **Categories** provide context for better guardrail generation

This ensures that guardrails are not just based on what's wrong in your code, but also on what industry best practices recommend.
