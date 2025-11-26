# Example TML Courses

This directory contains example TML course files demonstrating various features of the TML format.

## 📚 Available Examples

### `sample_course.tml`
A focused introduction to JavaScript Variables. Perfect for beginners learning the TML format.

**Features demonstrated:**
- Basic course structure
- Content sections with markdown
- Interactive worked examples (reading activities with code)
- Coding activities
- Quiz assessments with multiple question types

**Topics covered:**
- Variable declarations (let, const, var)
- Data types
- Variable naming conventions
- Best practices

### `example_course.tml`
A comprehensive "Introduction to Web Development" course showcasing all TML features.

**Features demonstrated:**
- Complete course structure with metadata
- Prerequisites
- Multiple modules and lessons
- All activity types (coding, reading, reflection, project, lab)
- All assessment question types (MCQ, MSQ, true/false, short answer, code)
- Resources and badges
- Grading schemes

**Topics covered:**
- HTML fundamentals
- CSS styling
- JavaScript basics

## 🚀 Using Examples

### Generate a course from an example:

```bash
# From project root
python3 tml_to_site.py examples/sample_course.tml site/

# Or with the comprehensive example
python3 tml_to_site.py examples/example_course.tml site/
```

### Use as templates:

1. Copy an example file:
   ```bash
   cp examples/sample_course.tml my_course.tml
   ```

2. Edit the content to match your course

3. Generate your site:
   ```bash
   python3 tml_to_site.py my_course.tml output/
   ```

## 📖 Learning from Examples

### For TML Authors:
- Study the structure and organization
- See how different elements are used
- Learn best practices for content formatting
- Understand activity and assessment patterns

### For Developers:
- See how TML is parsed and rendered
- Understand the relationship between TML and generated HTML
- Learn about the template system

## 🔍 Example Highlights

### Interactive Worked Examples
The examples show how to create interactive code examples:
```xml
<activity id="example-1" type="reading" est="PT15M">
  <expected format="markdown">
    ```javascript
    let age = 25;
    ```
  </expected>
</activity>
```

### Multiple Question Types
See how different question types are structured:
- Multiple choice (MCQ)
- Multiple select (MSQ)
- True/False
- Short answer
- Code questions

### Activity Variety
Examples of all activity types:
- **Coding**: Programming exercises
- **Reading**: Content with worked examples
- **Reflection**: Writing prompts
- **Project**: Larger assignments with rubrics
- **Lab**: Hands-on exercises

## 💡 Tips

1. **Start simple**: Begin with `sample_course.tml` to understand basics
2. **Explore features**: Use `example_course.tml` to see advanced features
3. **Modify and test**: Copy examples and experiment
4. **Validate**: Always validate your TML files before generating

## 📚 Related Documentation

- **[TML Schema Documentation](../docs/TML_SCHEMA_EXAMPLE.md)** - Complete schema reference
- **[Main README](../README.md)** - Project overview
- **[Template Documentation](../templates/README.md)** - Customization guide

---

Happy course creating! 🎓

