# Admin panel diagnosis

## Responsible module and function

`src/free_claude_code/api/admin_routes.py`, `_asset_response()` (lines 86–90).
Both `admin_page()` and `admin_asset()` use this helper. It returns
`FileResponse(path)` without specifying a media type for the bundled HTML,
CSS, or JavaScript.

## Root cause and mistaken assumption

The helper assumes that guessing a MIME type from a filename reliably supplies
the browser's required `Content-Type`. That guess depends on Python's MIME
database, including host-specific associations (such as Windows registry MIME
registrations), rather than solely on the known content of the bundled assets.
An incorrect association therefore becomes an incorrect HTTP response header,
even when the file exists and the request succeeds.

For example, an association of `.css` with `text/plain` makes the Admin
stylesheet arrive as plain text. The browser does not apply it, so the panel
loses its layout. An incorrect HTML association can prevent the page from
being interpreted as HTML; a browser-blocked JavaScript MIME type can prevent
the initialization script from running at all. Without that script, the
initial HTML contains empty navigation/configuration containers and a disabled
Apply button.

Restarting `fcc-server` does not repair the host's MIME associations: the same
helper produces the same incorrect headers again. The existing Admin
`Cache-Control: no-store` policy controls caching, not content interpretation.

## Verification

- Executed the unchanged `_asset_response()` function extracted from this
  tree. Its default headers were `text/html`, `text/css`, and
  `text/javascript` (with UTF-8 charset parameters). Overriding the in-memory
  `.css` MIME association to `text/plain` changed the actual helper's response
  header to `text/plain; charset=utf-8` without changing the asset.
- Loaded the repository's actual HTML, CSS, and JavaScript in Chromium with
  intercepted responses using the helper's headers and isolated config/API
  data. With normal types, navigation had three buttons and the sidebar's
  computed display was `flex`. With only the CSS MIME association changed to
  `text/plain`, navigation still initialized but the sidebar's display became
  `block`: the stylesheet was not applied.
- A default config response assembled successfully with 209 fields and 50
  providers. This is not an unconditional failure of config assembly or
  frontend initialization.
- In this Chromium run, JavaScript served as `text/plain` still executed.
  Therefore that particular JavaScript header alone is not evidence of a
  blocked script; the failure depends on the asset, MIME type, and browser.

## Scope and uncertainty

This establishes the asset-serving defect and a reproducible broken-layout
case. The affected user's response headers, browser, and OS associations were
not supplied, so their exact erroneous MIME mapping cannot be identified from
this tree alone. No runtime files were changed and no fix was implemented.
