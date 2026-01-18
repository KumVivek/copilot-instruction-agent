# Changelog

## Version 1.0.0 - Major Improvements

### Critical Fixes

1. **Updated OpenAI API** - Migrated from deprecated `openai.ChatCompletion.create()` to modern `openai>=1.0.0` client API
2. **Error Handling** - Added comprehensive try/except blocks throughout the codebase
3. **File I/O** - Replaced unsafe `open().write()` with proper context managers
4. **Input Validation** - Added validation for repository paths and configuration

### Enhancements

1. **Logging System** - Implemented rich logging with configurable levels and formats
   - Uses `rich` library for beautiful terminal output
   - Supports DEBUG, INFO, WARNING, ERROR, CRITICAL levels
   - Configurable via YAML config

2. **Type Hints** - Added comprehensive type hints throughout the codebase
   - All functions now have proper type annotations
   - Improves IDE support and code clarity

3. **Configuration System** - Added YAML-based configuration
   - `reposentinel.yaml` for custom settings
   - Supports output paths, LLM settings, risk scoring parameters
   - Deep merging with sensible defaults

4. **Real Code Analysis** - Implemented actual code parsing for .NET
   - Replaced mock data with real pattern matching
   - Detects architectural violations:
     - Controllers accessing DbContext
     - Business logic in controllers
     - Direct instantiation anti-patterns
     - Static service location issues

5. **Improved Risk Scoring** - Enhanced algorithm with severity multipliers
   - Considers finding severity (CRITICAL, HIGH, MEDIUM, LOW, INFO)
   - Accounts for occurrence counts
   - Configurable via config file

6. **Rich CLI Output** - Beautiful terminal interface
   - Progress indicators for long-running operations
   - Color-coded status messages
   - Summary tables with key metrics
   - Professional banner and formatting

7. **Enhanced Stack Detection** - Improved technology detection
   - Supports .NET, Node.js, Python, Java, Go, Rust
   - Better confidence scoring
   - Fallback detection based on file extensions
   - Proper error handling for permission issues

8. **Better Report Generation** - Enhanced markdown reports
   - Organized by category
   - Risk score tables with visual indicators
   - Detailed findings with evidence
   - Recommendations section

### Architecture Improvements

1. **Package Structure** - Added proper `__init__.py` files
2. **Entry Point** - Added setuptools entry point (`reposentinel` command)
3. **Extensibility** - Analyzer registry system for easy plugin addition
4. **Modularity** - Clear separation of concerns across modules

### Documentation

1. **Comprehensive README** - Updated with:
   - Installation instructions
   - Usage examples
   - Configuration guide
   - Extension guide
   - Architecture overview

2. **Example Configuration** - Created `reposentinel.yaml.example`
3. **Type Annotations** - Self-documenting code with type hints

### Dependencies

- Updated `openai>=1.0.0` for modern API
- Added `tree-sitter-languages>=1.0.0` for future code parsing
- Added development dependencies (pytest, mypy, black, ruff)
