# Browser capture

The goal is a real page archive with its styles, not a text-only web fetch. Read the browser tool's current documentation before using optional APIs. Prefer available supported browser controls over inventing a new automation stack.

## With Chromium CDP available

1. Open the supplied URL and inspect the rendered page. Capture after relevant content loads. Briefly scroll to load visible-page assets if needed. A successful navigation alone does not prove content loaded.
2. Use the tab's documented CDP capability with `Page.captureSnapshot` and `{ "format": "mhtml" }` where supported. The protocol's response contains a `data` string holding the MIME archive. Save the exact bytes/string as `capture/page.mhtml`; do not dump its full content into chat.
3. Use `scripts/unpack_mhtml.py` to produce `unpacked/index.html` and resources from the same snapshot. This gives an HTML document plus source files; it is not the browser's native "Webpage, Complete" export.
4. If supported, also save the live document's `document.documentElement.outerHTML` as `page.html`, preceded by its doctype, or use the browser's native complete-page save. Preserve resource relationships when using native save. DOM export alone is not a complete resource download.
5. Capture the current desktop viewport. For a responsive reference, use a supported viewport override (for example 390 × 844), observe the result, save the mobile screenshot, then restore the viewport.
6. Capture a few defining states only if needed: an open menu, selected tab, or hovered/focused primary control. Do not submit a form or trigger a transaction to discover styling.

For Codex's browser runtime, the tab may expose `capabilities.get("cdp")`. Read that capability's documentation, then use its documented `send` method. Save returned data using the runtime's supported file-writing mechanism. Do not assume arbitrary CDP commands or filesystem APIs are allowed in every environment. `Page.captureSnapshot` can be unavailable even when some CDP commands work.

## Without CDP capture

- Use native browser Save Page As when the available UI supports MHTML and/or "Webpage, Complete". Do not alter browser security settings to enable it.
- A supported browser automation CLI may provide equivalent archive export; use it only if already available or setup is authorized and appropriate.
- If MHTML export is unavailable, continue with the HTML, linked CSS/assets that can actually be retrieved, and screenshots. Identify failed or missing resources. A live computed-style inspection can still support a useful design.md.
- When only server HTML can be obtained, label the capture accordingly: client-rendered content and authenticated states may be absent.

## Capture notes

Record these in the document's Sources & Evidence section:

- Requested URL and final page URL; local timestamp/timezone or UTC.
- Actual archive/document paths and capture method.
- Viewport dimensions and page theme.
- Relevant state, e.g. default page or menu open.
- Missing CSS, fonts, media or cross-origin frames; actual failures rather than hypothetical gaps.

MHTML captures resources available to that browser snapshot. It does not guarantee all fonts, images, dynamic states, future scroll content, scripts, or mobile variants are embedded. Font availability and licensing are separate questions. Do not follow unrelated asset URLs or capture other tabs.
