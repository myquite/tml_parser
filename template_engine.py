#!/usr/bin/env python3
"""
Template Engine for TML Site Generator.
Supports templates, partials, and variable substitution.
"""
import os
import re
from typing import Dict, Optional


class TemplateEngine:
    """Simple template engine with partial support."""
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize template engine.
        
        Args:
            template_dir: Directory containing templates. If None, uses built-in defaults.
        """
        self.template_dir = template_dir
        self._cache: Dict[str, str] = {}
        self._partial_cache: Dict[str, str] = {}
    
    def _load_template(self, name: str) -> str:
        """Load a template from file or return default."""
        if name in self._cache:
            return self._cache[name]
        
        # Try to load from template directory
        if self.template_dir and os.path.exists(self.template_dir):
            template_path = os.path.join(self.template_dir, name)
            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self._cache[name] = content
                    return content
        
        # Return empty string if not found (caller should handle defaults)
        return ""
    
    def _load_partial(self, name: str) -> str:
        """Load a partial template."""
        if name in self._partial_cache:
            return self._partial_cache[name]
        
        # Try to load from partials subdirectory
        if self.template_dir and os.path.exists(self.template_dir):
            # Support both 'styles' and 'partials/styles.html'
            if not name.endswith('.html'):
                partial_path = os.path.join(self.template_dir, 'partials', f"{name}.html")
            else:
                partial_path = os.path.join(self.template_dir, 'partials', name)
            
            if os.path.exists(partial_path):
                with open(partial_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self._partial_cache[name] = content
                    return content
        
        return ""
    
    def _render_partials(self, content: str) -> str:
        """Replace {{> partial_name }} with partial content."""
        def replace_partial(match):
            partial_name = match.group(1).strip()
            partial_content = self._load_partial(partial_name)
            if partial_content:
                # Recursively render partials within partials
                return self._render_partials(partial_content)
            return f"<!-- Partial '{partial_name}' not found -->"
        
        pattern = r'\{\{>\s*([^\s}]+)\s*\}\}'
        return re.sub(pattern, replace_partial, content)
    
    def render(self, template_name: str, context: Dict[str, str]) -> str:
        """
        Render a template with the given context.
        
        Args:
            template_name: Name of the template file
            context: Dictionary of variables to substitute
            
        Returns:
            Rendered template string
        """
        template = self._load_template(template_name)
        
        # Render partials first
        template = self._render_partials(template)
        
        # Replace variables: {{ variable_name }}
        def replace_var(match):
            var_name = match.group(1).strip()
            return context.get(var_name, f"{{{{ {var_name} }}}}")
        
        pattern = r'\{\{\s*([^\s}]+)\s*\}\}'
        result = re.sub(pattern, replace_var, template)
        
        return result
    
    def render_string(self, template_string: str, context: Dict[str, str]) -> str:
        """
        Render a template string directly (for inline templates).
        
        Args:
            template_string: Template string with {{ variables }}
            context: Dictionary of variables to substitute
            
        Returns:
            Rendered string
        """
        # Render partials first
        template_string = self._render_partials(template_string)
        
        # Replace variables
        def replace_var(match):
            var_name = match.group(1).strip()
            return context.get(var_name, f"{{{{ {var_name} }}}}")
        
        pattern = r'\{\{\s*([^\s}]+)\s*\}\}'
        result = re.sub(pattern, replace_var, template_string)
        
        return result
    
    def get_default_template(self, name: str) -> str:
        """Get a built-in default template."""
        defaults = {
            'base.html': """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{{ title }}</title>
  {{> styles }}
</head>
<body data-course-id="{{ course_id }}" data-total-lessons="{{ total_lessons }}">
  {{> header }}
  <main>
    <div class="container">
      {{ content }}
    </div>
  </main>
  {{> footer }}
  {{> scripts }}
</body>
</html>""",
            'index.html': """{{> base }}
""",
            'lesson.html': """{{> base }}
""",
            'partials/header.html': """<header>
  <div class="container">
    {{ header_content }}
  </div>
</header>""",
            'partials/footer.html': """<footer>
  <div class="container">
    <div class="small">Generated by TML Parser v0.1</div>
  </div>
</footer>""",
            'partials/styles.html': """<style>
:root{--accent:#1f6feb;}
*{box-sizing:border-box}
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Arial,sans-serif;line-height:1.6;margin:0;padding:0;background:#0e1116;color:#c9d1d9}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
header,footer{background:#0b0e14;padding:1rem 1.25rem;border-bottom:1px solid #161b22}
.container{max-width:980px;margin:0 auto;padding:1.25rem}
.card{background:#0b0e14;border:1px solid #161b22;border-radius:12px;padding:1rem;margin:1rem 0}
.btn{display:inline-block;padding:.5rem .9rem;border:1px solid #30363d;border-radius:8px;background:#161b22;color:#c9d1d9;cursor:pointer}
.btn:hover{background:#1b2330}
.progress{width:100%;height:10px;background:#161b22;border-radius:999px;overflow:hidden;border:1px solid #30363d}
.progress > span{display:block;height:100%;background:var(--accent);width:0%}
.badge{display:inline-block;background:#161b22;border:1px solid #30363d;padding:.2rem .5rem;border-radius:999px;margin-right:.25rem}
.quiz{margin-top:1rem}
.quiz .q{margin:.5rem 0;padding:.75rem;border:1px dashed #30363d;border-radius:8px}
code{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:.1rem .3rem}
ul{margin:.25rem 0 .75rem .9rem}
h1,h2,h3{color:#e6edf3}
.small{font-size:.9rem;color:#8b949e}
footer{border-top:1px solid #161b22;border-bottom:0;margin-top:2rem}
kbd{border:1px solid #30363d;border-bottom-width:2px;padding:.1rem .25rem;border-radius:4px;background:#0b0e14}
</style>""",
            'partials/scripts.html': """<script>
const storeKey = (courseId) => `tml-progress::${courseId}`;
function getProgress(courseId){
  const raw = localStorage.getItem(storeKey(courseId));
  return raw ? JSON.parse(raw) : {completedLessons: {}, scores: {}};
}
function setProgress(courseId, data){
  localStorage.setItem(storeKey(courseId), JSON.stringify(data));
}
function markLessonComplete(courseId, lessonId){
  const p = getProgress(courseId);
  p.completedLessons[lessonId] = true;
  setProgress(courseId, p);
  updateProgressBar(courseId);
}
function saveScore(courseId, assessId, score){
  const p = getProgress(courseId);
  p.scores[assessId] = Math.max(p.scores[assessId]||0, score);
  setProgress(courseId, p);
  updateProgressBar(courseId);
}
function updateProgressBar(courseId){
  const p = getProgress(courseId);
  const total = parseInt(document.body.dataset.totalLessons || "0");
  const done = Object.keys(p.completedLessons).length;
  const pct = total>0 ? Math.round((done/total)*100) : 0;
  const el = document.querySelector('.progress > span');
  if(el){ el.style.width = pct + '%'; }
  const label = document.getElementById('progress-label');
  if(label){ label.textContent = pct + '% complete'; }
}
function checkQuiz(courseId, assessId){
  const assessEl = document.querySelector(`[data-assessment='${assessId}']`);
  let total=0, correct=0;
  assessEl.querySelectorAll('.q').forEach((q)=>{
    total++;
    const type = q.dataset.type;
    if(type==='mcq'){
      const chosen = q.querySelector('input[type=radio]:checked');
      if(!chosen) return;
      if(chosen.value === 'true') correct++;
    }else if(type==='msq'){
      let ok=true, any=false;
      q.querySelectorAll('input[type=checkbox]').forEach(cb=>{
        any = any || cb.checked;
        if((cb.value==='true') !== cb.checked){ ok=false; }
      });
      if(any && ok) correct++;
    }else if(type==='truefalse'){
      const chosen = q.querySelector('input[type=radio]:checked');
      if(chosen && chosen.value === q.dataset.answer) correct++;
    }
  });
  const score = Math.round((correct/Math.max(total,1))*100);
  saveScore(courseId, assessId, score);
  const out = assessEl.querySelector('.quiz-result');
  if(out){ out.textContent = `Score: ${score}% (${correct}/${Math.max(total,1)})`; }
}
document.addEventListener('DOMContentLoaded', ()=>{
  const cid = document.body.dataset.courseId;
  updateProgressBar(cid);
});
</script>""",
        }
        return defaults.get(name, "")
    
    def render_with_defaults(self, template_name: str, context: Dict[str, str]) -> str:
        """
        Render template, falling back to defaults if file not found.
        
        Args:
            template_name: Name of the template file
            context: Dictionary of variables to substitute
            
        Returns:
            Rendered template string
        """
        template = self._load_template(template_name)
        
        # If template not found, try to get default
        if not template:
            template = self.get_default_template(template_name)
        
        if not template:
            return f"<!-- Template '{template_name}' not found -->"
        
        # For partials, also check defaults
        def load_partial_with_default(name):
            # Try loading from file first
            content = self._load_partial(name)
            if not content:
                # Try with .html extension
                if not name.endswith('.html'):
                    content = self._load_partial(f"{name}.html")
            if not content:
                # Fall back to defaults
                default_key = f'partials/{name}' if not name.endswith('.html') else f'partials/{name}'
                content = self.get_default_template(default_key)
            return content
        
        # Replace partials: {{> partial_name }}
        def replace_partial(match):
            partial_name = match.group(1).strip()
            partial_content = load_partial_with_default(partial_name)
            if partial_content:
                # Render partial with same context (for nested variables)
                return self._render_partials(partial_content)
            return f"<!-- Partial '{partial_name}' not found -->"
        
        # First pass: render partials recursively
        max_iterations = 10  # Prevent infinite loops
        for _ in range(max_iterations):
            pattern = r'\{\{>\s*([^\s}]+)\s*\}\}'
            new_template = re.sub(pattern, replace_partial, template)
            if new_template == template:
                break
            template = new_template
        
        # Replace variables: {{ variable_name }}
        def replace_var(match):
            var_name = match.group(1).strip()
            value = context.get(var_name, "")
            # If value is empty and it's a partial placeholder, leave it
            if not value and var_name.startswith('>'):
                return match.group(0)
            return value if value else f"{{{{ {var_name} }}}}"
        
        pattern = r'\{\{\s*([^\s}]+)\s*\}\}'
        result = re.sub(pattern, replace_var, template)
        
        return result

