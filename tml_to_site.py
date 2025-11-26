#!/usr/bin/env python3
"""
TML v0.1 Parser & Static Site Generator (no external deps).

Usage:
  python tml_to_site.py path/to/course.tml out_dir/ [template_dir]
"""
import os, re
import html
from xml.etree import ElementTree as ET
from template_engine import TemplateEngine

def escape_html(text: str) -> str:
    """Escape HTML special characters to prevent XSS."""
    if text is None:
        return ""
    return html.escape(str(text), quote=True)

def safe_markdown(md: str) -> str:
    """
    Safely render markdown with HTML escaping.
    User content is escaped, but markdown formatting is preserved.
    """
    if not md:
        return ""
    
    md = md.strip()
    
    # First, extract and replace code blocks (```...```)
    code_blocks = []
    code_block_placeholder = "___CODE_BLOCK_{}___"
    
    def replace_code_block(match):
        idx = len(code_blocks)
        lang = match.group(1) or ""
        code = match.group(2)
        # Escape code content for safety
        code_blocks.append((lang, escape_html(code)))
        return code_block_placeholder.format(idx)
    
    # Match code blocks: ```lang\ncode\n```
    md = re.sub(r"```(\w+)?\n(.*?)```", replace_code_block, md, flags=re.DOTALL)
    
    # Escape the entire markdown text first (except our placeholders)
    # We'll unescape specific parts after processing
    md_escaped = escape_html(md)
    
    # Restore code block placeholders (they're safe)
    for idx in range(len(code_blocks)):
        md_escaped = md_escaped.replace(escape_html(code_block_placeholder.format(idx)), code_block_placeholder.format(idx))
    
    # Now process markdown formatting on escaped text
    # Bold: **text** -> <strong>text</strong>
    md_escaped = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', md_escaped)
    # Italic: *text* -> <em>text</em> (but not if it's part of **)
    md_escaped = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', md_escaped)
    
    # Process lines
    lines = []
    for line in md_escaped.splitlines():
        s = line.strip()
        
        # Check if this line is a code block placeholder
        code_match = re.match(r"___CODE_BLOCK_(\d+)___", s)
        if code_match:
            idx = int(code_match.group(1))
            lang, code = code_blocks[idx]
            # Code is already escaped
            code_html = f'<pre><code class="language-{escape_html(lang)}">{code.strip()}</code></pre>'
            lines.append(code_html)
            continue
        
        if s.startswith("### "): 
            lines.append(f"<h3>{s[4:]}</h3>")
        elif s.startswith("## "): 
            lines.append(f"<h2>{s[3:]}</h2>")
        elif s.startswith("# "):  
            lines.append(f"<h1>{s[2:]}</h1>")
        elif s.startswith("- "):  
            lines.append(f"<li>{s[2:]}</li>")
        else:
            lines.append("" if s=="" else f"<p>{s}</p>")
    
    # Handle inline code (single backticks) - do this after processing lines
    processed_lines = []
    for line in lines:
        # Only process inline code in paragraph/list/heading tags, not in code blocks
        if line.startswith("<p>") or line.startswith("<li>") or line.startswith("<h"):
            # Replace inline code - content is already escaped
            line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)
        processed_lines.append(line)
    
    # Build output with list handling
    in_ul = False
    out = []
    for l in processed_lines:
        if l.startswith("<li>"):
            if not in_ul: 
                out.append("<ul>")
                in_ul = True
            out.append(l)
        else:
            if in_ul: 
                out.append("</ul>")
                in_ul = False
            out.append(l)
    if in_ul: 
        out.append("</ul>")
    
    return "\n".join(out)

def safe_filename(name: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9_-]+", "-", name.strip().lower())
    name = re.sub(r"-+", "-", name).strip("-")
    return name or "lesson"

def mini_markdown(md: str) -> str:
    """Legacy function - use safe_markdown for new code."""
    return safe_markdown(md)


class TContent:
    def __init__(self, fmt, lang, value): self.format, self.lang, self.value = fmt, lang, value
class TQuestion:
    def __init__(self, qtype, points, data): self.type, self.points, self.data = qtype, points, data
class TAssessment:
    def __init__(self, aid, atype, passScore, questions): self.id, self.type, self.passScore, self.questions = aid, atype, passScore, questions
class TActivity:
    def __init__(self, aid, atype, est, instructions, expected): 
        self.id, self.type, self.est, self.instructions, self.expected = aid, atype, est, instructions, expected
class TLesson:
    def __init__(self, lid, title, duration, content, activities, assessments, module_title):
        self.id, self.title, self.duration = lid, title, duration
        self.content, self.activities, self.assessments = content, activities, assessments
        self.module_title = module_title
class TModule:
    def __init__(self, mid, title, order, lessons):
        self.id, self.title, self.order, self.lessons = mid, title, order, lessons
class TCourse:
    def __init__(self, cid, title, level, duration, objectives, modules):
        self.id, self.title, self.level, self.duration = cid, title, level or "", duration or ""
        self.objectives, self.modules = objectives, modules

class TMLParseError(Exception):
    """Custom exception for TML parsing errors with user-friendly messages."""
    pass

def get_required_attr(element, attr_name, element_name=None, element_id=None):
    """
    Get a required attribute from an XML element with user-friendly error reporting.
    
    Args:
        element: XML element
        attr_name: Name of the required attribute
        element_name: Type of element (e.g., 'module', 'lesson') for error messages
        element_id: ID of the element for error messages
    
    Returns:
        Attribute value
    
    Raises:
        TMLParseError: If attribute is missing
    """
    value = element.attrib.get(attr_name)
    if value is None:
        element_type = element_name or element.tag
        element_identifier = f" with id '{element_id}'" if element_id else ""
        available_attrs = ", ".join(element.attrib.keys()) if element.attrib else "none"
        raise TMLParseError(
            f"Missing required attribute '{attr_name}' on <{element_type}> element{element_identifier}.\n"
            f"Available attributes: {available_attrs if available_attrs else 'none'}\n"
            f"Please add the '{attr_name}' attribute to this element."
        )
    return value

def validate_tml_xsd(tml_path: str, xsd_path: str = None):
    """
    Validate TML file against XSD schema.
    
    Args:
        tml_path: Path to TML file
        xsd_path: Path to XSD schema file. If None, looks for tml-v0.1.xsd in same directory.
    
    Returns:
        Tuple of (is_valid, error_message)
        If lxml is not available, returns (True, "XSD validation skipped (lxml not installed)")
    """
    try:
        from lxml import etree
    except ImportError:
        return (True, "XSD validation skipped (lxml not installed - install with: pip install lxml)")
    
    # Find XSD file
    if xsd_path is None:
        tml_dir = os.path.dirname(os.path.abspath(tml_path))
        xsd_path = os.path.join(tml_dir, 'tml-v0.1.xsd')
        # Also try in current directory
        if not os.path.exists(xsd_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            xsd_path = os.path.join(script_dir, 'tml-v0.1.xsd')
    
    if not os.path.exists(xsd_path):
        return (True, f"XSD validation skipped (schema file not found: {xsd_path})")
    
    try:
        # Parse and validate
        xmlschema_doc = etree.parse(xsd_path)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        
        xml_doc = etree.parse(tml_path)
        xmlschema.assertValid(xml_doc)
        return (True, "XSD validation passed")
    except etree.XMLSchemaParseError as e:
        return (False, f"XSD schema error: {e}")
    except etree.DocumentInvalid as e:
        return (False, f"TML file does not match schema: {e}")
    except etree.XMLSyntaxError as e:
        return (False, f"XML syntax error: {e}")
    except Exception as e:
        return (False, f"Validation error: {e}")

def parse_tml(path: str, validate: bool = True) -> TCourse:
    """
    Parse TML file and return TCourse object.
    
    Args:
        path: Path to TML file
        validate: If True, validate against XSD schema before parsing
    
    Returns:
        TCourse object
    
    Raises:
        TMLParseError: If validation fails or parsing encounters errors
    """
    # Validate against XSD schema if requested
    if validate:
        is_valid, message = validate_tml_xsd(path)
        if not is_valid:
            raise TMLParseError(f"XSD validation failed: {message}")
        # Log validation success (optional, can be removed)
        # print(f"✓ {message}", file=sys.stderr)
    
    tree = ET.parse(path)
    root = tree.getroot()
    cid = root.attrib.get("id")
    title = root.attrib.get("title","")
    level = root.attrib.get("level","")
    duration = root.attrib.get("duration","")
    objectives = [ (obj.text or "").strip() for obj in root.findall("./objective") if (obj.text or "").strip() ]
    modules=[]
    for m in root.findall("./module"):
        mid = m.attrib.get("id","")
        try:
            mtitle = get_required_attr(m, "title", "module", mid)
        except TMLParseError as e:
            raise TMLParseError(f"Error in module {mid or '(no id)'}: {e}")
        order = int(m.attrib.get("order","0") or "0")
        lessons=[]
        for l in m.findall("./lesson"):
            lid = l.attrib.get("id","")
            try:
                ltitle = get_required_attr(l, "title", "lesson", lid)
            except TMLParseError as e:
                raise TMLParseError(f"Error in lesson {lid or '(no id)'} of module '{mtitle}': {e}")
            lduration = l.attrib.get("duration","")
            content=[]
            for c in l.findall("./content"):
                fmt = c.attrib.get("format","markdown")
                lang = c.attrib.get("lang","")
                value = (c.text or "").strip()
                content.append(TContent(fmt, lang, value))
            activities=[]
            for a in l.findall("./activity"):
                aid = a.attrib.get("id","")
                atype = a.attrib.get("type","")
                est = a.attrib.get("est","")
                # Content will be escaped during rendering, but store raw for processing
                instructions = (a.findtext("./instructions") or "").strip()
                expected = (a.findtext("./expected") or "").strip()
                activities.append(TActivity(aid, atype, est, instructions, expected))
            assessments=[]
            for asmt in l.findall("./assessment"):
                aid = asmt.attrib.get("id","")
                atype = asmt.attrib.get("type","quiz")
                passScore = int(float(asmt.attrib.get("passScore","0") or "0"))
                questions=[]
                for q in asmt.findall("./question"):
                    qtype = q.attrib.get("type","mcq")
                    points = float(q.attrib.get("points","1"))
                    data={}
                    if qtype in ("mcq","msq"):
                        stem = (q.findtext("./stem") or "").strip()
                        choices=[]
                        for ch in q.findall("./choice"):
                            text = (ch.text or "").strip()
                            correct = ch.attrib.get("correct","false").lower()=="true"
                            choices.append({"text":text,"correct":correct})
                        data={"stem":stem,"choices":choices}
                    elif qtype=="truefalse":
                        statement = (q.findtext("./statement") or "").strip()
                        answer_el = q.find("./answer")
                        answer = (answer_el.attrib.get("value","false").lower() if answer_el is not None else "false")
                        data={"statement":statement,"answer":answer}
                    elif qtype in ("short", "long"):
                        prompt = (q.findtext("./prompt") or "").strip()
                        solution = (q.findtext("./solution") or "").strip()
                        data={"prompt":prompt,"solution":solution}
                    elif qtype=="code":
                        prompt = (q.findtext("./prompt") or "").strip()
                        lang = (q.findtext("./lang") or "").strip()
                        starter = (q.findtext("./starter") or "").strip()
                        tests = (q.findtext("./tests") or "").strip()
                        solution = (q.findtext("./solution") or "").strip()
                        data={"prompt":prompt,"lang":lang,"starter":starter,"tests":tests,"solution":solution}
                    elif qtype=="matching":
                        pairs=[]
                        for pair_el in q.findall("./pair"):
                            left = (pair_el.findtext("./left") or "").strip()
                            right = (pair_el.findtext("./right") or "").strip()
                            pairs.append({"left":left,"right":right})
                        data={"pairs":pairs}
                    elif qtype=="ordering":
                        items=[]
                        for item_el in q.findall("./item"):
                            item_text = (item_el.text or "").strip()
                            if item_text:
                                items.append(item_text)
                        data={"items":items}
                    else:
                        data={"raw":ET.tostring(q, encoding='unicode')}
                    questions.append(TQuestion(qtype, points, data))
                assessments.append(TAssessment(aid, atype, passScore, questions))
            lessons.append(TLesson(lid, ltitle, lduration, content, activities, assessments, mtitle))
        modules.append(TModule(mid, mtitle, order, lessons))
    modules.sort(key=lambda m: m.order)
    return TCourse(cid, title, level, duration, objectives, modules)

def render_course(course: TCourse, outdir: str, template_dir: str = None):
    os.makedirs(outdir, exist_ok=True)
    engine = TemplateEngine(template_dir)
    total_lessons = sum(len(m.lessons) for m in course.modules)
    
    # Render index page
    modules_html = []
    for m in course.modules:
        lessons_list = []
        for l in m.lessons:
            fname = f"{safe_filename(l.title)}.html"
            lesson_item_html = engine.render_with_defaults(
                'partials/lesson_item.html',
                {
                    'lesson_file': fname,
                    'lesson_title': l.title,
                    'duration': (l.duration or "")
                }
            )
            lessons_list.append(lesson_item_html)
        
        module_card_html = engine.render_with_defaults(
            'partials/module_card.html',
            {
                'mod_title': m.title,
                'lessons': "\n".join(lessons_list)
            }
        )
        modules_html.append(module_card_html)
    
    obj_items = "\n".join([f"<li>{o}</li>" for o in course.objectives])
    
    # Render index header
    index_header_html = engine.render_with_defaults(
        'partials/index_header.html',
        {
            'title': course.title,
            'level': course.level or "n/a",
            'duration': course.duration or "n/a"
        }
    )
    
    # Render main header partial
    header_html = engine.render_with_defaults(
        'partials/header.html',
        {'header_content': index_header_html}
    )
    
    # Build index content
    index_content = f"""<div class="card">
  <h2>Objectives</h2>
  <ul>{obj_items}</ul>
</div>
{chr(10).join(modules_html)}"""
    
    # Render base template for index
    index_html = engine.render_with_defaults(
        'base.html',
        {
            'title': f"{course.title} — Course",
            'course_id': course.id,
            'total_lessons': str(total_lessons),
            'content': index_content,
            'header_html': header_html
        }
    )
    
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # Render lesson pages with slides
    for m in course.modules:
        for l in m.lessons:
            slides = []
            slide_num = 0
            
            # Process content - create one slide per content section
            if l.content:
                for idx, c in enumerate(l.content):
                    # Process each content section individually
                    if c.format == "html":
                        # For HTML format, escape to prevent XSS
                        # Note: In production, consider using a proper HTML sanitizer like bleach
                        # that allows safe HTML tags while removing scripts
                        content_html = escape_html(c.value)
                    elif c.format == "markdown":
                        content_html = safe_markdown(c.value)
                    else:
                        content_html = f"<pre>{escape_html(c.value)}</pre>"
                    
                    # Render content slide for this section
                    content_slide_html = engine.render_with_defaults(
                        'partials/content_slide.html',
                        {'content_html': content_html}
                    )
                    
                    slide_num += 1
                    slide_html = engine.render_with_defaults(
                        'partials/slide.html',
                        {
                            'slide_type': 'content',
                            'slide_id': f'content-{l.id or safe_filename(l.title)}-{idx}',
                            'slide_content': content_slide_html,
                            'slide_number': str(slide_num),
                            'total_slides': '1'  # Will update later
                        }
                    )
                    slides.append(slide_html)

            # Render activity slides
            if l.activities:
                for a in l.activities:
                    est_html = f'<p class="small">Estimated time: {a.est}</p>' if a.est else ""
                    
                    # Check if this is a worked example (reading activity with code blocks)
                    is_example = (a.type.lower() == "reading" and a.expected and "```javascript" in a.expected)
                    
                    if is_example:
                        # Parse the worked example
                        import re
                        expected = a.expected
                        
                        # Extract title/explanation (before first code block)
                        code_match = re.search(r'```javascript\n(.*?)```', expected, re.DOTALL)
                        if code_match:
                            initial_code = code_match.group(1).strip()
                            # HTML escape the code for the textarea
                            initial_code_escaped = html.escape(initial_code)
                            # Get text before code block
                            before_code = expected[:code_match.start()].strip()
                            # Get text after code block (key takeaways)
                            after_code = expected[code_match.end():].strip()
                            
                            # Render explanation
                            example_explanation = ""
                            if before_code:
                                # Process with safe markdown (escapes HTML)
                                example_explanation = f'<div class="activity-expected"><h3>Example</h3><div class="expected-content">{safe_markdown(before_code)}</div></div>'
                            
                            # Render key takeaways
                            key_takeaways = ""
                            if after_code and ("Key Takeaways" in after_code or "takeaway" in after_code.lower()):
                                key_takeaways = f'<div class="activity-expected" style="margin-top:1.5rem;"><h3>Key Takeaways</h3><div class="expected-content">{safe_markdown(after_code)}</div></div>'
                            
                            activity_content = engine.render_with_defaults(
                                'partials/activity_example.html',
                                {
                                    'activity_id': a.id or f"act-{len(slides)}",
                                    'instructions': escape_html(a.instructions or ""),
                                    'est_html': est_html,
                                    'example_explanation': example_explanation,
                                    'initial_code': initial_code_escaped,
                                    'key_takeaways': key_takeaways
                                }
                            )
                        else:
                            # Fallback to regular reading
                            expected_html = f'<div class="activity-expected"><h3>Expected Output</h3><div class="expected-content">{safe_markdown(a.expected)}</div></div>'
                            activity_content = engine.render_with_defaults(
                                'partials/activity_reading.html',
                                {
                                    'activity_id': a.id or f"act-{len(slides)}",
                                    'instructions': escape_html(a.instructions or ""),
                                    'expected_html': expected_html,
                                    'est_html': est_html
                                }
                            )
                    else:
                        # Regular activity
                        expected_html = ""
                        if a.expected:
                            expected_html = f'<div class="activity-expected"><h3>Expected Output</h3><div class="expected-content">{safe_markdown(a.expected)}</div></div>'
                        
                        # Choose activity template based on type
                        activity_template = f'partials/activity_{a.type.lower()}.html'
                        
                        activity_content = engine.render_with_defaults(
                            activity_template,
                            {
                                'activity_id': a.id or f"act-{len(slides)}",
                                'activity_type': a.type.title(),
                                'instructions': escape_html(a.instructions or ""),
                                'expected_html': expected_html,
                                'est_html': est_html
                            }
                        )
                    
                    slide_num += 1
                    slide_html = engine.render_with_defaults(
                        'partials/slide.html',
                        {
                            'slide_type': 'activity',
                            'slide_id': f'activity-{a.id or f"act-{len(slides)}"}',
                            'slide_content': activity_content,
                            'slide_number': str(slide_num),
                            'total_slides': '1'  # Will update later
                        }
                    )
                    slides.append(slide_html)

            # Render assessment slides
            if l.assessments:
                for asmt in l.assessments:
                    q_html = []
                    for idx, q in enumerate(asmt.questions, start=1):
                        points = str(int(q.points)) if q.points == int(q.points) else str(q.points)
                        type_labels = {
                            "mcq": "Multiple Choice",
                            "msq": "Multiple Select",
                            "truefalse": "True/False",
                            "short": "Short Answer",
                            "long": "Long Answer",
                            "code": "Code",
                            "matching": "Matching",
                            "ordering": "Ordering"
                        }
                        type_label = type_labels.get(q.type, q.type.upper())
                        
                        if q.type in ("mcq", "msq"):
                            name = f"{asmt.id}__q{idx}"
                            stem = q.data.get("stem", "")
                            inputs = []
                            input_type = "radio" if q.type == "mcq" else "checkbox"
                            for j, ch in enumerate(q.data["choices"], start=1):
                                inputs.append(f"""<label data-option-number="{j}"><input type="{input_type}" name="{name}" value="{str(ch['correct']).lower()}" style="display:none;"> <span style="flex:1;">{escape_html(ch['text'])}</span></label>""")
                            # Join choices without <br> - CSS flexbox will handle spacing
                            choices_html = "\n".join(inputs)
                            question_html = engine.render_with_defaults(
                                'partials/question.html',
                                {
                                    'q_type': q.type,
                                    'q_index': str(idx),
                                    'q_points': points,
                                    'q_type_label': type_label,
                                    'stem': escape_html(stem),
                                    'choices': choices_html
                                }
                            )
                            q_html.append(question_html)
                        elif q.type == "truefalse":
                            name = f"{asmt.id}__q{idx}"
                            stmt = q.data["statement"]
                            ans = q.data["answer"]
                            choices_html = f"""<label data-option-number="1"><input type="radio" name="{name}" value="true" style="display:none;"> <span style="flex:1;">True</span></label>
<label data-option-number="2"><input type="radio" name="{name}" value="false" style="display:none;"> <span style="flex:1;">False</span></label>"""
                            question_html = engine.render_with_defaults(
                                'partials/question.html',
                                {
                                    'q_type': 'truefalse',
                                    'q_index': str(idx),
                                    'q_points': points,
                                    'q_type_label': type_label,
                                    'stem': escape_html(stmt),
                                    'choices': choices_html
                                }
                            )
                            # Add data-answer attribute
                            question_html = question_html.replace(
                                'data-type="truefalse"',
                                f'data-type="truefalse" data-answer="{ans}"'
                            )
                            q_html.append(question_html)
                        elif q.type in ("short", "long"):
                            name = f"{asmt.id}__q{idx}"
                            prompt = q.data.get("prompt", "")
                            solution = q.data.get("solution", "")
                            solution_attr = f' data-solution="{escape_html(solution)}"' if solution else ""
                            question_html = f"""<div class="q" data-type="{q.type}" data-question-id="{name}" data-points="{points}"{solution_attr}>
  <div class="question-meta">
    <span class="question-type-label">{type_label}</span>
    <span class="question-points-label">{points} pts</span>
  </div>
  <div class="stem">{escape_html(prompt)}</div>
  <div class="answer-input">
    <textarea class="text-answer" name="{name}" rows="{4 if q.type == 'short' else 8}" placeholder="Enter your answer here..."></textarea>
  </div>
  <div class="solution" style="display:none;">
    <strong>Solution:</strong> <div class="solution-content">{escape_html(solution)}</div>
  </div>
</div>"""
                            q_html.append(question_html)
                        elif q.type == "code":
                            name = f"{asmt.id}__q{idx}"
                            prompt = q.data.get("prompt", "")
                            lang = q.data.get("lang", "javascript")
                            starter = q.data.get("starter", "")
                            solution = q.data.get("solution", "")
                            solution_attr = f' data-solution="{escape_html(solution)}"' if solution else ""
                            question_html = f"""<div class="q q-code" data-type="code" data-question-id="{name}" data-lang="{escape_html(lang)}" data-points="{points}"{solution_attr}>
  <div class="question-meta">
    <span class="question-type-label">{type_label}</span>
    <span class="question-points-label">{points} pts</span>
  </div>
  <div class="stem">{escape_html(prompt)}</div>
  <div class="code-answer">
    <textarea class="code-editor" name="{name}" rows="10" placeholder="Write your code here...">{escape_html(starter)}</textarea>
  </div>
  <div class="solution" style="display:none;">
    <strong>Solution:</strong>
    <pre><code class="language-{escape_html(lang)}">{escape_html(solution)}</code></pre>
  </div>
</div>"""
                            q_html.append(question_html)
                        elif q.type == "matching":
                            name = f"{asmt.id}__q{idx}"
                            pairs = q.data.get("pairs", [])
                            # Get all right items and shuffle for dropdown options
                            import random
                            all_right_items = [p["right"] for p in pairs]
                            shuffled_rights = all_right_items.copy()
                            random.shuffle(shuffled_rights)
                            # Create matching interface
                            matching_html = '<div class="matching-pairs">'
                            for i, pair in enumerate(pairs):
                                left_text = escape_html(pair["left"])
                                correct_right = escape_html(pair["right"])
                                matching_html += f'''<div class="matching-pair">
      <div class="matching-left">{left_text}</div>
      <select class="matching-select" name="{name}__pair{i}" data-correct="{correct_right}">
        <option value="">-- Select --</option>
        {''.join([f'<option value="{escape_html(r)}">{escape_html(r)}</option>' for r in shuffled_rights])}
      </select>
    </div>'''
                            matching_html += '</div>'
                            question_html = f"""<div class="q q-matching" data-type="matching" data-question-id="{name}" data-points="{points}">
  <div class="question-meta">
    <span class="question-number-badge">{idx}</span>
    <span class="question-type-label">{type_label}</span>
    <span class="question-points-label">{points} pts</span>
  </div>
  <div class="stem">Match each item on the left with the correct item on the right.</div>
  {matching_html}
</div>"""
                            q_html.append(question_html)
                        elif q.type == "ordering":
                            name = f"{asmt.id}__q{idx}"
                            items = q.data.get("items", [])
                            # Create ordering interface with number inputs
                            ordering_html = '<div class="ordering-items">'
                            for i, item in enumerate(items):
                                item_text = escape_html(item)
                                ordering_html += f'''<div class="ordering-item">
      <label>Step <input type="number" class="ordering-input" name="{name}__item{i}" min="1" max="{len(items)}" data-correct="{i+1}" placeholder="{i+1}"></label>
      <span class="ordering-text">{item_text}</span>
    </div>'''
                            ordering_html += '</div>'
                            question_html = f"""<div class="q q-ordering" data-type="ordering" data-question-id="{name}" data-points="{points}">
  <div class="question-meta">
    <span class="question-number-badge">{idx}</span>
    <span class="question-type-label">{type_label}</span>
    <span class="question-points-label">{points} pts</span>
  </div>
  <div class="stem">Put the following items in the correct order (1, 2, 3, ...).</div>
  {ordering_html}
</div>"""
                            q_html.append(question_html)
                        else:
                            q_html.append(f"""<div class="q" data-type="{q.type}">
  <div>Unsupported question type: {q.type}</div>
</div>""")
                    
                    assessment_content = engine.render_with_defaults(
                        'partials/assessment_slide.html',
                        {
                            'assess_id': asmt.id,
                            'course_id': course.id,
                            'pass_score': str(asmt.passScore or 0),
                            'questions': ''.join(q_html)
                        }
                    )
                    
                    slide_num += 1
                    slide_html = engine.render_with_defaults(
                        'partials/slide.html',
                        {
                            'slide_type': 'assessment',
                            'slide_id': f'assessment-{asmt.id}',
                            'slide_content': assessment_content,
                            'slide_number': str(slide_num),
                            'total_slides': '1'  # Will update later
                        }
                    )
                    slides.append(slide_html)

            # Add completion slide
            completion_content = f"""<div class="card" style="text-align:center;padding:3rem 2rem;">
  <h2 style="margin-bottom:1rem;">🎉 Lesson Complete!</h2>
  <p style="font-size:1.125rem;margin-bottom:2rem;color:var(--text-secondary);">You've finished this lesson. Great work!</p>
  <button class="btn" onclick="markLessonComplete('{course.id}','{l.id or safe_filename(l.title)}')" style="font-size:1rem;padding:1rem 2rem;">✓ Mark Lesson Complete</button>
</div>"""
            
            slide_num += 1
            completion_slide = engine.render_with_defaults(
                'partials/slide.html',
                {
                    'slide_type': 'completion',
                    'slide_id': f'completion-{l.id or safe_filename(l.title)}',
                    'slide_content': completion_content,
                    'slide_number': str(slide_num),
                    'total_slides': str(slide_num)
                }
            )
            slides.append(completion_slide)

            # Update slide numbers and total in all slides
            total_slides = len(slides)
            updated_slides = []
            for idx, slide_html in enumerate(slides, start=1):
                # Replace placeholders that might have been left by template engine
                updated_slide = slide_html.replace('{{ slide_number }}', str(idx))
                updated_slide = updated_slide.replace('{{ total_slides }}', str(total_slides))
                # Fix slide counter text if it was rendered with placeholder
                import re
                updated_slide = re.sub(r'(\d+) / 1', rf'\1 / {total_slides}', updated_slide)
                updated_slides.append(updated_slide)

            # Render lesson header
            lesson_header_html = engine.render_with_defaults(
                'partials/lesson_header.html',
                {
                    'lesson_title': l.title,
                    'module_title': l.module_title
                }
            )
            
            header_html = engine.render_with_defaults(
                'partials/header.html',
                {'header_content': lesson_header_html}
            )
            
            # Render lesson template with slides
            lesson_html = engine.render_with_defaults(
                'lesson.html',
                {
                    'lesson_title': l.title,
                    'course_title': course.title,
                    'course_id': course.id,
                    'total_lessons': str(total_lessons),
                    'lesson_id': l.id or safe_filename(l.title),
                    'header_html': header_html,
                    'slides': '\n'.join(updated_slides)
                }
            )
            
            fname = os.path.join(outdir, f"{safe_filename(l.title)}.html")
            with open(fname, "w", encoding="utf-8") as f:
                f.write(lesson_html)

def build(tml_path: str, outdir: str, template_dir: str = None, validate: bool = True):
    """
    Build static site from TML file.
    
    Args:
        tml_path: Path to TML course file
        outdir: Output directory for generated HTML
        template_dir: Optional custom template directory
        validate: If True, validate TML against XSD schema before parsing
    """
    import sys
    try:
        course = parse_tml(tml_path, validate=validate)
        render_course(course, outdir, template_dir)
    except TMLParseError as e:
        print(f"Error parsing TML file: {e}", file=sys.stderr)
        sys.exit(1)
    except ET.ParseError as e:
        print(f"XML parsing error in {tml_path}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python tml_to_site.py path/to/course.tml out_dir/ [template_dir]")
        sys.exit(1)
    template_dir = sys.argv[3] if len(sys.argv) > 3 else None
    # Default to templates directory if it exists
    if template_dir is None:
        default_template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        if os.path.exists(default_template_dir):
            template_dir = default_template_dir
    build(sys.argv[1], sys.argv[2], template_dir)
