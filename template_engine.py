#!/usr/bin/env python3
"""
Template Engine for TML Site Generator.
Supports templates, partials, and variable substitution.

All render methods (render, render_string, render_with_defaults) automatically
fall back to built-in default templates and partials when files are not found.
This ensures consistent behavior across the API.

To disable default fallbacks, use render(..., use_defaults=False) or
render_string(..., use_defaults=False).
"""
import os
import re
from typing import Dict, Optional


class TemplateEngine:
    """
    Simple template engine with partial support.
    
    All render methods automatically fall back to built-in defaults when
    templates or partials are not found in the filesystem. This provides
    a consistent API where defaults are always available.
    """
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize template engine.
        
        Args:
            template_dir: Directory containing templates. If None, uses built-in defaults.
        """
        self.template_dir = template_dir
        self._cache: Dict[str, str] = {}
        self._partial_cache: Dict[str, str] = {}
    
    def _load_template(self, name: str, use_defaults: bool = True) -> str:
        """
        Load a template from file or return default.
        
        Args:
            name: Template name
            use_defaults: If True, fall back to built-in defaults if file not found
        
        Returns:
            Template content or empty string
        """
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
        
        # Fall back to defaults if enabled
        if use_defaults:
            default = self.get_default_template(name)
            if default:
                self._cache[name] = default
                return default
        
        return ""
    
    def _load_partial(self, name: str, use_defaults: bool = True) -> str:
        """
        Load a partial template.
        
        Args:
            name: Partial name (with or without .html extension)
            use_defaults: If True, fall back to built-in defaults if file not found
        
        Returns:
            Partial content or empty string
        """
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
        
        # Fall back to defaults if enabled
        if use_defaults:
            # Default keys always have .html extension
            if name.endswith('.html'):
                default_key = f'partials/{name}'
            else:
                default_key = f'partials/{name}.html'
            
            default = self.get_default_template(default_key)
            if default:
                self._partial_cache[name] = default
                return default
        
        return ""
    
    def _render_partials(self, content: str, use_defaults: bool = True) -> str:
        """
        Replace {{> partial_name }} with partial content.
        
        Args:
            content: Template content with partial references
            use_defaults: If True, fall back to built-in defaults for missing partials
        """
        def replace_partial(match):
            partial_name = match.group(1).strip()
            partial_content = self._load_partial(partial_name, use_defaults=use_defaults)
            if partial_content:
                # Recursively render partials within partials
                return self._render_partials(partial_content, use_defaults=use_defaults)
            return f"<!-- Partial '{partial_name}' not found -->"
        
        pattern = r'\{\{>\s*([^\s}]+)\s*\}\}'
        return re.sub(pattern, replace_partial, content)
    
    def render(self, template_name: str, context: Dict[str, str], use_defaults: bool = True) -> str:
        """
        Render a template with the given context.
        
        This method automatically falls back to built-in default templates if the
        template file is not found. To disable this behavior, set use_defaults=False.
        
        Args:
            template_name: Name of the template file
            context: Dictionary of variables to substitute
            use_defaults: If True (default), fall back to built-in defaults for missing templates/partials
            
        Returns:
            Rendered template string, or HTML comment if template not found and use_defaults=False
        """
        template = self._load_template(template_name, use_defaults=use_defaults)
        
        if not template:
            return f"<!-- Template '{template_name}' not found -->"
        
        # Render partials first (with same default behavior)
        template = self._render_partials(template, use_defaults=use_defaults)
        
        # Replace variables: {{ variable_name }}
        def replace_var(match):
            var_name = match.group(1).strip()
            return context.get(var_name, f"{{{{ {var_name} }}}}")
        
        pattern = r'\{\{\s*([^\s}]+)\s*\}\}'
        result = re.sub(pattern, replace_var, template)
        
        return result
    
    def render_string(self, template_string: str, context: Dict[str, str], use_defaults: bool = True) -> str:
        """
        Render a template string directly (for inline templates).
        
        Partial references ({{> partial_name }}) in the template string will
        automatically fall back to built-in defaults if the partial file is not found.
        To disable this behavior, set use_defaults=False.
        
        Args:
            template_string: Template string with {{ variables }} and optionally {{> partials }}
            context: Dictionary of variables to substitute
            use_defaults: If True (default), fall back to built-in defaults for missing partials
            
        Returns:
            Rendered string
        """
        # Render partials first (with default fallback)
        template_string = self._render_partials(template_string, use_defaults=use_defaults)
        
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
        
        **Note:** This method is now equivalent to `render()` with `use_defaults=True`.
        It is kept for backward compatibility. All render methods now support
        default fallbacks by default.
        
        Args:
            template_name: Name of the template file
            context: Dictionary of variables to substitute
            
        Returns:
            Rendered template string
        """
        # Delegate to render() with defaults enabled
        return self.render(template_name, context, use_defaults=True)

