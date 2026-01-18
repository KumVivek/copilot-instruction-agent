# RepoSentinel 🛡️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Production-grade repo intelligence engine that generates enforceable GitHub Copilot guardrails.**

RepoSentinel analyzes your codebase to detect architectural patterns, security issues, and code quality problems. It then generates GitHub Copilot instruction files that enforce best practices and prevent common mistakes—all powered by industry-standard best practices and AI.

## ✨ Features

- **🔍 Multi-language Support**: Detects and analyzes .NET, Node.js, Python, Java, Go, and Rust projects
- **📚 Best Practices Integration**: Language-specific best practices database that guides code evaluation
- **🤖 Intelligent Analysis**: Uses pattern matching and code analysis to find architectural violations
- **✅ Best Practices Checking**: Validates code against industry best practices for each language
- **📊 Risk Scoring**: Calculates risk scores by category to prioritize issues
- **🤖 LLM-Powered Instructions**: Generates comprehensive Copilot instruction files using OpenAI, informed by best practices
- **🎨 Rich CLI**: Beautiful terminal output with progress indicators and summaries
- **⚙️ Configurable**: YAML-based configuration for customization
- **🔌 Extensible**: Plugin-based analyzer system for adding new checks and best practices

## 🚀 Quick Start

```bash
# Install RepoSentinel
pip install reposentinel

# Or from source
git clone https://github.com/yourusername/copilot-instruction-agent.git
cd copilot-instruction-agent
pip install -e .

# Set your OpenAI API key (optional, for guardrail generation)
export OPENAI_API_KEY="your-api-key-here"

# Analyze your repository (choose one method):
reposentinel /path/to/your/repo
# OR
python3 -m cmd.reposentinel.main /path/to/your/repo
# OR (if in project directory)
./reposentinel /path/to/your/repo
```

**That's it!** RepoSentinel will:
1. ✅ Detect your technology stack
2. 🔍 Analyze code for violations
3. 📚 Check against best practices
4. 📝 Generate guardrails and reports

## 📖 Documentation

- **[Full Documentation](docs/README.md)** - Complete guide with examples
- **[Best Practices Guide](docs/BEST_PRACTICES.md)** - Understanding the best practices system
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- **[Changelog](CHANGELOG.md)** - Version history

## 🎯 Use Cases

- **Code Quality**: Ensure your team follows best practices
- **Security**: Detect common security vulnerabilities
- **Architecture**: Enforce architectural patterns
- **Onboarding**: Help new developers understand code standards
- **CI/CD**: Integrate into your pipeline for automated checks

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Star Us!

If you find RepoSentinel useful, please consider giving it a star! ⭐

---

**Made with ❤️ by the RepoSentinel team**
