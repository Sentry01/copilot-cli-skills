# Frontend Patterns Reference

## Contents
- Design Thinking (new projects)
- Framework Selection
- Focus Trap Implementation
- Error Handling Patterns
- Styling Standards
- Performance Essentials
- Testing Expectations

## Design Thinking (New Projects Only)

⛔ **ONLY when ALL of these are true:** (1) no existing design system, (2) no existing components to match, (3) greenfield project. Otherwise: skip and match existing patterns.

### Priority Order
1. **Honor existing systems** — Respect established tokens, components, brand guidelines
2. **Define new direction** — Only when nothing exists, make deliberate choices

### For New Projects, Document:
- **Tone** — Pick ONE: brutalist, editorial monochrome, retro-futuristic, botanical, luxury minimal, playful toybox, etc.
- **Signature moment** — ONE memorable element: hero animation, kinetic typography, custom cursor, glassmorphism layer
- **Constraints** — Performance budget, accessibility targets, browser support

### Quick Aesthetic Checklist
| Element | Guidance |
|---------|----------|
| **Typography** | Pair distinctive display font + elegant body font. Avoid overused defaults (Inter, Roboto) unless required. |
| **Color** | Dominant hue + accent. Codify in CSS variables. Ensure WCAG AA+ contrast. |
| **Motion** | CSS for simple, Framer Motion/React Spring for complex. Always respect `prefers-reduced-motion`. |
| **Backgrounds** | Build depth: gradient meshes, noise textures, shadows. Avoid flat solid colors. |

**Commit design decisions to writing before implementation.**

## Framework Selection

| Framework | Use When |
|-----------|----------|
| **Next.js** | SSR/SSG needed, SEO important, API routes helpful |
| **React (Vite)** | Pure SPA, maximum flexibility needed |
| **Vue** | Existing Vue codebase, gradual migration |
| **Svelte** | Bundle size critical, minimal runtime needed |
| **Astro** | Content-heavy, partial hydration beneficial |

**Decision process:** Check repo conventions first → Evaluate requirements → Consider team expertise

## Focus Trap Implementation

Minimal focus trap for modals — copy and adapt:

```typescript
useEffect(() => {
  if (!isOpen) return;
  
  const dialog = dialogRef.current;
  const previousFocus = document.activeElement as HTMLElement;
  
  // Focus first interactive element
  const focusable = dialog?.querySelectorAll<HTMLElement>(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  focusable?.[0]?.focus();
  
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Escape') { onClose(); return; }
    if (e.key !== 'Tab' || !focusable?.length) return;
    
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    
    if (e.shiftKey && document.activeElement === first) {
      last.focus();
      e.preventDefault();
    } else if (!e.shiftKey && document.activeElement === last) {
      first.focus();
      e.preventDefault();
    }
  };
  
  document.addEventListener('keydown', handleKeyDown);
  return () => {
    document.removeEventListener('keydown', handleKeyDown);
    previousFocus?.focus(); // Restore focus
  };
}, [isOpen, onClose]);
```

## Error Handling Patterns

### Error Boundaries
- Wrap route-level components with error boundaries
- Provide recovery UI (retry button, help link)
- Log errors to monitoring service (Sentry, LogRocket)

### Network Failures
- Implement retry with exponential backoff for transient failures
- Show actionable messages ("Check your connection" not "Error 500")
- Provide offline fallbacks when appropriate

### Loading States
- Use skeleton screens for predictable layouts
- Avoid spinners for operations <500ms
- Show progress indicators for long operations (uploads, processing)

### Form Validation
- Use shared schemas (Zod, Yup) for validation logic
- Surface errors inline with `role="alert"`
- Preserve user input on error (never clear form fields)
- Disable submit button for invalid states

## Styling Standards

### Design Tokens
- Never introduce arbitrary values without justification
- Use CSS custom properties for colors, spacing, typography
- Prefer logical properties (`margin-inline`, `padding-block`)
- Use `clamp()` for fluid spacing/typography

### Semantic HTML
- Use native elements: `<button>`, `<nav>`, `<main>`, `<article>`
- Use ARIA only when native semantics are insufficient
- Implement roving tabindex for composite widgets (tabs, menus, grids)

### RTL & Internationalization
- Use logical properties for automatic RTL support
- Handle dynamic locale strings and date/number formatting
- Respect `prefers-color-scheme` and high-contrast modes

## Performance Essentials

### Bundle Size
- Track impact with Bundle Analyzer or size-limit
- Implement code splitting at route boundaries
- Memoize expensive computations with `useMemo`/`useCallback`

### Images & Assets
- Use WebP/AVIF with proper sizing
- Always include `width`/`height` to prevent layout shift
- Lazy load below-the-fold content

### Core Web Vitals
- **LCP** (Largest Contentful Paint): <2.5s
- **CLS** (Cumulative Layout Shift): <0.1
- **INP** (Interaction to Next Paint): <200ms

## Testing Expectations

### Unit & Component Tests
- Use React Testing Library + Jest/Vitest
- Verify keyboard flows and ARIA roles
- Test edge cases: empty, error, loading states
- Mock API calls and async operations

### Accessibility Testing
- Enable eslint-plugin-jsx-a11y
- Run axe-core or pa11y in CI
- Manual keyboard + screen reader verification

### Visual Regression
- Screenshot tests at multiple viewport sizes
- Test hover, focus, disabled states
- Compare light/dark themes if applicable
