# Contributing to DeepLens

Thank you for your interest in contributing to DeepLens! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/DeepLens.git`
3. Create a virtual environment: `python -m venv venv && source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up your `.env` file with your OpenAI API key

## Development Workflow

1. Create a new branch for your feature: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Test your changes thoroughly
4. Commit with clear, descriptive messages
5. Push to your fork: `git push origin feature/your-feature-name`
6. Open a Pull Request

## Code Style

### Python Style Guide
- Follow PEP 8
- Use type hints where appropriate
- Write clear docstrings for all public methods
- Keep functions focused and single-purpose

### Docstring Format
```python
def method_name(param1: str, param2: int) -> Dict[str, Any]:
    """
    Brief description of what the method does
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
    """
```

### Agent System Prompts
When adding or modifying agent system prompts:
- Be specific about the agent's expertise
- Provide clear principles and guidelines
- Use examples when helpful
- Keep the tone consistent with the agent's purpose

## Testing

### Running Tests
```bash
# Validate structure
python validate.py

# Syntax check
python -m py_compile deeplens/**/*.py

# Run examples (requires API key)
python examples.py
```

### Writing Tests
- Test individual agent methods
- Test orchestrator coordination
- Include both success and error cases
- Use example data from `example_data/`

## Adding New Features

### New Agent
1. Create agent file in `deeplens/agents/`
2. Follow existing agent structure
3. Define clear system prompt
4. Implement analysis methods
5. Update orchestrator to include agent
6. Update documentation

### New Analysis Method
1. Add method to appropriate agent
2. Define prompt template
3. Return structured dictionary
4. Add example in `examples.py`
5. Document in README

### New Examples
1. Add example function in `examples.py`
2. Use example data from `example_data/`
3. Show clear input and output
4. Document in README

## Documentation

### What to Document
- New features and their usage
- API changes
- Configuration options
- Example use cases

### Where to Document
- `README.md` - User-facing documentation, quick start
- `ARCHITECTURE.md` - System design and technical details
- Code docstrings - Method/class level documentation
- `examples.py` - Usage examples

## Pull Request Guidelines

### PR Checklist
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive
- [ ] PR description explains the changes

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
Describe how you tested your changes

## Related Issues
Closes #issue_number
```

## Agent Design Principles

When designing or modifying agents, follow these principles:

1. **Specificity**: Agents should have clear, specific roles
2. **Expertise**: System prompts should establish strong domain expertise
3. **Skepticism**: Be critical and contrarian, especially in TrendAssessmentAgent
4. **Structure**: Return structured, parseable results
5. **Context**: Use system prompts to provide consistent context

## Example Contributions

### Good Contributions
- New agent for a specific analysis type
- Improved system prompts with better results
- Better error handling
- Performance improvements
- Clear documentation improvements

### Less Ideal Contributions
- Overly broad agents without clear focus
- Changes that break existing API
- Undocumented features
- Style-only changes without functional improvement

## Questions?

- Open an issue for questions
- Check existing issues and PRs
- Review `ARCHITECTURE.md` for technical details

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on the code, not the person
- Assume good intentions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
