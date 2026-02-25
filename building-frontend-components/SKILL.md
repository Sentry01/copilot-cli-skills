---
name: building-frontend-components
description: "Builds accessible, production-ready frontend components. Use when building UI components, forms, modals, or any React/Vue/Svelte frontend work — before writing component code."
---

# Building Frontend Components

## Iron Law

**NO COMPONENT CODE WITHOUT PRE-IMPLEMENTATION CHECKLIST FIRST.**

Wrote JSX before checking for existing design system components? Delete it. Styled before planning keyboard interaction? Delete it. These aren't optional steps.

## Pre-Implementation Checklist

**Before writing ANY component code:**

1. **Check for existing design system** — tokens, components, patterns already in repo
2. **Document component requirements** — states (loading, error, empty), variants, accessibility needs
3. **Plan keyboard interaction** — focus order, shortcuts, trap requirements

Do NOT skip this for "simple" components. Simple components have accessibility bugs too.

**New project with no design system?** See `references/patterns.md` → "Design Thinking" for direction-setting.

**Framework selection guidance:** See `references/patterns.md` → "Framework Selection".

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

Modals MUST implement focus trap. See `references/patterns.md` → "Focus Trap Implementation" for copy-paste hook.

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

## Component State Checklist

Every component MUST handle:

- [ ] **Default** — Normal display state
- [ ] **Loading** — Skeleton or spinner (avoid for <500ms operations)
- [ ] **Empty** — Meaningful empty state, not blank
- [ ] **Error** — Actionable message with recovery path
- [ ] **Disabled** — Visual indication + `aria-disabled` or `disabled`
- [ ] **Focus** — Visible focus indicator (never `outline: none` without replacement)

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

## Common Mistakes from Baseline Testing

| What Agent Did | What Was Missing |
|----------------|------------------|
| Modal with Escape handling | No `role="dialog"`, no focus trap, no focus restoration |
| Form with labels | No `aria-invalid`, no `aria-describedby` for errors |
| Error message display | No `role="alert"` for screen reader announcement |
| Inline styles | No design tokens, creates maintenance burden |

## When NOT to Use This Skill

- Pure backend/API work with no UI
- Static content pages (use Astro or static HTML instead)
- Design system documentation (use the design system's own tooling)

## Additional References

For error handling, styling standards, performance, and testing → see `references/patterns.md`.

## Definition of Done

Before marking work complete:

- [ ] Pre-implementation checklist completed (design system check, requirements, keyboard plan)
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
