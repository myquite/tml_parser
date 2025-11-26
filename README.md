# TML Parser & Static Site Generator

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python-based parser for **TML (Teaching Markup Language) v0.1** that generates beautiful, interactive static HTML websites from course XML files. Perfect for creating online courses, tutorials, and educational content.

## ✨ Features

- 📚 **Parse TML v0.1 XML course files** - Structured course definition format
- 🎨 **Template-based generation** - Fully customizable HTML templates
- 📱 **Responsive design** - Works on desktop, tablet, and mobile
- 🎯 **Interactive activities** - Coding exercises, reflections, projects, and labs
- 📝 **Assessments** - Multiple choice, multiple select, true/false, and short answer questions
- 💡 **Worked examples** - Interactive code examples with live execution
- 📊 **Progress tracking** - LocalStorage-based progress persistence
- 🔒 **XSS protection** - HTML escaping for secure content rendering
- ✅ **XSD validation** - Schema validation for TML files (optional)

## 🚀 Quick Start

### Installation

No installation required! Just clone the repository:

```bash
git clone https://github.com/your-username/tml_parser_demo.git
cd tml_parser_demo
```

### Basic Usage

1. **Create or use an example TML course file**:
   ```bash
   # Use the provided example
   python3 tml_to_site.py examples/sample_course.tml site/
   ```

2. **Open the generated site**:
   ```bash
   open site/index.html  # macOS
   # or
   xdg-open site/index.html  # Linux
   # or just open it in your browser
   ```

### Example

```bash
# Generate a course website
python3 tml_to_site.py examples/example_course.tml output/

# With custom templates
python3 tml_to_site.py examples/example_course.tml output/ custom_templates/

# Skip XSD validation
python3 tml_to_site.py examples/example_course.tml output/ --no-validate
```

## 📖 Documentation

- **[TML Schema Documentation](docs/TML_SCHEMA_EXAMPLE.md)** - Complete guide to the TML format
- **[Template Documentation](templates/README.md)** - How to customize templates
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[Changelog](CHANGELOG.md)** - Version history and changes

## 🏗️ Project Structure

```
tml_parser_demo/
├── tml_to_site.py          # Main parser and site generator
├── template_engine.py       # Template rendering engine
├── tml-v0.1.xsd            # XSD schema definition
│
├── examples/                # Example TML course files
│   ├── sample_course.tml    # Simple JavaScript variables course
│   └── example_course.tml   # Comprehensive web development course
│
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── index.html           # Course index page
│   ├── lesson.html          # Lesson page template
│   └── partials/            # Reusable template components
│       ├── styles.html      # CSS styles
│       ├── scripts.html     # JavaScript
│       ├── slide.html       # Slide component
│       └── ...
│
├── docs/                    # Documentation
│   └── TML_SCHEMA_EXAMPLE.md
│
├── README.md                # This file
├── LICENSE                  # MIT License
├── CONTRIBUTING.md          # Contribution guidelines
├── CHANGELOG.md             # Version history
└── requirements.txt         # Optional dependencies
```

## 🎓 What is TML?

TML (Teaching Markup Language) is an XML-based format for defining educational courses. It supports:

- **Modules and Lessons** - Hierarchical course structure
- **Content Sections** - Markdown, HTML, or plain text
- **Activities** - Coding, reading, reflection, projects, labs
- **Assessments** - Quizzes with multiple question types
- **Resources** - External links and materials
- **Badges** - Achievement system
- **Grading** - Flexible grading schemes

See the [TML Schema Documentation](docs/TML_SCHEMA_EXAMPLE.md) for complete details.

## 🛠️ Requirements

- **Python 3.8+** (uses only standard library)
- **Optional**: `lxml` for XSD schema validation
  ```bash
  pip install -r requirements.txt
  ```

## 🎨 Customization

### Templates

The project uses a flexible template system. Customize the appearance by editing files in `templates/`:

- **Styles**: `templates/partials/styles.html` - CSS customization
- **Layout**: `templates/base.html` - Page structure
- **Components**: `templates/partials/` - Individual UI components

See [Template Documentation](templates/README.md) for details.

### Example Customization

```bash
# Use custom templates
python3 tml_to_site.py course.tml output/ my_custom_templates/
```

## 🔍 XSD Schema Validation

By default, TML files are validated against `tml-v0.1.xsd` before parsing:

- **With lxml**: Full XSD validation with detailed error messages
- **Without lxml**: Validation skipped (graceful degradation)

Install lxml for full validation:
```bash
pip install lxml
```

## 📝 Example TML File

```xml
<?xml version="1.0" encoding="UTF-8"?>
<course id="my-course" title="My Course" level="beginner" duration="P4W">
  <objective>Learn something new</objective>
  
  <module id="mod-1" title="Module 1">
    <lesson id="les-1" title="Lesson 1">
      <content format="markdown">
        ## Welcome
        
        This is a lesson about...
      </content>
      
      <activity id="act-1" type="coding" est="PT15M">
        <instructions>Write some code...</instructions>
      </activity>
      
      <assessment id="quiz-1" type="quiz" passScore="70">
        <question id="q1" type="mcq" points="10">
          <stem>What is the answer?</stem>
          <choice correct="true">Correct answer</choice>
          <choice>Wrong answer</choice>
        </question>
      </assessment>
    </lesson>
  </module>
</course>
```

See `examples/` directory for complete examples.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- TML v0.1 schema definition
- All contributors and users

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/tml_parser_demo/issues)
- **Documentation**: See `docs/` directory
- **Examples**: See `examples/` directory

---

Made with ❤️ for educators and learners
