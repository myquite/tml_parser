# Changelog

All notable changes to TML Parser will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- XSD schema validation support (optional, requires lxml)
- Comprehensive example course file (`examples/example_course.tml`)
- Documentation in `docs/` directory
- Interactive worked examples for reading activities
- Improved assessment question spacing and layout
- HTML escaping for XSS protection
- User-friendly error messages for missing TML attributes

### Changed
- Improved assessment slide layout and spacing
- Enhanced question rendering (removed `<br>` tags, better flexbox layout)
- Better visual feedback for selected quiz options
- Improved overall UI spacing and typography

### Fixed
- Code blocks in markdown not rendering correctly
- Assessment choices being cut off or poorly spaced
- XSS vulnerabilities in user-supplied content
- Missing attribute validation errors

## [0.1.0] - 2024-11-25

### Added
- Initial release
- TML v0.1 parser
- Template engine with partials support
- Slide-based lesson UI
- Activity types: coding, reading, reflection, project, lab
- Assessment types: quiz (MCQ, MSQ, true/false, short answer)
- Progress tracking with localStorage
- Interactive code execution for worked examples

