# A4 to A0 pattern converter (SewCraftly tool)

Client-side tool: pdf.js analyses the tiled pages (cut lines + layout), pdf-lib writes the A0 PDF as vector form XObjects at 100% scale.

- `src/tool.js` + `src/widget.html` → `build.py` → `widget.html` (WordPress reusable block, JS stored as text/plain with & replaced by ǂ).
- `pages.json`: EN/FR/DE/NL page bodies ({{BLOCK}} = widget block id).
- `test/gen.py` builds synthetic tiled patterns, `test/run.py` checks the output against the master drawing.
