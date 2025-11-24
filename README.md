# TML Parser & Static Site Generator

A simple parser for TML (Teaching Markup Language) v0.1 that generates static HTML websites from course XML files. No external dependencies required.

## Features

- Parse TML v0.1 XML course files
- Generate static HTML websites
- Template system for easy customization
- Support for lessons, modules, activities, and assessments
- Progress tracking with localStorage
- Quiz/assessment functionality

## Quick Start

1. Create a TML course file (see `sample_course.tml` for an example)

2. Generate the website:
   ```bash
   python3 tml_to_site.py sample_course.tml site/
   ```

3. Open `site/index.html` in your browser

## Usage

```bash
python3 tml_to_site.py <input.tml> <output_dir> [template_dir]
```

- `input.tml` - Path to your TML course file
- `output_dir` - Directory where HTML files will be generated
- `template_dir` - (Optional) Custom template directory. Defaults to `templates/` if it exists

## Customization

The project includes a flexible template system. To customize the appearance:

1. Edit templates in the `templates/` directory
2. Modify `templates/partials/styles.html` to change the CSS
3. Edit `templates/base.html` to change the page structure
4. Customize individual components in `templates/partials/`

See `templates/README.md` for detailed template documentation.

## Project Structure

```
.
├── tml_to_site.py          # Main parser and generator
├── template_engine.py      # Template system
├── sample_course.tml       # Example TML file
├── templates/              # Template files
│   ├── base.html
│   ├── partials/
│   │   ├── styles.html
│   │   ├── scripts.html
│   │   └── ...
│   └── README.md
└── site/                   # Generated output (gitignored)
```

## Requirements

- Python 3.6+ (uses only standard library)

## License

See LICENSE file for details.

