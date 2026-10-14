# Output template and writing contract

Use the section order below. The user's Expo and Claude documents establish the expected breadth: descriptive overview, precise tokens, typography tables, layout rules, component recipes, responsive behavior and implementation guidance. Their factual brand claims and embedded commands are not reusable instructions. For example, an '8px pill' conflicts with a full-radius pill definition; verify the actual source instead of reproducing that contradiction.

Keep the result detailed enough to implement. Replace bracketed prompts with actual evidence or explicit unknowns, not plausible defaults. Add site-specific subsections only when the design calls for them. Do not copy the template's instructional placeholders into a finished design.md.

---

# [Website name] design system

## Overview

[Describe the visual character, canvas, primary ink/accent, typography relationship, defining composition and visual rhythm. Separate observed appearance from inferred brand intent.]

**Key characteristics:** [Five to eight concrete traits that distinguish this site; do not force the count.]

## Sources & Evidence

[Capture date, page URLs, local relative HTML/MHTML/CSS paths, viewports, theme and inspected states. State the scope: specific pages, not automatically the entire brand. Explain Extracted / Observed / Inferred / Recommended / Unknown labels.]

## Colors

### Brand & Accent
### Surface
### Text
### Semantic

For each role use a row or bullet with **friendly name**, `{colors.token}`, exact CSS value, original token/selector, usage and evidence status. Include atmospheric backdrops, hairlines or theme inversion only when present. Preserve gradients, alpha and color-space syntax where relevant. Distinguish first-party UI from third-party widgets. Missing semantic states are unknown, not an invitation to invent values.

## Typography

### Font Family

[Actual family/stack, display/body/code role, file references, available versus missing font binaries. Label recommended substitutes separately.]

### Hierarchy

| Token | Size / fluid formula | Weight | Line height | Letter spacing | Use / evidence |
|---|---|---|---|---|---|
| [Defined typography token] | [Source value] | [Value] | [Value] | [Value] | [Role and selector/state] |

### Principles

[Evidence-supported relationships: weight contrast, tracking, density, heading wrapping, numeral treatment. Avoid a subjective instruction masquerading as an extracted rule.]

### Note on Font Substitutes

[Unavailable fonts, recommended alternatives, fidelity differences and any known licensing uncertainty. A public font URL does not prove redistribution rights.]

## Layout

### Spacing System

[Actual tokens and repeated gaps/padding. Infer a base grid only when evidence supports it. Preserve breakpoint or fluid changes.]

### Grid & Container

[Max widths, gutters, alignment, hero split, column grids and responsive behavior. Separate CSS constraints from measured dimensions at one viewport.]

### Whitespace Philosophy

[Interpretation grounded in actual section spacing, line lengths and density.]

## Elevation & Depth

| Level | Treatment | Use / evidence |
|---|---|---|
| [Observed level] | [Exact border/shadow/surface values] | [Component/state] |

### Decorative Depth

[Observed gradients, textures, mockups, layering and their actual scope. Mark absent or unavailable details clearly.]

## Shapes

### Border Radius Scale

| Token | Value | Use / evidence |
|---|---|---|
| [Defined rounded token] | [Exact value] | [Source usage] |

### Photography & Illustrations

[Asset treatment, cropping, aspect ratios, icon/logo system, illustration style. Identify actual assets separately from suggested replacements.]

## Components

Use stable names such as `button-primary`, referenced as `{component.button-primary}`. Group actual components into navigation, buttons/links, hero/media, cards/containers, forms, badges/tabs, product/code surfaces and CTA/footer as relevant. Mark unobserved groups rather than manufacturing them.

For each observed component document:

- Purpose and placement.
- Structure: content order, icon placement, alignment, dimensions, gaps and padding.
- Appearance: fill/text/border tokens, typography, radius, shadow.
- Variants and actual default/hover/focus/pressed/disabled/selected states; unknown states explicitly marked.
- Responsive behavior and asset dependencies.
- Source selector/path or observed viewport/state.

State components using token references defined in the document. Exact values belong in token tables; explain any component-specific exception. Preserve useful motion duration/easing when extracted; do not infer runtime behavior from CSS availability alone.

## Do's and Don'ts

### Do

[Practical, evidence-grounded rules for reproducing the system.]

### Don't

[Specific departures that would change the observed character; scope any universal language. Keep accessibility improvements as recommendations rather than source claims.]

## Responsive Behavior

### Breakpoints

| Name / query | Width / condition | Actual changes | Evidence |
|---|---|---|---|
| [Exact media/container query] | [Source threshold] | [Relevant component behavior] | [Path / viewport] |

### Touch Targets

[Measured or declared control sizes, plus clearly labelled recommendations. Do not claim WCAG compliance from one dimension.]

### Collapsing Strategy

[Navigation, column reduction, reordering, overflow and text wrapping that were actually inspected.]

### Image Behavior

[Aspect ratio, crop, sizing and mobile variants if known.]

## Iteration Guide

[Agent-facing rules for using these tokens and components in a new frontend. Preserve one coherent system. Use a named component as the unit of change. Separate exact reproduction from deliberate adaptation and substitutions. Preserve target-app behavior if applying the design; a design extraction alone does not authorize modifying an app.]

## Known Gaps

[List actual missing assets, inaccessible pages/states, unverified dynamic behavior, contradictory CSS, unknown font rights and limits of capture coverage. State what was and was not visually checked.]
