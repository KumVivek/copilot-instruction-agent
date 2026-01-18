# Contributing to RepoSentinel

Thank you for your interest in contributing to RepoSentinel! This document provides guidelines and instructions for contributing.

## How to Contribute

We welcome contributions of all kinds:

- 🐛 **Bug reports**: Found a bug? Please open an issue!
- 💡 **Feature requests**: Have an idea? We'd love to hear it!
- 📝 **Documentation**: Help us improve our docs
- 🔧 **Code contributions**: Fix bugs, add features, improve code quality
- 🎨 **Best practices**: Add patterns for new languages or improve existing ones
- ⭐ **Star the repo**: Help others discover RepoSentinel!

## Getting Started

### Prerequisites

- Python >= 3.11
- Git
- Basic understanding of the project structure

### Development Setup

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/copilot-instruction-agent.git
   cd copilot-instruction-agent
   ```

3. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

5. **Set up pre-commit hooks** (optional but recommended):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Development Workflow

### 1. Create a Branch

Create a feature branch from `main`:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

- Write clean, readable code
- Follow existing code style
- Add type hints
- Write docstrings for functions/classes
- Add tests when possible

### 3. Test Your Changes

```bash
# Run tests
pytest

# Check code style
black .
ruff check .

# Type checking
mypy .
```

### 4. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: add support for Java best practices"
```

**Commit message format:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Reference any related issues
- Screenshots/examples if applicable

## Areas for Contribution

### 1. Adding Best Practices

Add patterns for new languages or improve existing ones:

**Location**: `core/best_practices/practices/[language].yaml`

**Example**:
```yaml
patterns:
  - id: "SEC-001"
    name: "SQL injection vulnerability"
    type: "anti-pattern"
    severity: "CRITICAL"
    category: "Security"
    description: "Description of the issue"
    regex: "your-regex-pattern"
    constraint: "Suggested constraint"
```

### 2. Adding Analyzers

Create new analyzers for specific languages:

**Location**: `engines/[language]/[analyzer].py`

**Example**:
```python
from core.analyzers.base import Analyzer

class MyLanguageAnalyzer(Analyzer):
    def run(self, repo: str) -> List[Dict[str, Any]]:
        # Your analysis logic
        return findings
```

Then register in `core/analyzers/runner.py`.

### 3. Improving Documentation

- Fix typos and improve clarity
- Add examples and use cases
- Create tutorials or guides
- Translate documentation

### 4. Bug Fixes

- Fix reported bugs
- Improve error handling
- Add edge case handling

### 5. Performance Improvements

- Optimize code analysis
- Improve caching
- Reduce memory usage

## Code Style Guidelines

### Python Style

- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Keep functions focused and small
- Use meaningful variable names

### Example:

```python
def analyze_code(repo_path: str, language: str) -> List[Dict[str, Any]]:
    """Analyze codebase for violations.
    
    Args:
        repo_path: Path to repository root
        language: Programming language identifier
    
    Returns:
        List of finding dictionaries
    """
    # Implementation
    pass
```

## Testing

- Write tests for new features
- Ensure existing tests pass
- Aim for good test coverage

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** with your changes
5. **Request review** from maintainers

## Code Review

All contributions go through code review. We aim to:
- Provide constructive feedback
- Review within 48 hours
- Help contributors improve their code

## Questions?

- Open an issue with the `question` label
- Check existing issues and discussions
- Reach out to maintainers

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Appreciated by the community! 🎉

Thank you for contributing to RepoSentinel!
