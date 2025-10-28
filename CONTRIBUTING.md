# Contributing to n8n Workflow Intelligence Agent

Thank you for your interest in contributing to the n8n Workflow Intelligence Agent! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs
- Use the GitHub Issues page to report bugs
- Describe the bug in detail
- Include steps to reproduce
- Include your environment details (OS, Python version, n8n version)

### Suggesting Features
- Open a GitHub Issue with the "enhancement" label
- Describe the feature and its use case
- Explain why it would be valuable

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Fork and clone
git clone https://github.com/yourusername/n8n-workflow-agent.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Include type hints where appropriate

### Testing
- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to maintain a welcoming and inclusive community.

## Questions?

Feel free to open an issue or contact the maintainers if you have any questions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.