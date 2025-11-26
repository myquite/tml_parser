# Contributing to TML Parser

Thank you for your interest in contributing to TML Parser! This document provides guidelines and instructions for contributing.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/tml_parser_demo.git
   cd tml_parser_demo
   ```

3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

The project uses Python 3.8+ with no required external dependencies (uses only the standard library).

For optional XSD validation support:
```bash
pip install -r requirements.txt
```

## Making Changes

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

### Testing

Before submitting changes:

1. **Test with example files**:
   ```bash
   python3 tml_to_site.py examples/sample_course.tml test_output/
   ```

2. **Validate against XSD** (if lxml is installed):
   ```bash
   python3 tml_to_site.py examples/example_course.tml test_output/
   ```

3. **Check for errors**:
   - Ensure generated HTML is valid
   - Test in multiple browsers
   - Verify all features work as expected

### Documentation

- Update relevant documentation when adding features
- Add examples to `examples/` directory if applicable
- Update `CHANGELOG.md` with your changes

## Submitting Changes

1. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

   Use clear, descriptive commit messages following conventional commits:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `style:` for formatting changes
   - `refactor:` for code refactoring
   - `test:` for adding tests

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** on GitHub:
   - Provide a clear description of your changes
   - Reference any related issues
   - Include screenshots if UI changes are involved

## Areas for Contribution

- **Bug fixes**: Report and fix issues
- **New features**: Add functionality to the parser or template system
- **Documentation**: Improve guides, examples, and API documentation
- **Templates**: Enhance or create new template designs
- **Testing**: Add test cases and improve test coverage
- **Performance**: Optimize parsing and rendering

## Questions?

If you have questions or need help, please:
- Open an issue on GitHub
- Check existing documentation in the `docs/` directory

Thank you for contributing! 🎉

