# Assessment UI Redesign Brief
## Senior UI/UX Design Recommendations for EdTech Assessment Interface

---

## 1. Visual Hierarchy & Spacing

### Current Issues
- Assessment header and questions exist within the same container, creating visual density
- Insufficient breathing room between assessment metadata and question content
- Typography scale doesn't clearly differentiate hierarchy levels

### Actionable Design Changes

#### 1.1 Container Separation
**Implementation:**
- Remove the single `assessment-container` wrapper
- Create distinct visual zones:
  - **Header Zone**: Elevated card with gradient background, separated by 4rem margin
  - **Question Zone**: Individual question cards with 3rem spacing between them
  - **Action Zone**: Fixed bottom action bar (sticky on scroll)

**CSS Changes:**
```css
.assessment-header-zone {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
  padding: 2.5rem 3rem;
  border-radius: 20px;
  margin-bottom: 4rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border);
}

.quiz-content {
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 3rem; /* Increased from 4rem margin on .q */
}
```

#### 1.2 Typographic Scale
**Implementation:**
- **Assessment Title**: 2.5rem (40px), weight 700, letter-spacing -0.75px
- **Question Stem**: 1.625rem (26px), weight 600, line-height 1.4
- **Question Instructions**: 1rem (16px), weight 400, color var(--text-secondary)
- **Option Text**: 1.0625rem (17px), weight 500, line-height 1.6
- **Input Text**: 0.9375rem (15px), weight 400

**CSS Changes:**
```css
.assessment-header h2 {
  font-size: 2.5rem;
  font-weight: 700;
  letter-spacing: -0.75px;
  line-height: 1.2;
}

.quiz .q .stem {
  font-size: 1.625rem;
  font-weight: 600;
  line-height: 1.4;
  margin-bottom: 2rem;
}

.quiz .q .question-instructions {
  font-size: 1rem;
  font-weight: 400;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  line-height: 1.6;
}
```

#### 1.3 Whitespace Strategy
**Implementation:**
- Assessment header: 4rem bottom margin
- Between questions: 3rem gap
- Question internal padding: 2.5rem (maintain)
- Option spacing: 1.25rem gap (increase from 1rem)

---

## 2. Interaction Design by Question Type

### 2.1 Multiple Choice: Selectable Card Design

#### Current Issues
- Standard radio buttons are small click targets
- Limited visual feedback on interaction
- Options don't feel "selectable" until clicked

#### Redesign Specifications

**Card Structure:**
- Each option is a full-width card (min-height: 4.5rem)
- Left side: Content area with option text
- Right side: Selection indicator (checkmark icon when selected)
- Number badge: Top-right corner, 2.75rem × 2.75rem

**Interaction States:**

1. **Default State:**
   - Background: `var(--bg-secondary)`
   - Border: 2px solid `var(--border)`
   - Number badge: `var(--bg-tertiary)` background
   - Shadow: None

2. **Hover State:**
   - Background: `var(--bg-tertiary)`
   - Border: 2px solid `var(--accent)` (50% opacity)
   - Transform: `translateY(-3px)`
   - Shadow: `0 6px 20px rgba(37, 99, 235, 0.15)`
   - Number badge: Accent color background
   - Cursor: pointer

3. **Selected State:**
   - Background: Linear gradient `135deg, rgba(37, 99, 235, 0.15) 0%, rgba(37, 99, 235, 0.05) 100%`
   - Border: 3px solid `var(--accent)`
   - Transform: `translateY(-2px)`
   - Shadow: `0 8px 24px rgba(37, 99, 235, 0.25)`
   - Number badge: Accent color with white checkmark icon
   - Checkmark icon: Visible on right side (SVG, 24px × 24px)

**Implementation:**
```css
.quiz .q .choice-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 4.5rem;
  padding: 1.5rem 2rem;
  border-radius: 14px;
  border: 2px solid var(--border);
  background: var(--bg-secondary);
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.quiz .q .choice-card:hover {
  background: var(--bg-tertiary);
  border-color: rgba(37, 99, 235, 0.5);
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.15);
}

.quiz .q .choice-card.selected {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.15) 0%, rgba(37, 99, 235, 0.05) 100%);
  border: 3px solid var(--accent);
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.25);
}

.quiz .q .choice-card .checkmark {
  display: none;
  width: 24px;
  height: 24px;
  color: var(--accent);
}

.quiz .q .choice-card.selected .checkmark {
  display: block;
}
```

### 2.2 Code Input: Monaco/CodeMirror Integration

#### Current Issues
- Plain textarea insufficient for code editing
- No syntax highlighting
- No line numbers
- Poor code editing experience

#### Redesign Specifications

**Component Requirements:**
- Integrate Monaco Editor (VS Code's editor) or CodeMirror 6
- Minimum height: 300px, expandable to 600px
- Features:
  - Line numbers (left gutter)
  - Syntax highlighting (language-specific)
  - Auto-indentation
  - Bracket matching
  - Code folding
  - Find/replace (optional)

**Container Design:**
- Dark theme matching assessment UI
- Border: 2px solid `var(--border)`
- Border-radius: 12px
- Background: `var(--bg-primary)`
- Header bar: Language indicator + line/column counter

**Implementation Approach:**
```html
<div class="code-question-editor">
  <div class="editor-header">
    <span class="language-badge">Python</span>
    <span class="editor-stats">Line 1, Col 1</span>
  </div>
  <div id="code-editor-{{ question_id }}" class="monaco-container"></div>
</div>
```

**JavaScript Integration:**
```javascript
// Load Monaco Editor
import * as monaco from 'monaco-editor';

function initCodeEditor(containerId, language, starterCode) {
  return monaco.editor.create(document.getElementById(containerId), {
    value: starterCode,
    language: language,
    theme: 'vs-dark',
    fontSize: 14,
    lineNumbers: 'on',
    minimap: { enabled: false },
    scrollBeyondLastLine: false,
    automaticLayout: true,
    tabSize: 2,
    wordWrap: 'on'
  });
}
```

**Styling:**
```css
.code-question-editor {
  margin-top: 2rem;
  border: 2px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  background: var(--bg-primary);
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
}

.monaco-container {
  min-height: 300px;
  max-height: 600px;
}
```

### 2.3 Ordering/Matching: Drag-and-Drop Interface

#### Current Issues
- Static number inputs for ordering
- Dropdown selects for matching
- No visual feedback during interaction
- Poor mobile experience

#### Redesign Specifications

**Ordering Questions - Drag & Drop:**

**Visual Design:**
- Each item is a draggable card (similar to choice cards)
- Drag handle icon on left (6-dot grip icon)
- Item content in center
- Drop zone indicators between items
- Visual feedback during drag (opacity: 0.5, scale: 1.05)

**Interaction Flow:**
1. User clicks and holds drag handle
2. Card becomes draggable (cursor: grabbing)
3. Drop zones appear between items (highlighted line)
4. On drop, item animates to new position
5. Order numbers update automatically

**Implementation:**
```css
.ordering-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  background: var(--bg-secondary);
  border: 2px solid var(--border);
  border-radius: 12px;
  cursor: grab;
  transition: all 0.2s ease;
  margin-bottom: 0.75rem;
}

.ordering-item.dragging {
  opacity: 0.5;
  transform: scale(1.05);
  cursor: grabbing;
}

.drag-handle {
  width: 24px;
  height: 24px;
  color: var(--text-muted);
  cursor: grab;
}

.drop-zone {
  height: 4px;
  background: var(--accent);
  border-radius: 2px;
  margin: 0.5rem 0;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.drop-zone.active {
  opacity: 1;
}
```

**Matching Questions - Drag & Drop:**

**Visual Design:**
- Two-column layout: Left (terms) and Right (definitions)
- Left items: Draggable cards
- Right items: Drop zones with placeholder text
- Visual connection line when matched (optional)
- Match indicator badge when correct

**Interaction Flow:**
1. User drags left item to right drop zone
2. Drop zone highlights on hover
3. On drop, item snaps into place
4. Match is visually confirmed
5. Both items become non-draggable (locked state)

**Implementation:**
```css
.matching-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

.matching-left-item {
  padding: 1.25rem 1.5rem;
  background: var(--bg-secondary);
  border: 2px solid var(--border);
  border-radius: 12px;
  cursor: grab;
}

.matching-right-zone {
  padding: 1.25rem 1.5rem;
  background: var(--bg-primary);
  border: 2px dashed var(--border);
  border-radius: 12px;
  min-height: 3.5rem;
  transition: all 0.2s ease;
}

.matching-right-zone.drag-over {
  background: rgba(37, 99, 235, 0.1);
  border-color: var(--accent);
  border-style: solid;
}
```

**JavaScript Library Recommendation:**
- Use **SortableJS** (lightweight, touch-friendly)
- Alternative: **react-beautiful-dnd** (if using React)
- Fallback: Native HTML5 Drag & Drop API

---

## 3. Progress & Navigation

### 3.1 Stepped Progress Tracker

#### Current Issues
- Generic progress bar shows "0%" regardless of question position
- No visual connection between current question and overall progress
- Progress bar doesn't reflect question-by-question completion

#### Redesign Specifications

**Visual Design:**
- Horizontal step indicator above assessment header
- Each question = one step
- Steps connected by progress line
- Current step: Highlighted with accent color
- Completed steps: Filled with accent color
- Future steps: Outlined/grayed

**Step Indicator Design:**
- Circle: 2.5rem diameter
- Active: Accent background, white number, pulsing animation
- Completed: Accent background, white checkmark
- Pending: Gray outline, gray number

**Implementation:**
```html
<div class="assessment-progress-tracker">
  <div class="progress-steps">
    <div class="step completed">
      <span class="step-number">1</span>
      <span class="step-checkmark">✓</span>
    </div>
    <div class="step-connector completed"></div>
    <div class="step completed">
      <span class="step-number">2</span>
      <span class="step-checkmark">✓</span>
    </div>
    <div class="step-connector completed"></div>
    <div class="step active">
      <span class="step-number">3</span>
    </div>
    <div class="step-connector"></div>
    <div class="step">
      <span class="step-number">4</span>
    </div>
    <!-- ... more steps ... -->
  </div>
  <div class="progress-text">
    Question <strong>3</strong> of <strong>8</strong>
  </div>
</div>
```

**CSS:**
```css
.assessment-progress-tracker {
  margin-bottom: 3rem;
  padding: 1.5rem 0;
}

.progress-steps {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.step {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  position: relative;
  transition: all 0.3s ease;
}

.step.completed {
  background: var(--accent);
  color: white;
  border: 2px solid var(--accent);
}

.step.active {
  background: var(--accent);
  color: white;
  border: 3px solid var(--accent);
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.2);
  animation: pulse 2s infinite;
}

.step:not(.completed):not(.active) {
  background: transparent;
  border: 2px solid var(--border);
  color: var(--text-muted);
}

.step-connector {
  flex: 1;
  height: 3px;
  background: var(--border);
  max-width: 4rem;
  transition: background 0.3s ease;
}

.step-connector.completed {
  background: var(--accent);
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.2); }
  50% { box-shadow: 0 0 0 8px rgba(37, 99, 235, 0.1); }
}

.progress-text {
  text-align: center;
  font-size: 0.9375rem;
  color: var(--text-secondary);
}
```

### 3.2 Enhanced Navigation

#### Current Issues
- Previous/Next buttons are small and secondary
- Navigation is at bottom, requires scrolling
- No keyboard shortcuts indication

#### Redesign Specifications

**Navigation Bar Design:**
- Fixed bottom navigation bar (sticky on scroll)
- Large, prominent buttons (min-height: 3.5rem)
- Left: Previous button (disabled on first question)
- Center: Question counter + keyboard hint
- Right: Next button (primary style)

**Button Styles:**
- Previous: Secondary style, outlined
- Next: Primary style, filled with accent color
- Disabled state: Reduced opacity, no pointer events

**Keyboard Shortcuts:**
- Display hint: "← → Arrow keys to navigate"
- Implement: ArrowLeft, ArrowRight, Enter (submit)

**Implementation:**
```html
<div class="assessment-navigation">
  <button class="btn-nav btn-nav-prev" onclick="previousQuestion()" disabled>
    <svg>...</svg>
    Previous
  </button>
  <div class="nav-info">
    <span class="question-counter">Question 3 of 8</span>
    <span class="keyboard-hint">← → Arrow keys</span>
  </div>
  <button class="btn-nav btn-nav-next btn-primary" onclick="nextQuestion()">
    Next
    <svg>...</svg>
  </button>
</div>
```

**CSS:**
```css
.assessment-navigation {
  position: sticky;
  bottom: 0;
  background: var(--bg-secondary);
  border-top: 2px solid var(--border);
  padding: 1.25rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.3);
  z-index: 100;
}

.btn-nav {
  min-width: 140px;
  min-height: 3.5rem;
  padding: 1rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.btn-nav:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.nav-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.keyboard-hint {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
```

---

## 4. Aesthetic Polish (Dark Mode)

### 4.1 Refined Color Palette

#### Current Issues
- Flat dark blue background lacks depth
- No visual separation between content zones
- Limited use of gradients or elevation

#### Redesign Specifications

**Color System:**
```css
:root {
  /* Base Colors */
  --bg-primary: #0a0e1a;        /* Deepest background */
  --bg-secondary: #141b2d;      /* Card backgrounds */
  --bg-tertiary: #1e2742;      /* Elevated surfaces */
  --bg-elevated: #252f47;       /* Hover states */
  
  /* Accent Colors */
  --accent: #3b82f6;            /* Primary blue */
  --accent-hover: #2563eb;      /* Darker blue */
  --accent-light: rgba(59, 130, 246, 0.1);
  --accent-medium: rgba(59, 130, 246, 0.2);
  
  /* Border & Divider */
  --border: #1e2742;
  --border-light: #252f47;
  --border-accent: rgba(59, 130, 246, 0.3);
  
  /* Text Colors */
  --text-primary: #f1f5f9;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
  --text-disabled: #64748b;
  
  /* Status Colors */
  --success: #10b981;
  --warning: #f59e0b;
  --error: #ef4444;
  
  /* Shadows */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.4);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.5);
  --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.6);
  --shadow-accent: 0 4px 20px rgba(59, 130, 246, 0.3);
}
```

**Gradient Applications:**
- Assessment header: `linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%)`
- Selected options: `linear-gradient(135deg, var(--accent-light) 0%, var(--accent-medium) 100%)`
- Progress tracker: Subtle gradient on active step

### 4.2 Background Separation

**Zone-Based Backgrounds:**
- **Header Zone**: `var(--bg-tertiary)` with subtle gradient
- **Question Zone**: `var(--bg-primary)` (deepest, creates contrast)
- **Navigation Zone**: `var(--bg-secondary)` with border-top

**Elevation System:**
- Use box-shadows to create depth hierarchy
- Cards: `var(--shadow-md)`
- Hover states: `var(--shadow-lg)`
- Active/Selected: `var(--shadow-accent)`

### 4.3 Visual Refinements

**Border Radius Scale:**
- Small elements: 8px
- Cards: 14px
- Containers: 20px
- Buttons: 12px

**Spacing Scale:**
- xs: 0.5rem (8px)
- sm: 1rem (16px)
- md: 1.5rem (24px)
- lg: 2rem (32px)
- xl: 3rem (48px)
- xxl: 4rem (64px)

**Transitions:**
- Standard: `0.2s ease`
- Interactive: `0.25s cubic-bezier(0.4, 0, 0.2, 1)`
- Complex: `0.3s ease`

---

## Implementation Priority

### Phase 1: Foundation (Week 1)
1. Typographic scale implementation
2. Color palette refinement
3. Spacing system standardization
4. Basic card redesign for multiple choice

### Phase 2: Interactions (Week 2)
1. Selectable card interactions (hover/active states)
2. Progress tracker implementation
3. Enhanced navigation bar
4. Keyboard shortcuts

### Phase 3: Advanced Features (Week 3)
1. Monaco Editor integration for code questions
2. Drag-and-drop for ordering questions
3. Drag-and-drop for matching questions
4. Animation polish

### Phase 4: Polish & Testing (Week 4)
1. Accessibility audit (WCAG 2.1 AA)
2. Mobile responsiveness testing
3. Performance optimization
4. User testing and iteration

---

## Accessibility Considerations

- **Keyboard Navigation**: All interactions must be keyboard accessible
- **Screen Readers**: Proper ARIA labels for drag-and-drop, progress tracker
- **Color Contrast**: Minimum 4.5:1 for text, 3:1 for UI components
- **Focus Indicators**: Clear focus states for all interactive elements
- **Touch Targets**: Minimum 44×44px for mobile interactions

---

## Success Metrics

- **Task Completion Rate**: >95% users complete assessment without confusion
- **Time to Complete**: Reduce average completion time by 15%
- **Error Rate**: <5% accidental selections or navigation errors
- **User Satisfaction**: >4.5/5 rating on assessment experience
- **Accessibility Score**: 100% WCAG 2.1 AA compliance

---

*This redesign brief provides actionable, implementable design specifications that can be directly translated into code. Each recommendation includes specific measurements, color values, and interaction patterns.*

