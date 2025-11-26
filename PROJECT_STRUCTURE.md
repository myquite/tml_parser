# Project Structure

This document describes the organization of the TML Parser project.

## 📁 Directory Structure

```
tml_parser_demo/
│
├── 📄 Core Files
│   ├── tml_to_site.py          # Main parser and site generator
│   ├── template_engine.py       # Template rendering engine
│   ├── tml-v0.1.xsd            # XSD schema definition
│   └── requirements.txt        # Optional dependencies
│
├── 📚 Documentation
│   ├── README.md                # Main project README
│   ├── LICENSE                  # MIT License
│   ├── CONTRIBUTING.md          # Contribution guidelines
│   ├── CHANGELOG.md             # Version history
│   ├── PROJECT_STRUCTURE.md      # This file
│   │
│   └── docs/                    # Documentation directory
│       ├── README.md            # Documentation index
│       └── TML_SCHEMA_EXAMPLE.md # Complete TML schema guide
│
├── 📝 Examples
│   └── examples/                # Example TML course files
│       ├── README.md            # Examples guide
│       ├── sample_course.tml    # Simple JavaScript course
│       └── example_course.tml   # Comprehensive web dev course
│
└── 🎨 Templates
    └── templates/               # HTML templates
        ├── README.md            # Template documentation
        ├── base.html            # Base template
        ├── index.html           # Course index
        ├── lesson.html          # Lesson page
        └── partials/            # Reusable components
            ├── styles.html     # CSS
            ├── scripts.html    # JavaScript
            ├── slide.html      # Slide component
            └── ...             # Other partials
```

## 📂 Directory Purposes

### Root Directory
- **Core Python files**: Main parser and template engine
- **Schema file**: XSD definition for validation
- **Configuration**: `.gitignore`, `requirements.txt`
- **Documentation**: Main README, LICENSE, contributing guide

### `docs/`
Contains all project documentation:
- Schema documentation
- API references
- Guides and tutorials

### `examples/`
Example TML course files:
- Simple examples for learning
- Comprehensive examples showcasing features
- Use as templates for new courses

### `templates/`
HTML template system:
- Base templates for pages
- Partial components for reuse
- Styles and scripts

## 🗂️ File Organization Principles

1. **Separation of Concerns**
   - Documentation in `docs/`
   - Examples in `examples/`
   - Templates in `templates/`

2. **Clear Naming**
   - Descriptive file names
   - Consistent naming conventions
   - README files in each directory

3. **GitHub Best Practices**
   - Comprehensive README
   - Contributing guidelines
   - License file
   - Changelog
   - Proper .gitignore

4. **User-Friendly**
   - Clear documentation structure
   - Examples for quick start
   - Well-organized templates

## 📋 Key Files

### Documentation
- `README.md` - Project overview and quick start
- `docs/TML_SCHEMA_EXAMPLE.md` - Complete TML reference
- `CONTRIBUTING.md` - How to contribute
- `CHANGELOG.md` - Version history

### Examples
- `examples/sample_course.tml` - Beginner-friendly example
- `examples/example_course.tml` - Feature-complete example

### Configuration
- `.gitignore` - Git ignore patterns
- `requirements.txt` - Optional dependencies
- `LICENSE` - MIT License

## 🔄 Generated Files (Gitignored)

The following directories are generated and should not be committed:
- `site/` - Generated output
- `site_example/` - Example output
- `test_output/` - Test output
- `__pycache__/` - Python cache

## 📝 Adding New Files

When adding new files:

1. **Documentation**: Place in `docs/` with appropriate README
2. **Examples**: Add to `examples/` with description in README
3. **Templates**: Add to `templates/` following existing structure
4. **Core code**: Add to root or appropriate subdirectory

## 🎯 Best Practices

- Keep related files together
- Document new features
- Update relevant README files
- Follow existing naming conventions
- Update CHANGELOG.md for significant changes

---

This structure is designed to be:
- ✅ Easy to navigate
- ✅ Well-documented
- ✅ GitHub-ready
- ✅ User-friendly
- ✅ Maintainable

