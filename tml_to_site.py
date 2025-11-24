#!/usr/bin/env python3
"""
TML v0.1 Parser & Static Site Generator (no external deps).

Usage:
  python tml_to_site.py path/to/course.tml out_dir/ [template_dir]
"""
import os, re
from xml.etree import ElementTree as ET
from template_engine import TemplateEngine

def safe_filename(name: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9_-]+", "-", name.strip().lower())
    name = re.sub(r"-+", "-", name).strip("-")
    return name or "lesson"

def mini_markdown(md: str) -> str:
    import re
    md = md.strip()
    md = re.sub(r"`([^`]+)`", r"<code>\1</code>", md)
    md = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", md)
    md = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", md)
    lines, out = [], []
    for line in md.splitlines():
        s = line.strip()
        if s.startswith("### "): lines.append(f"<h3>{s[4:]}</h3>")
        elif s.startswith("## "): lines.append(f"<h2>{s[3:]}</h2>")
        elif s.startswith("# "):  lines.append(f"<h1>{s[2:]}</h1>")
        elif s.startswith("- "):  lines.append(f"<li>{s[2:]}</li>")
        else:
            lines.append("" if s=="" else f"<p>{s}</p>")
    in_ul=False
    for l in lines:
        if l.startswith("<li>"):
            if not in_ul: out.append("<ul>"); in_ul=True
            out.append(l)
        else:
            if in_ul: out.append("</ul>"); in_ul=False
            out.append(l)
    if in_ul: out.append("</ul>")
    return "\n".join(out)


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

def parse_tml(path: str) -> TCourse:
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
        mtitle = m.attrib["title"]
        order = int(m.attrib.get("order","0") or "0")
        lessons=[]
        for l in m.findall("./lesson"):
            lid = l.attrib.get("id","")
            ltitle = l.attrib["title"]
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

    # Render lesson pages
    for m in course.modules:
        for l in m.lessons:
            # Process content
            content_parts = []
            for c in l.content:
                if c.format == "html":
                    content_parts.append(c.value)
                elif c.format == "markdown":
                    content_parts.append(mini_markdown(c.value))
                else:
                    content_parts.append(f"<pre>{c.value}</pre>")
            content_html = "\n".join(content_parts) if content_parts else "<p>No content.</p>"

            # Render activities
            activities_html = ""
            if l.activities:
                blocks = []
                for a in l.activities:
                    expected_html = f"<p><strong>Expected:</strong> {a.expected}</p>" if a.expected else ""
                    est_html = f"<p class='small'>Estimated: {a.est}</p>" if a.est else ""
                    activity_html = engine.render_with_defaults(
                        'partials/activity.html',
                        {
                            'activity_type': a.type.title(),
                            'instructions': a.instructions or "",
                            'expected_html': expected_html,
                            'est_html': est_html
                        }
                    )
                    blocks.append(activity_html)
                activities_html = "\n".join(blocks)

            # Render assessments
            assessments_html = ""
            if l.assessments:
                blocks = []
                for asmt in l.assessments:
                    q_html = []
                    for idx, q in enumerate(asmt.questions, start=1):
                        if q.type in ("mcq", "msq"):
                            name = f"{asmt.id}__q{idx}"
                            stem = q.data.get("stem", "")
                            inputs = []
                            input_type = "radio" if q.type == "mcq" else "checkbox"
                            for j, ch in enumerate(q.data["choices"], start=1):
                                inputs.append(f"""<label><input type="{input_type}" name="{name}" value="{str(ch['correct']).lower()}"> {ch['text']}</label>""")
                            choices_html = "<br>".join(inputs)
                            question_html = engine.render_with_defaults(
                                'partials/question.html',
                                {
                                    'q_type': q.type,
                                    'q_index': str(idx),
                                    'stem': stem,
                                    'choices': choices_html
                                }
                            )
                            q_html.append(question_html)
                        elif q.type == "truefalse":
                            name = f"{asmt.id}__q{idx}"
                            stmt = q.data["statement"]
                            ans = q.data["answer"]
                            choices_html = f"""<label><input type="radio" name="{name}" value="true"> True</label>
  <label><input type="radio" name="{name}" value="false"> False</label>"""
                            question_html = engine.render_with_defaults(
                                'partials/question.html',
                                {
                                    'q_type': 'truefalse',
                                    'q_index': str(idx),
                                    'stem': stmt,
                                    'choices': choices_html
                                }
                            )
                            # Add data-answer attribute
                            question_html = question_html.replace(
                                'data-type="truefalse"',
                                f'data-type="truefalse" data-answer="{ans}"'
                            )
                            q_html.append(question_html)
                        else:
                            q_html.append(f"""<div class="q" data-type="{q.type}">
  <div>Unsupported question type in demo exporter.</div>
</div>""")
                    
                    assessment_html = engine.render_with_defaults(
                        'partials/assessment.html',
                        {
                            'assess_id': asmt.id,
                            'course_id': course.id,
                            'pass_score': str(asmt.passScore or 0),
                            'questions': ''.join(q_html)
                        }
                    )
                    blocks.append(assessment_html)
                assessments_html = "\n".join(blocks)

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
            
            # Build lesson content
            lesson_content = f"""<div class="card">
    {content_html}
  </div>
  {activities_html}
  {assessments_html}
  <div class="card">
    <button class="btn" onclick="markLessonComplete('{course.id}','{l.id or safe_filename(l.title)}')">Mark Lesson Complete</button>
  </div>"""
            
            # Render base template for lesson
            lesson_html = engine.render_with_defaults(
                'base.html',
                {
                    'title': f"{l.title} — {course.title}",
                    'course_id': course.id,
                    'total_lessons': str(total_lessons),
                    'content': lesson_content,
                    'header_html': header_html
                }
            )
            
            fname = os.path.join(outdir, f"{safe_filename(l.title)}.html")
            with open(fname, "w", encoding="utf-8") as f:
                f.write(lesson_html)

def build(tml_path: str, outdir: str, template_dir: str = None):
    course = parse_tml(tml_path)
    render_course(course, outdir, template_dir)

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
