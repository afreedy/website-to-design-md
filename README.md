# Website to Design.md

An AI-agent skill that turns website URLs or saved HTML/HTM/MHTML pages into reusable, source-backed design specifications.

Give your agent a website you like. The skill guides it to open the page, capture its available HTML/MHTML and resources, inspect the actual styles, and write a `design.md` another agent can use to build a frontend.

## Use

```text
Use $website-to-design-md for https://example.com.
Save the design reference under design-references/example/.
```

Multiple sites:

```text
Use $website-to-design-md for these three websites:
[URLs]
Create a separate design.md for each website.
```

Saved pages:

```text
Use $website-to-design-md with /path/to/page.mhtml
and /path/to/page.html plus its resource folder.
```

Applying the result is a separate request:

```text
Use design-references/example/design.md to redesign this app.
Preserve its data, routes, and interactions.
```

## Install in Codex

Clone this repository into your skills folder:

```bash
git clone https://github.com/afreedy/website-to-design-md.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/website-to-design-md"
```

For an existing install, update that checkout instead of cloning over it. Start a new chat or reload skills as supported by your client. For other agents that support SKILL.md, install the folder using that agent's skill mechanism; browser/file APIs may differ.

## What the document contains

The template follows the breadth of Expo/Claude-style design references:

- Overview and defining visual characteristics
- Source evidence and capture coverage
- Colors and surface themes
- Font families and a precise typography hierarchy
- Spacing, grids, containers and whitespace
- Elevation, shapes and asset treatments
- Component recipes and interaction states
- Do's and don'ts
- Responsive behavior, touch targets and collapsing rules
- Iteration guidance and known gaps

Exact extracted facts, rendered observations, inferred design intent, and recommended adaptations are distinguished. Source values take precedence over assumptions in an example.

## Capture support

The agent uses its available browser tools. Chromium's `Page.captureSnapshot` can produce a real MHTML archive when the environment exposes it. Native browser complete-page save is another option. If archive export is unavailable, the skill reports the gap and uses the HTML/CSS/screenshots it can obtain.

The bundled Python 3.9+ helper unpacks an existing MHTML archive without network access or third-party packages:

```bash
python3 scripts/unpack_mhtml.py page.mhtml --out capture-unpacked
```

It writes a UTF-8 `index.html`, resources under safe generated filenames, and an `inventory.json` with original locations, MIME types, byte sizes and checksums. The output directory must be new. It does not rewrite resource URLs or promise an offline-working clone.

## Limits

This is a design extraction workflow, not a universal pixel-perfect cloning tool. Captures can miss fonts, hidden states, deferred media, authenticated views, or client-rendered content. The skill records those limits. It does not automatically modify an app or publish downloaded pages/assets.

The templates are generalized from user-supplied examples; those full example documents and downloaded third-party pages are not included. This repository's MIT license covers its own instructions and helper code, not third-party website content, trademarks or fonts.

## Checks

```bash
python3 -m unittest discover -s scripts -p 'test_*.py'
```

These tests cover MIME decoding, correct main-document selection, binary preservation, safe filenames, rejection of invalid archives, and preservation of an existing output directory. They do not prove every browser can capture every website.
