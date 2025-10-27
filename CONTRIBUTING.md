# Contributing to PR-CYBR-P0D

Thank you for your interest in contributing to PR-CYBR-P0D! This document provides guidelines for contributing to the project.

> **Note**: If you want to create your own podcast automation pipeline using this code, see the [Forking This Repository](README.md#forking-this-repository) section in the README for customization guidance. This guide is for contributing improvements back to the PR-CYBR-P0D project itself.

## Development Workflow

This project follows the [Spec-Kit framework](https://github.com/PR-CYBR/spec-bootstrap) for specification-driven development.

### Branching Strategy

We use a comprehensive branching model with the following branches:

- `main` - Stable baseline (production-ready)
- `dev` - Active development integration
- `spec` - Specifications and requirements
- `plan` - Implementation planning
- `impl` - Implementation work
- `design` - Design artifacts
- `test` - Testing environment
- `stage` - Staging/pre-production
- `prod` - Production deployment
- `pages` - Documentation site
- `codex` - Knowledge base

See [BRANCHING.md](BRANCHING.md) for detailed information about each branch and the workflow.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/PR-CYBR/PR-CYBR-P0D/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details (OS, Python version, etc.)
   - Relevant logs or screenshots

### Suggesting Enhancements

1. Check existing issues for similar suggestions
2. Create a new issue with:
   - Clear description of the enhancement
   - Use cases and benefits
   - Possible implementation approach
   - Any relevant examples

### Contributing Code

#### 1. Start with Specifications

Before writing code, work in the `spec` branch to define what needs to be built:

```bash
git checkout spec
# Edit .specify/spec.md to add your feature specification
git add .specify/spec.md
git commit -m "spec: add specification for [feature]"
git push origin spec
```

#### 2. Create an Implementation Plan

Move to the `plan` branch to break down the specification:

```bash
git checkout plan
# Edit .specify/plan.md to add implementation tasks
git add .specify/plan.md
git commit -m "plan: add implementation plan for [feature]"
git push origin plan
```

#### 3. Implement the Feature

Work in the `impl` branch for coding:

```bash
git checkout impl
# Make your changes
git add .
git commit -m "feat: implement [feature]"
git push origin impl
```

#### 4. Create a Pull Request

1. Create a PR from `impl` → `dev`
2. Ensure all tests pass
3. Request review from maintainers
4. Address review feedback

### Code Style

#### Python Code

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Include docstrings for all functions and classes
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

Example:
```python
def download_episode(url: str, destination: Path) -> bool:
    """
    Download an episode from a URL to a destination file.
    
    Args:
        url: The URL of the MP3 file to download
        destination: Path where the file should be saved
    
    Returns:
        True if download was successful, False otherwise
    """
    # Implementation here
```

#### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add support for episode chapters
fix: handle network timeout errors gracefully
docs: update setup guide with troubleshooting
```

### Testing

Before submitting a PR:

1. Test your changes locally
2. Ensure the sync script runs without errors
3. Verify edge cases are handled
4. Check that error messages are clear and helpful

#### Local Testing

```bash
# Set up environment
export NOTION_TOKEN="your_token"
export NOTION_DATABASE_ID="your_database_id"

# Install dependencies
pip install -r scripts/requirements.txt

# Run the sync script
python scripts/sync_notion.py
```

### Documentation

- Update README.md if you add features
- Update SETUP.md if setup steps change
- Add docstrings to new functions
- Update .specify/ documents to reflect changes

## Project Structure

```
PR-CYBR-P0D/
├── .github/
│   └── workflows/          # GitHub Actions workflows
├── .specify/               # Spec-Kit specifications
│   ├── constitution.md     # Project rules
│   ├── spec.md            # Technical specification
│   ├── plan.md            # Implementation plan
│   └── tasks/             # Task breakdown
├── episodes/              # Podcast episode files
├── scripts/               # Automation scripts
│   ├── sync_notion.py    # Main sync script
│   └── requirements.txt  # Python dependencies
└── docs/                  # Additional documentation
```

## Questions?

If you have questions about contributing:

1. Check the [README.md](README.md)
2. Review [BRANCHING.md](BRANCHING.md)
3. Look through existing [Issues](https://github.com/PR-CYBR/PR-CYBR-P0D/issues)
4. Open a new issue with the `question` label

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers and help them learn
- Focus on what is best for the project
- Show empathy towards other contributors

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
