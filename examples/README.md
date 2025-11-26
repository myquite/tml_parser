# Example TML Courses

This directory contains example TML course files demonstrating various features of the TML format.

## 📚 Available Examples

### `example_course.tml`
A comprehensive "Python Programming Basics" course showcasing all TML features and question types.

**Features demonstrated:**
- Complete course structure with metadata
- Prerequisites
- Multiple modules and lessons
- All activity types (coding, reading, reflection, project, lab)
- **All 8 assessment question types** (MCQ, MSQ, true/false, short answer, long answer, code, matching, ordering)
- Resources and badges
- Grading schemes

**Topics covered:**
- Python basics and syntax
- Variables and data types
- Control flow (if/else, loops)
- Functions

## 🚀 Using Examples

### Generate a course from an example:

```bash
# From project root
python3 tml_to_site.py examples/example_course.tml site/
```

### Use as templates:

1. Copy an example file:
   ```bash
   cp examples/example_course.tml my_course.tml
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
- See examples of all 8 question types in action

### For Developers:
- See how TML is parsed and rendered
- Understand the relationship between TML and generated HTML
- Learn about the template system

## 🔍 Example Highlights

### Interactive Worked Examples
The example shows how to create interactive code examples:
```xml
<activity id="example-1" type="reading" est="PT15M">
  <expected format="markdown">
    ```python
    print("Hello, World!")
    ```
  </expected>
</activity>
```

### All Question Types
See how all 8 question types are structured:
- Multiple choice (MCQ)
- Multiple select (MSQ)
- True/False
- Short answer
- Long answer
- Code questions
- Matching questions
- Ordering questions

### Activity Variety
Examples of all activity types:
- **Coding**: Programming exercises
- **Reading**: Content with worked examples
- **Reflection**: Writing prompts
- **Project**: Larger assignments with rubrics
- **Lab**: Hands-on exercises

## 💡 Tips

1. **Start with the example**: Use `example_course.tml` to see all features
2. **Explore all question types**: The example includes all 8 question types
3. **Modify and test**: Copy the example and experiment
4. **Validate**: Always validate your TML files before generating

## 📚 Related Documentation

- **[TML Schema Documentation](../docs/TML_SCHEMA_EXAMPLE.md)** - Complete schema reference
- **[Main README](../README.md)** - Project overview
- **[Template Documentation](../templates/README.md)** - Customization guide

---

Happy course creating! 🎓

