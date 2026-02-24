---
name: frontend-development
description: Use when building UI components, forms, modals, or any React/Vue/Svelte frontend work. Use before writing component code to ensure accessibility, focus management, and design system compliance.
---

# Frontend Development

## Overview

Production-ready frontend code requires **accessibility-first implementation**, not accessibility as afterthought. Every interactive component needs proper ARIA, focus management, and keyboard handling from the start.

## Pre-Implementation Checklist

**Before writing ANY component code:**

1. **Check for existing design system** - tokens, components, patterns
2. **Document component requirements** - states (loading, error, empty), variants, accessibility needs
3. **Plan keyboard interaction** - focus order, shortcuts, trap requirements

**Do NOT skip this for "simple" components.** Simple components have accessibility bugs too.

## Design Thinking (New Projects Only)

When no existing design system exists, establish direction **before** coding:

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

## Accessibility Essentials (Non-Negotiable)

### Modal/Dialog Components

```typescript
// REQUIRED attributes
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title-id"
  ref={dialogRef}
>
  <h2 id="modal-title-id">{title}</h2>
</div>

// REQUIRED behaviors
// 1. Focus first interactive element on open
// 2. Trap focus within modal (Tab cycles inside)
// 3. Restore focus to trigger element on close
// 4. Close on Escape key
```

### Form Components

```typescript
// REQUIRED: Link errors to fields
<input
  id="email"
  aria-invalid={errors.email ? 'true' : 'false'}
  aria-describedby={errors.email ? 'email-error' : undefined}
/>
{errors.email && (
  <span id="email-error" role="alert">
    {errors.email.message}
  </span>
)}

// REQUIRED: Form identification
<form aria-label="Login form">
  {/* or aria-labelledby pointing to a heading */}
</form>
```

### Interactive Elements

| Element | Requirements |
|---------|-------------|
| Button | Visible focus indicator, disabled state styling |
| Link | Underline or clear affordance, focus visible |
| Custom control | `role`, `aria-*` attributes, keyboard handler |
| Menu/Dropdown | `aria-expanded`, `aria-haspopup`, roving tabindex |

## Framework Selection Quick Reference

| Framework | Use When |
|-----------|----------|
| **Next.js** | SSR/SSG needed, SEO important, API routes helpful |
| **React (Vite)** | Pure SPA, maximum flexibility needed |
| **Vue** | Existing Vue codebase, gradual migration |
| **Svelte** | Bundle size critical, minimal runtime needed |
| **Astro** | Content-heavy, partial hydration beneficial |

**Decision process:** Check repo conventions first → Evaluate requirements → Consider team expertise

## Anti-Patterns (Stop If You See These)

### Generic AI Aesthetics
- ❌ Purple-on-white gradients with no context
- ❌ Cookie-cutter card layouts (centered hero + three icons)
- ❌ Flat solid backgrounds lacking atmosphere
- ✅ Honor existing design system OR establish distinctive direction

### Technical Debt
- ❌ Inline styles scattered throughout (use CSS modules, Tailwind, or tokens)
- ❌ Magic numbers instead of design tokens
- ❌ Hardcoded colors like `#2563eb` without token reference
- ✅ Use CSS custom properties or design tokens

### Accessibility Oversights
- ❌ Missing `role="dialog"` and `aria-modal` on modals
- ❌ No focus trap in modals/drawers
- ❌ Error messages without `role="alert"`
- ❌ Form fields without `aria-invalid` / `aria-describedby`
- ❌ Interactive elements without visible focus indicators

## Focus Trap Implementation

```typescript
// Minimal focus trap for modals
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

## Component State Checklist

Every component should handle:

- [ ] **Default** - Normal display state
- [ ] **Loading** - Skeleton or spinner (avoid for <500ms operations)
- [ ] **Empty** - Meaningful empty state, not blank
- [ ] **Error** - Actionable message with recovery path
- [ ] **Disabled** - Visual indication + `aria-disabled` or `disabled`
- [ ] **Focus** - Visible focus indicator (never `outline: none` without replacement)

## Common Mistakes from Baseline Testing

| What Agent Did | What Was Missing |
|----------------|------------------|
| Modal with Escape handling | No `role="dialog"`, no focus trap, no focus restoration |
| Form with labels | No `aria-invalid`, no `aria-describedby` for errors |
| Error message display | No `role="alert"` for screen reader announcement |
| Inline styles | No design tokens, creates maintenance burden |

**All of these must be addressed before shipping.**

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

## Definition of Done

Before marking work complete:

- [ ] All states implemented (default, loading, empty, error, disabled)
- [ ] Keyboard navigation works (Tab, Shift+Tab, Enter, Escape, arrows)
- [ ] Screen reader announces all interactive elements
- [ ] Color contrast meets WCAG AA (4.5:1 text, 3:1 UI)
- [ ] Responsive at 360px, 768px, 1280px
- [ ] Works with 200% browser zoom
- [ ] `prefers-reduced-motion` respected
- [ ] Error boundaries catch render failures
- [ ] No `any` types, console logs, or TODOs remain
- [ ] Tests pass (unit, a11y, visual if applicable)
