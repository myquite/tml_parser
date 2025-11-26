# TML Schema Example Documentation

This document explains the TML (Teaching Markup Language) v0.1 schema structure using the concrete example in `example_course.tml`.

## Overview

TML is an XML-based format for defining educational courses. It supports:
- Structured course content (modules, lessons, content sections)
- Multiple activity types (coding, reading, reflection, project, lab)
- Various assessment types (quiz, coding challenges)
- Resources, badges, and grading schemes

## Schema Structure

### Root Element: `<course>`

The root element defines the entire course with required attributes:

```xml
<course id="web-dev-intro" 
        title="Introduction to Web Development" 
        level="beginner" 
        duration="P8W" 
        version="1.0" 
        lang="en">
```

**Attributes:**
- `id` (required): Unique identifier for the course
- `title` (required): Course title
- `level` (optional): `beginner` | `intermediate` | `advanced` | `mixed`
- `duration` (optional): ISO 8601 duration (e.g., `P8W` = 8 weeks, `PT45M` = 45 minutes)
- `version` (optional): Course version string
- `lang` (optional): Language code (e.g., `en`, `es`, `fr`)

### Course-Level Elements

#### `<meta>` - Course Metadata

```xml
<meta>
  <description>Course description...</description>
  <author>Author Name</author>
  <tag>tag-name</tag>
</meta>
```

#### `<prereq>` - Prerequisites

References other courses or modules:

```xml
<prereq ref="computer-basics">Basic computer skills</prereq>
```

#### `<objective>` - Learning Objectives

```xml
<objective level="beginner">Understand HTML structure</objective>
```

**Attributes:**
- `level` (optional): Objective difficulty level

### `<module>` - Course Modules

Modules group related lessons:

```xml
<module id="html-basics" title="HTML Fundamentals" order="1" duration="P2W">
  <objective>Create well-structured HTML documents</objective>
  <lesson>...</lesson>
</module>
```

**Attributes:**
- `id` (optional): Unique identifier
- `title` (required): Module title
- `order` (optional): Display order
- `duration` (optional): ISO 8601 duration

### `<lesson>` - Individual Lessons

Lessons contain content, activities, and assessments:

```xml
<lesson id="html-structure" title="HTML Document Structure" order="1" duration="PT30M">
  <content>...</content>
  <activity>...</activity>
  <assessment>...</assessment>
</lesson>
```

**Attributes:**
- `id` (optional): Unique identifier
- `title` (required): Lesson title
- `order` (optional): Display order
- `duration` (optional): ISO 8601 duration
- `visibility` (optional): `public` | `private` | `locked` | `beta`

### `<content>` - Content Sections

Content sections are rendered as slides in the lesson:

```xml
<content format="markdown">
  ## Heading
  Paragraph text with **bold** and *italic*.
</content>
```

**Attributes:**
- `format` (optional): `markdown` | `html` | `text` (default: `markdown`)
- `lang` (optional): Language code

**Formats:**
- **markdown**: Supports headings, lists, bold, italic, code blocks, inline code
- **html**: Raw HTML content (use with caution - content is escaped for security)
- **text**: Plain text (minimal formatting)

### `<activity>` - Learning Activities

Activities provide hands-on practice:

```xml
<activity id="html-practice-1" type="coding" est="PT15M">
  <instructions>Create an HTML document...</instructions>
  <expected>Your HTML should include...</expected>
</activity>
```

**Attributes:**
- `id` (optional): Unique identifier
- `type` (required): `coding` | `reading` | `reflection` | `project` | `lab`
- `est` (optional): Estimated time (ISO 8601 duration)
- `tool` (optional): Tool or platform name

**Activity Types:**
- **coding**: Programming exercises with code editors
- **reading**: Reading materials (can include worked examples with code)
- **reflection**: Reflective writing prompts
- **project**: Larger, multi-step projects with rubrics
- **lab**: Hands-on lab exercises

**Elements:**
- `<instructions>`: What the learner should do
- `<input>`: Starter code or input data
- `<expected>`: Expected output or solution description
- `<rubric>`: Grading criteria (for projects)

### `<assessment>` - Assessments

Assessments evaluate learner understanding:

```xml
<assessment id="html-quiz-1" type="quiz" passScore="70" attempts="3">
  <question>...</question>
</assessment>
```

**Attributes:**
- `id` (optional): Unique identifier
- `type` (required): `quiz` | `coding` | `scenario`
- `passScore` (optional): Passing percentage (0-100)
- `attempts` (optional): Maximum number of attempts

### `<question>` - Assessment Questions

Questions can be multiple types:

#### Multiple Choice (MCQ)

```xml
<question id="q1" type="mcq" points="10">
  <stem>What does HTML stand for?</stem>
  <choice correct="true">HyperText Markup Language</choice>
  <choice>High-Level Text Markup Language</choice>
</question>
```

#### Multiple Select (MSQ)

```xml
<question id="q2" type="msq" points="15">
  <stem>Select all semantic HTML5 elements:</stem>
  <choice correct="true">&lt;header&gt;</choice>
  <choice correct="true">&lt;nav&gt;</choice>
  <choice>&lt;div&gt;</choice>
</question>
```

#### True/False

```xml
<question id="q3" type="truefalse" points="10">
  <statement>All HTML tags must have a closing tag.</statement>
  <answer value="false"/>
</question>
```

#### Short Answer

```xml
<question id="q4" type="short" points="20">
  <prompt>What is the purpose of the meta charset tag?</prompt>
  <solution>It specifies the character encoding...</solution>
</question>
```

#### Code Question

```xml
<question id="css-q1" type="code" points="50">
  <prompt>Write CSS to style a navigation bar...</prompt>
  <lang>css</lang>
  <starter>/* Your CSS here */</starter>
  <solution>nav { background-color: #333; }</solution>
</question>
```

**Question Types:**
- `mcq`: Multiple choice (single correct answer)
- `msq`: Multiple select (multiple correct answers)
- `truefalse`: True/false questions
- `short`: Short answer questions
- `long`: Long-form essay questions
- `code`: Coding challenges
- `matching`: Matching pairs
- `ordering`: Ordering/sequencing

### `<resource>` - External Resources

Links to external learning materials:

```xml
<resource id="mdn-html" type="link" href="https://developer.mozilla.org/en-US/docs/Web/HTML" lang="en">
  <title>MDN HTML Documentation</title>
</resource>
```

**Attributes:**
- `id` (optional): Unique identifier
- `type` (optional): `link` | `pdf` | `video` | `image` | `dataset` | `slides`
- `href` (required): Resource URL
- `lang` (optional): Language code

### `<badge>` - Achievement Badges

Badges reward learner accomplishments:

```xml
<badge id="html-master" name="HTML Master" trigger="completeModule" threshold="80">
  <desc>Earned by completing the HTML Fundamentals module with at least 80% score</desc>
</badge>
```

**Attributes:**
- `id` (required): Unique identifier
- `name` (required): Badge display name
- `trigger` (required): `completeLesson` | `completeModule` | `scoreAtLeast`
- `threshold` (optional): Percentage threshold for `scoreAtLeast` trigger

### `<grading>` - Grading Scheme

Defines how course grades are calculated:

```xml
<grading scheme="weighted" passing="70">
  <weight type="module" ref="html-basics" percent="30"/>
  <weight type="module" ref="css-basics" percent="35"/>
  <weight type="module" ref="js-basics" percent="35"/>
</grading>
```

**Attributes:**
- `scheme` (optional): `points` | `weighted`
- `passing` (optional): Passing percentage (0-100)

**Weight Types:**
- `lesson`: Weight for a specific lesson
- `activity`: Weight for a specific activity
- `assessment`: Weight for a specific assessment
- `module`: Weight for a module (sum of its lessons/activities)

## Best Practices

1. **Use semantic IDs**: Choose descriptive, unique IDs (e.g., `html-structure`, not `lesson1`)

2. **ISO 8601 Durations**: Use proper duration format:
   - `P6W` = 6 weeks
   - `PT45M` = 45 minutes
   - `P1D` = 1 day
   - `PT2H30M` = 2 hours 30 minutes

3. **Content Format**: Prefer `markdown` for readability and maintainability

4. **Activity Instructions**: Be clear and specific about what learners should do

5. **Assessment Questions**: 
   - Use appropriate question types for the learning objective
   - Provide clear stems/prompts
   - Include distractors in multiple choice questions

6. **Prerequisites**: Reference other courses/modules by their IDs

7. **Resources**: Include relevant external links to supplement learning

## Validation

The TML parser validates files against `tml-v0.1.xsd` before parsing. To enable full validation, install `lxml`:

```bash
pip install lxml
```

Then run the parser normally - validation happens automatically:

```bash
python3 tml_to_site.py example_course.tml site/
```

To skip validation:

```bash
python3 tml_to_site.py example_course.tml site/ --no-validate
```

## Example Files

- **`example_course.tml`**: Comprehensive example demonstrating all schema features
- **`sample_course.tml`**: Simpler example focused on JavaScript variables
- **`tml-v0.1.xsd`**: XML Schema Definition for validation

## See Also

- [README.md](README.md) - Project overview and usage
- [tml-v0.1.xsd](tml-v0.1.xsd) - Complete schema definition

