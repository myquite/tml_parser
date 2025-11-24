# Template System

This directory contains templates for customizing the generated HTML output. The template system supports:

- **Base templates**: Main page structure (`base.html`)
- **Partials**: Reusable components (`partials/`)
- **Variable substitution**: Use `{{ variable_name }}` in templates
- **Partial inclusion**: Use `{{> partial_name }}` to include partials

## Directory Structure

```
templates/
├── base.html              # Base page template
├── index.html             # Index page template (extends base)
├── lesson.html            # Lesson page template (extends base)
└── partials/
    ├── header.html        # Page header
    ├── footer.html        # Page footer
    ├── styles.html        # CSS styles
    ├── scripts.html       # JavaScript
    ├── index_header.html  # Index page header content
    ├── lesson_header.html # Lesson page header content
    ├── module_card.html   # Module card component
    ├── lesson_item.html   # Lesson list item
    ├── activity.html      # Activity component
    ├── assessment.html    # Assessment/quiz component
    └── question.html      # Question component
```

## Customization

### Customizing Styles

To customize the appearance, edit `partials/styles.html`:

```html
<style>
:root{
  --accent: #your-color;
}
body {
  background: #your-background;
  color: #your-text-color;
}
/* Add your custom styles */
</style>
```

### Customizing Layout

Edit `base.html` to change the overall page structure:

```html
<!doctype html>
<html>
<head>
  <title>{{ title }}</title>
  {{> styles }}
</head>
<body>
  {{ header_html }}
  <main>
    {{ content }}
  </main>
  {{> footer }}
  {{> scripts }}
</body>
</html>
```

### Customizing Components

Edit any partial in `partials/` to customize specific components. For example, to change how activities are displayed, edit `partials/activity.html`.

## Usage

The template system automatically uses templates from this directory. To use custom templates:

1. Copy this `templates/` directory to your project
2. Modify the templates as needed
3. Run the generator with the template directory:

```bash
python tml_to_site.py course.tml output/ templates/
```

If no template directory is specified, the system will use the default templates from this directory if it exists, or fall back to built-in defaults.

## Template Variables

### Base Template Variables
- `{{ title }}` - Page title
- `{{ course_id }}` - Course ID
- `{{ total_lessons }}` - Total number of lessons
- `{{ header_html }}` - Rendered header HTML
- `{{ content }}` - Main page content

### Index Page Variables
- `{{ title }}` - Course title
- `{{ level }}` - Course level
- `{{ duration }}` - Course duration

### Lesson Page Variables
- `{{ lesson_title }}` - Lesson title
- `{{ module_title }}` - Module title

## Partials

Partials are included using `{{> partial_name }}`. The system will look for:
1. `partials/partial_name.html` in the template directory
2. Built-in defaults if not found

Available partials:
- `styles` - CSS styles
- `scripts` - JavaScript
- `header` - Page header wrapper
- `footer` - Page footer

