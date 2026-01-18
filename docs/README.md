# RepoSentinel

Production-grade repo intelligence engine that generates enforceable GitHub Copilot guardrails.

## Overview

RepoSentinel analyzes your codebase to detect architectural patterns, security issues, and code quality problems. It then generates GitHub Copilot instruction files that enforce best practices and prevent common mistakes.

## Features

- **Multi-language Support**: Detects and analyzes .NET, Node.js, Python, Java, Go, and Rust projects
- **Best Practices Integration**: Language-specific best practices database that guides code evaluation
- **Intelligent Analysis**: Uses pattern matching and code analysis to find architectural violations
- **Best Practices Checking**: Validates code against industry best practices for each language
- **Risk Scoring**: Calculates risk scores by category to prioritize issues
- **LLM-Powered Instructions**: Generates comprehensive Copilot instruction files using OpenAI, informed by best practices
- **Rich CLI**: Beautiful terminal output with progress indicators and summaries
- **Configurable**: YAML-based configuration for customization
- **Extensible**: Plugin-based analyzer system for adding new checks and best practices

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd copilot-instruction-agent

# Install dependencies
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

## Configuration

1. Copy the example configuration:
   ```bash
   cp reposentinel.yaml.example reposentinel.yaml
   ```

2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. Customize `reposentinel.yaml` as needed (optional)

## Usage

### Basic Usage

```bash
# Analyze current directory
python -m cmd.reposentinel.main

# Analyze specific repository
python -m cmd.reposentinel.main /path/to/repo
```

### Output Files

RepoSentinel generates two files:

1. **`.github/copilot-instructions.md`** - GitHub Copilot instruction file with enforceable rules
2. **`analysis-report.md`** - Detailed analysis report with findings and risk scores

## Architecture

```
copilot-instruction-agent/
├── cmd/reposentinel/     # Main entry point
├── core/                 # Core functionality
│   ├── analyzers/       # Analyzer framework
│   ├── best_practices/  # Best practices system
│   │   ├── loader.py    # Loads practices for languages
│   │   ├── checker.py   # Validates code against practices
│   │   └── practices/   # Language-specific practice files
│   ├── config.py        # Configuration management
│   ├── logger.py        # Logging setup
│   ├── profiler/        # Stack detection
│   ├── report/          # Report generation
│   ├── risk/            # Risk scoring
│   └── rules/           # Rules builder
├── engines/             # Language-specific analyzers
│   └── dotnet/         # .NET analyzers
└── llm/                # LLM client
```

## How It Works

RepoSentinel uses a three-layer approach to generate guardrails:

1. **Code Analysis**: Analyzes your codebase for architectural patterns and violations
2. **Best Practices Evaluation**: Checks code against language-specific best practices
3. **Guardrail Generation**: Combines findings and best practices to create enforceable rules

### Best Practices System

RepoSentinel includes a comprehensive best practices database for each supported language:

- **Pattern-Based Detection**: Regex patterns to identify anti-patterns and violations
- **Rule Sets**: Industry-standard rules and guidelines
- **Category Organization**: Practices organized by category (Architecture, Security, Performance, Code Quality)
- **Constraint Generation**: Automatically generates constraints based on best practices

### Analyzers

#### .NET Architecture Analyzer

Detects common architectural violations in .NET projects:

- **ARCH-001**: Controllers accessing DbContext directly
- **ARCH-002**: Business logic in controllers
- **ARCH-003**: Direct instantiation instead of dependency injection
- **ARCH-004**: Static service location anti-patterns

#### Best Practices Checker

Automatically checks code against best practices for the detected language:

- **Security Patterns**: SQL injection, hardcoded secrets, input validation
- **Architecture Patterns**: Dependency injection, separation of concerns
- **Code Quality**: Type hints, async/await usage, code organization
- **Performance**: Optimization patterns and anti-patterns

## Configuration Options

See `reposentinel.yaml.example` for all available options:

- **Output paths**: Customize where files are written
- **LLM settings**: Model selection, temperature, token limits
- **Risk scoring**: Adjust scoring algorithm parameters
- **Logging**: Control log level and format

## Extending RepoSentinel

### Adding a New Analyzer

1. Create a new analyzer class inheriting from `Analyzer`:

```python
from core.analyzers.base import Analyzer
from typing import List, Dict, Any

class MyCustomAnalyzer(Analyzer):
    def run(self, repo: str) -> List[Dict[str, Any]]:
        # Your analysis logic
        return findings
```

2. Register it in `core/analyzers/runner.py`:

```python
from engines.mylang.analyzer import MyCustomAnalyzer

_ANALYZER_REGISTRY["mylang"] = [MyCustomAnalyzer]
```

## Requirements

- Python >= 3.11
- OpenAI API key
- Dependencies listed in `pyproject.toml`

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests (when implemented)
pytest

# Type checking
mypy .

# Format code
black .

# Lint code
ruff .
```

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
