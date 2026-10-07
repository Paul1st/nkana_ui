# Nkana Water and Sanitation UI: maintainer's guide

How the Nkana ERP look-and-feel is built, where to change things, and the traps to avoid.
Keep this file up to date when you add a feature.

---

## 1. What this app is

`nkana_ui` is a **look-and-feel app** for the Nkana Water ERP site. It has no DocTypes.
Its only database change is one customisation shipped as a fixture (extra colour choices for
Workflow State → Style, §13). It does four things:

| What | How it's wired | Files |
|---|---|---|
| Re-skins the **desk** (`/app/...`) | `hooks.py → app_include_css = "ui_desk.bundle.css"` loads one bundled stylesheet on every desk page, after Frappe's own CSS | `public/css/ui_desk.bundle.scss` + the files it imports |
| Adds the **side menu** (navy "rail") on every desk page | `hooks.py → app_include_js = "ui_desk.bundle.js"` loads one bundled script on every desk page | `public/js/ui_desk.bundle.js` → `public/js/ui_rail.js`; styles in `public/css/rail.css` |
| Adds **colours for workflow states** | a fixture adds choices to Workflow State → Style; `ui_workflow_colours.js` maps them to pill colours | `fixtures/property_setter.json`, `api.py`, `public/js/ui_workflow_colours.js`, `public/css/workflow_colours.css` |
| Replaces the **login page** (`/login`) | A page in `www/` named `login` wins over Frappe's own; `website_route_rules` maps `/login` to it | `www/login.html`, `www/login.py`, `public/css/ui_login.bundle.scss` → `login.css` |

Everything in `public/` is served at `/assets/nkana_ui/...` (through the symlink
`sites/assets/nkana_ui → apps/nkana_ui/nkana_ui/public`).

**Bundles:** the `*.bundle.scss` / `*.bundle.js` files are entry points for Frappe's build (`bench build`).
The build combines each one with the plain-CSS files it imports into a single minified,
**fingerprinted** file in `public/dist/css/` (e.g. `ui_desk.bundle.SSI6IM4K.css`), and records the
current name in `sites/assets/assets.json`. Because the name changes whenever the content
changes, browsers always load the latest styles. (A plain `/assets/.../custom.css` link is cached
by browsers for up to 12 hours, which is why changes once "didn't show".)

**Where it's installed (2026-10-07):** the dev site `d-code.localhost` in the frappe_docker
devcontainer (bench at `/workspace/frappe-bench`) only. Not on UAT or Prod yet (§8).

---

## 2. Folder map

```
apps/nkana_ui/
├── GUIDE.md                 ← this file
├── README.md
├── design/
│   ├── reference/           ← brand material and original photos (local only: NOT served, NOT in git)
│   └── preview/             ← tools to screenshot/measure/preview pages (see §7)
└── nkana_ui/
    ├── hooks.py             ← app_include_css, app_include_js, boot_session, /login route, fixtures
    ├── api.py               ← workflow_state_styles(); colour themes: UI_THEMES, set_ui_theme(), boot_session()
    ├── fixtures/
    │   └── property_setter.json ← Workflow State → Style: extra colour choices (+ help text)
    ├── templates/includes/
    │   └── splash_screen.html ← desk loading screen ("The Drop": drop → splash → ripples → Nkana logo), §15
    ├── www/
    │   ├── login.html       ← login page template (settings block at the top)
    │   └── login.py         ← reuses Frappe's login context; sets page title
    └── public/
        ├── css/
        │   ├── nkana_palette.css   ← Nkana brand colours (shared by login + desk)
        │   ├── ui_desk.bundle.scss ← DESK entry point (bundled): imports the files below, in order
        │   ├── variables.css     ←   desk design tokens (--ui-*) + breakpoints + dark mode (= the Nkana Blue theme)
        │   ├── themes.css        ←   per-user colour themes (re-map the roles) + the picker dialog
        │   ├── base.css          ←   body, buttons, dropdown/autocomplete hover
        │   ├── navbar.css        ←   top bar, search, notifications + other navbar dropdowns
        │   ├── sidebar.css       ←   page layout columns + workspace sidebar items
        │   ├── main_section.css  ←   page body, workspace widgets, forms, form tabs
        │   ├── rail.css          ←   the navy side menu (rail) + its desktop/mobile layout
        │   ├── workspace.css     ←   workspace pages: section panels, shortcut pills + icons
        │   ├── form.css          ←   document forms: title accent, status pill, section bars, fields
        │   ├── list.css          ←   lists: header row, wider status column; paging; report tables
        │   ├── workflow_colours.css ← Nkana colours for workflow state pills
        │   ├── dark_mode.css     ←   dark-mode-only surfaces
        │   ├── splash.css        ←   desk loading screen animation (§15)
        │   ├── ui_login.bundle.scss ← LOGIN entry point (bundled): nkana_palette + login.css
        │   └── login.css         ← LOGIN page only (scoped under .nk-login)
        ├── js/
        │   ├── ui_desk.bundle.js ← DESK scripts entry point (bundled)
        │   ├── ui_themes.js      ← per-user colour theme: applies it, "Colour Theme" menu item + picker
        │   ├── ui_rail.js        ← builds the side menu (rail) from the user's workspaces
        │   ├── ui_workspace.js   ← workspace pages: section panels + shortcut icons
        │   └── ui_workflow_colours.js ← workflow state pill colours (new Style choices, fresh styles)
        ├── fonts/           ← Plus Jakarta Sans (self-hosted, OFL licence)
        └── images/          ← Nkana logo, login photos, Automate E + Innovative Dynamics logos
```

---

## 3. Where do I change…?

### Login page

| I want to change… | Go to |
|---|---|
| Any wording (system name, tagline, slogan, mission, vision, welcome headline, feature names) | `www/login.html`, **settings block at the top** |
| Navy vs light-blue footer | `login_variant` in the same settings block |
| Animated water scene vs a still photo | `hero_style` (`"water"` or `"photo"`) and `hero_photo` in the settings block |
| ICT Support / Privacy / Terms links | `ict_support_url`, `privacy_url`, `terms_url` in the settings block |
| A caption on the photo (place / credit) | `photo_caption` in the settings block (empty = hidden) |
| The browser-tab title | `www/login.py` (`context["title"]`) |
| The still photo (`hero_style = "photo"`) | Put it in `public/images/` (≈1400px wide, under ~500 KB) and set `hero_photo` |
| The tap photo in the water scene | `public/images/login_tap.webp` (left half fades to transparent; it is tinted blue by CSS). Its framing: `.nk-login__hero::before` in `login.css` |
| Sizes, spacing, colours | `public/css/login.css`. Tokens (`--rl-*`) are at the top; sections are labelled |
| How much the photo is darkened behind the text | the `linear-gradient(...)` in `.nk-login__hero::after` |

Login-page behaviour that comes from **Frappe settings**, not from this app:
- "Email me a sign-in link" shows only when *System Settings → Login with email link* is on.
- Sign-up link shows only when *Website Settings → Disable Signup* is off.
- Social / LDAP sign-in buttons appear automatically when configured.

### Desk

Desk colours are **roles** in `public/css/variables.css`. Change a role there and every place
that uses it follows:

| Role token | What it colours | Nkana look |
|---|---|---|
| `--ui-navbar-bg` / `--ui-navbar-ink` | Top bar and its text/icons | Nkana Sky / Nkana Navy |
| `--ui-sidebar-bg`, `--ui-sidebar-ink` | Side menu | Nkana Navy / white |
| `--ui-sidebar-active-bg` / `-ink` | Selected menu item's icon tile (and its soft tint) | Nkana Sky / Nkana Navy |
| `--ui-sidebar-accent` | Marker beside the current page, ring around the menu avatar | Nkana Sun (yellow) |
| `--ui-primary` (+ `-hover`, `--ui-on-primary`) | Primary buttons (Save, Add …), focus, Frappe's accent | Royal blue |
| `--ui-badge-bg` / `-ink` | Count badges on shortcuts | Nkana Sun / Nkana Navy |
| `--ui-highlight` | Chart titles; also the current breadcrumb unless a theme sets `--ui-navbar-highlight` | Aqua deep |
| `--ui-avatar-ink`, `--ui-card-hover-border` | Initials in the top-bar avatar; shortcut card border on hover | Aqua deep; Nkana Aqua |
| `--ui-tint`, `--ui-tint-strong` | Soft blue backgrounds: list row hover, dropdown option hover | Sky 20 % / 40 % |
| `--ui-filterbar-bg` (+ `-field-bg`, `-field-border`, `-field-ink`, `-placeholder`, `-focus`) | The filter strip above every list, and the fields/buttons on it | Same blue as the top bar (`var(--ui-navbar-bg)`), white fields, royal-blue focus ring (see §10) |
| `--ui-page-bg`, `--ui-surface`, `--ui-border`, `--ui-text*` | Page, cards, lines, text | Warm off-white, white, stone grey |

| I want to change… | Go to |
|---|---|
| Any of the colours above | `variables.css` |
| Dark-mode colours | the `html[data-theme="dark"]` block in `variables.css` |
| The colour themes users can pick (add, change, remove one) | `themes.css` (see **§14 Colour themes**) |
| Desk font | `--ui-font` in `variables.css` (font file loaded in `base.css`) |
| Navbar height | `--navbar-height` in `variables.css` (also tells Frappe where sticky headers go) |
| Tablet / phone sizes | the `@media (max-width: 991.98px)` / `575.98px` blocks in `variables.css` |
| Buttons, dropdown hover | `base.css` |
| Top bar, breadcrumb, avatar, notifications panel, bell (size, outline, dot colour) | `navbar.css` (dot colour: `--ui-bell-dot` in `variables.css`) |
| Side menu (rail) look: width, badge size, item spacing, collapsed width | `rail.css` (`--ui-rail-width`, `--ui-rail-collapsed-width` at the top) |
| Side menu colours | the `--ui-sidebar-*` roles in `variables.css` |
| Side menu behaviour: which pages, highlighting, collapse, mobile | `public/js/ui_rail.js` (see §10) |
| Frappe's own workspace sidebar (only visible on phones now) | `sidebar.css` |
| Shortcut pills (size, icon circle, count badge position), section panels | `workspace.css` |
| Icons: side menu, shortcuts, the automatic choices | see **§12 Icons** |
| Colour of a workflow state's pill | see **§13 Workflow state colours** |
| Form title accent bar, status pill dot, section bars, column labels, field labels/inputs | `form.css` (accent colour: `--ui-title-accent` in `variables.css`) |
| Bold status pills in lists | `list.css` ("Status pills in list rows") |
| List header row (Employee Name, Status…), status column width, paging buttons, report table colours | `list.css` (report tables use DataTable's `--dt-*` variables, mapped at the `.datatable` rule) |
| Number cards, list filter bar, form card, form tabs | `main_section.css` |

The other CSS files use colour tokens only. If you find a hard-coded colour outside
`variables.css`, `nkana_palette.css` or `login.css`, move it into a token.

---

## 4. Colours

`public/css/nkana_palette.css`, taken from the Nkana logo (`images/nkana_logo.png`):

| Name | Variable | Hex | Use |
|---|---|---|---|
| Nkana Navy | `--nk-navy` | `#0B1F3F` | text, dark surfaces (side menu, login footer) |
| Nkana Sky | `--nk-sky` | `#8ED6F5` | top bar, selected menu item (navy text on it, 10:1) |
| Nkana Aqua | `--nk-aqua` | `#22B8E6` | accent bars, edges, card hover |
| Nkana Sun | `--nk-sun` | `#F5C400` | count badges (navy text on it), lit windows in the splash |
| Royal blue | `--nk-sky-deep` | `#1B3FC4` | **buttons and links with white text** (8.2:1) – the logo's ring |
| Aqua deep | `--nk-aqua-deep` | `#0A6E99` | highlights on white (current breadcrumb, chart titles) |

80/60/40/20 % tints are there too (`--nk-sky-40` etc.).

Logos: `images/nkana_logo.png` (login, side menu, splash). Login footer: "[Automate E logo] by
[Innovative Dynamics logo]" using `images/automatee.png` and `images/innovative_dynamics_light.png`
(white text, navy footer) or `innovative_dynamics.png` (light-blue footer).

---

## 5. Rules that prevent bugs (please read)

1. **Never redefine Frappe's own CSS variables** (`--text-light`, `--text-muted`, `--border-color`,
   `--primary-color`, …). The old theme set `--text-light: #FFFFFF`. Frappe uses that variable for
   error toasts, help text, the timeline and more, so all of that went white-on-white. Use the
   `--ui-*` (desk) or `--rl-*` (login) names instead. The only Frappe variables we deliberately
   set are listed in the "Frappe bridge" in `variables.css`: `--navbar-height`, `--bg-color`,
   `--text-color`, `--primary`.
2. **CSS order matters.** A rule later in the file wins over an equal rule earlier. Put small
   `@media` overrides **after** the base rule they override (see "Short screens" at the end of `login.css`).
3. **Scope the login styles** under `.nk-login` so they can't leak into other web pages.
4. **Keep reference files out of `public/`.** Anything in `public/` can be downloaded by anyone.
5. **Contrast:** white text needs the *deep* blues (royal blue, aqua deep), and the light sky blue or sun yellow needs dark (navy) text.
   Aim for at least **4.5:1** for any text, including placeholder text. Frappe's own placeholder grey
   (`#999` on its light-grey inputs) is only about 2.5:1, which is why we override it desk-wide
   (`base.css`) and on the filter bar.
6. **When you put a colour behind Frappe controls** (inputs, buttons), restyle the controls too.
   Frappe's grey fields disappear on a tinted or coloured background.
7. **Frappe's desk CSS uses `!important` in places** (e.g. `body { padding: 0 !important }`).
   If a rule of ours "does nothing", check whether Frappe forces the property. A more specific
   selector with `!important` wins (that's how the rail's page offset works).
8. **Frappe has two icon families.** Old icons are `<svg class="icon …">` (stroke). The newer
   "espresso" icons are `<svg class="es-icon …">` and are *filled* with `var(--icon-stroke)`.
   To recolour an icon, target `svg` (or both classes) and set `--icon-stroke`. Targeting only
   `.icon` misses the espresso ones (that's why the menu arrows were once nearly invisible).
9. **Never put `overflow` other than `visible` on the form card, or on any box that holds a
   sticky element or a dropdown.** `overflow: hidden`/`auto`/`scroll` makes that box the sticky
   container (on 2026-10-01 the form tab bar stuck 63px down, over "Charge Details"). `overflow: clip`
   avoids that, but still **cuts off dropdowns** that open past the box (2026-10-02: the Company
   list on Chart of Accounts Importer showed only a sliver). To get rounded corners, round the
   child that touches them instead (the form card rounds its tab bar).
10. **Check light AND dark mode.** Dark mode is a per-user setting (avatar menu → Toggle Theme),
   and some users have it on (the Administrator account does). `preview_css.py … light dark`
   screenshots both.

---

**Start-up handlers must never throw.** Frappe fires `startup`, `app_ready` and `toolbar_setup`
*inside* `new frappe.Application()`. If our handler throws there, Frappe's start-up stops half
way: the desk still looks fine, but `frappe.app` is never set, so "Log out" and anything else that
uses `frappe.app` silently stop working. Wrap such handlers in `try { … } catch (e) { console.error(…) }`,
and don't assume `frappe.get_route()` has a value yet (use `(frappe.get_route() || [])[0]`).

---

## 6. Seeing your changes

On **dev** (frappe_docker devcontainer, http://d-code.localhost:8000):

| You changed… | Then |
|---|---|
| Any **CSS or JS** file | `bench build --app nkana_ui`, then `bench --site d-code.localhost clear-cache`, then reload the page. Files saved from Windows don't trigger the container's `bench watch`, so always build by hand. If the page shows **unstyled**, the build raced `bench watch`: build once more when it's idle, clear the cache again, and check the page's `/assets/nkana_ui/dist/css/*.css` links load. |
| `www/login.html` | Just reload the page |
| An image or font | Reload; if it's cached, hard-refresh (**Ctrl+Shift+R**) or rename the file |

Still old? `bench --site d-code.localhost clear-cache`. **Python changes** (`www/login.py`,
`hooks.py`) make the dev web server reload itself, and changing `hooks.py` also needs
`bench --site d-code.localhost clear-cache` (Frappe caches the hooks). Don't touch Frappe files to force that: it takes down the
whole `bench start` (see §9).

---

## 7. Preview & measurement tools (`design/preview/`)

| Script | What it does |
|---|---|
| `render.py <navy\|sky>` | Renders the login template **outside Frappe** (no install needed) into `root/` |
| `probe.py login 1366x768 1920x1080 …` | Opens the live dev login page in headless Firefox at each size. Reports page/card scroll, saves `probe_login_<size>.png` |
| `probe.py notif 1366x768` | Opens the desk, clicks the notification bell, measures the panel. **Needs a session id in `design/preview/.sid`** (create a temporary one; delete it afterwards) |
| `probe_footer.py <sizes>` | Measures the login footer's items, to check they stay on one line |
| `probe_forgot.py` | Checks the forgot-password and email-link screens |
| `probe_frames.py` | Screenshots alternative frame colours (from an earlier design) |
| `shoot.py <WxH> name=/app/route …` | Screenshots desk pages (needs `.sid`) |
| `dom.py /app/route "<css selector>" …` | Prints the HTML/classes/colours of elements, to find what to style (needs `.sid`) |
| `preview_css.py /app/route <file.css> <name> light dark` | **Try a design idea without changing the site:** injects the CSS into the page in the browser only, then screenshots it in light and dark mode (needs `.sid`) |
| `shoot_light.py /app/route` | Screenshots a desk page forced into light mode (needs `.sid`) |
| `probe_rail.py 1366x768 /app/home /app/employee-advance …` | Opens each route (clicking through like a user) and reports: menu present, highlighted item, page offset, script errors (needs `.sid`) |
| `probe_rail2.py` | Tests menu states: expand a group, collapse/expand, dark mode, phone slide-in (needs `.sid`) |
| `probe_edit2.py` | Workspace panels/icons in and out of **Edit** mode. Ends with **Discard** (needs `.sid`) |
| `scrolltabs.py` | Opens the Disciplinary form's Charge tab, scrolls in steps and reports where the tab bar, page header and first section sit (catches sticky-header bugs) (needs `.sid`) |
| `tabs.py /app/<doctype>/<name> <prefix>` | Clicks through a form's tabs, lists each tab's visible section headings with/without numbers, screenshots each tab (needs `.sid`) |
| `blocks.py /app/<workspace> …` | Lists a workspace's editor blocks (headings, shortcuts, cards…) and their widths (needs `.sid`) |
| `login_live.py` | Screenshots the live `/login` (signed out) at the given sizes and reports whether the page scrolls |
| `coa_dd.py` | Opens a Link field's dropdown on a form (default: Company on Chart of Accounts Importer) and lists any ancestor that clips it (needs `.sid`) |
| `notif_half.py` | Opens the notifications panel at the given window sizes (e.g. `683x768 1366x768`), screenshots it and prints its position, so overflow shows up as a negative `left` (needs `.sid`) |
| `themes_shot.py` | Every colour theme on home + a list, Light and Dark, plus the picker (needs `.sid`) |
| `probe_edit.py` | Workspace **Edit** with the menu: Frappe's sidebar appears, the menu rebuilds from new data. Ends with **Discard**, so nothing is saved (needs `.sid`) |

Setup (once): `python3 -m venv design/preview/.venv && design/preview/.venv/bin/pip install selenium`.
Firefox is the snap build: use `/snap/bin/geckodriver`, and keep profiles in a **non-hidden folder
under home** (snap can't read `/tmp` or dot-folders).

Screenshots, `.venv`, `.sid` and `root/` are git-ignored. Only the scripts are tracked.

**Temporary session (`.sid`):** to screenshot desk pages the tools need to be signed in. Create a
short-lived Administrator session on **dev only**, and delete it when done. Never do this on Prod.

```python
# create (run from ~/frappe-bench/sites with ../env/bin/python)
frappe.init(site="frappe.local", sites_path="."); frappe.connect()
# … set frappe.local.request / form_dict / response / cookie_manager, then:
LoginManager().login_as("Administrator"); frappe.db.commit()   # frappe.session.sid → .sid
# delete
from frappe.sessions import delete_session; delete_session(sid); frappe.db.commit()
```

---

## 8. Releasing to UAT / Prod (not done yet)

On the target bench:

```bash
# 1. get the code there (copy the app folder or git pull from a shared remote)
# 2. register it
./env/bin/pip install -e apps/nkana_ui
echo "nkana_ui" >> sites/apps.txt        # check the file ends with a newline first
# 3. back up, then swap themes on the site
bench --site <site> backup
bench --site <site> uninstall-app automatee_theme   # and any other theme app that replaces /login
bench --site <site> install-app nkana_ui
bench build --app nkana_ui
# 4. restart that bench's processes (production: supervisor / systemd)
```

Do UAT first, test, then Prod. Prod has live data: take a backup right before the switch.

`install-app` also loads the app's **fixtures** (the Workflow State → Style colour choices).
If you change that customisation on dev, re-export it with
`bench --site frappe.local export-fixtures --app nkana_ui` and commit the JSON.

---

## 9. Known gotchas

- **Restarting the dev server:** `bench start` runs under honcho. If any one process exits,
  honcho stops them all. Touching a Frappe `.py` file to force a reload took the whole dev
  bench down once. Restart it with `bench start` (it currently runs detached, logging to
  `logs/bench-start.log`).
- **Other theme apps** in the bench (e.g. `automatee_theme`, or another client's UI app) must not be
  installed on the same site as this app: they also replace `/login` and restyle the desk. Only the
  *installed* apps' hooks run, so apps that are merely in the bench are harmless.
- **Browser cache:** fixed for CSS by the fingerprinted bundles (§1). If a change "doesn't show",
  first check you ran `bench build --app nkana_ui`. Images and fonts can still be cached:
  hard-refresh (**Ctrl+Shift+R**).
- **`bench watch` doesn't see edits saved from Windows** (the bind mount sends no file events), so
  run `bench build --app nkana_ui` by hand after CSS/JS edits (§6).

---

## 10. Design decisions (what we chose, why, and how to undo it)

Older versions are all in git history (`git log --oneline`): any of them can be brought back.

### Login page
- **Layout:** the card sits on the left (Nkana logo, company name, form, ICT help). The right side
  is the welcome area: the slogan "Bigger • Better • Smarter", "Welcome to Nkana ERP", a short
  description, the mission card, and three features (Bigger / Better / Smarter, with water-themed
  icons: a drop with a rising arrow, a checked drop with a sparkle, a lightbulb with a drop).
  A navy footer runs underneath.
- **Right-side background (2026-10-07):** `hero_style = "water"` (current): a blue gradient with
  the black-and-white tap photo tinted Nkana blue (`mix-blend-mode: luminosity`), its water
  pouring into slowly drifting waves, plus rising bubbles. `hero_style = "photo"` shows a plain
  photo (`hero_photo`) with no animation and only a soft shade behind the text; it was previewed
  with the tap photo and the user chose the animated version for now.
- **Footer:** "[Automate E logo] by [Innovative Dynamics logo]" on the left, Privacy/Terms on the right.
- **No scrolling on laptops:** measured at 1280×720, 1366×768, 1440×900 and 1920×1080. Spacing
  steps down on short screens. On phones the page scrolls on purpose.
- **"Remember me" left out:** Frappe has no such feature, so the checkbox would do nothing.
- **Login label** follows the site's login settings (currently "Email"). "Employee number"
  sign-in would first need usernames set to employee numbers.
- **"Email me a sign-in link"** is Frappe's *Login with email link* (System Settings). It emails a
  one-time link valid for 10 minutes, at most 5 per address per hour. It only works if outgoing
  email works. Anyone with access to the mailbox can sign in without the password. To remove it,
  untick the setting and the link disappears automatically.

### Desk
- **Colours by role, not by brand colour** (`variables.css`): navbar, side menu, primary
  buttons, badges, highlight, tints. A future per-user theme only has to swap these roles.
- **Light-blue (sky) top bar with navy text; navy side menu; royal-blue buttons; sun-yellow count
  badges; aqua current breadcrumb.** All taken from the Nkana logo (`nkana_palette.css`).
- **List filter bar uses the same blue as the top bar** (`--ui-filterbar-bg: var(--ui-navbar-bg)`),
  with white fields and a royal-blue focus ring.
  - *History (all 2026-10-01):*
    1. A pale tint with Frappe's grey fields was unreadable, so the fields became white and outlined.
    2. A dark bar (white borderless fields, yellow focus ring) was tried, then reverted to pale.
    3. The user then asked for the top-bar colour, which is the current choice.
  - *Why it works:* white fields stand out on the sky blue, and navy text on it is ~10:1. Because it
    reads the top bar's token, the two always match, including in dark mode (both become the dark
    slate top-bar colour) and in future themes.
  - *Dark mode:* the bar follows the dark top bar, so the fields get a visible outline there
    (`--ui-filterbar-field-border` in the dark block). Without it, dark fields on a dark bar vanish.
  - *Trade-off:* a little more colour on list pages than the pale tint. It's still a light colour,
    so the data stays the focus.
  - *Alternatives:* the exact pale and dark values are in the comment above the
    `--ui-filterbar-*` tokens in `variables.css`. Copy them in to switch.
- **Readable placeholders everywhere:** Frappe's `#999` placeholder grey (~2.5:1) is replaced
  desk-wide with `--ui-text-soft` (~5:1). The filter fields were nearly invisible before.
- **Notifications panel:** Frappe's 480 px minimum height and roomy rows covered most of a laptop
  screen. It now sizes to content (max ~440 px list), 400 px wide, with 2-line rows. It opens below
  the 64 px top bar and shows as a sheet on phones.
- **Fingerprinted CSS bundles:** see §1. This is why a page reload is enough after `bench build`.
- **One font across login and desk:** Plus Jakarta Sans, self-hosted (`public/fonts/`, OFL licence).

### Side menu (rail), desk step 2
- **Why a script:** Frappe only has a navigation sidebar on *workspace* pages. The design shows
  the navy menu on every page (lists, forms, reports), so `ui_rail.js` builds one menu and shows
  it everywhere.
- **Look (redesigned 2026-10-07):** a compact logo + "Nkana ERP / Water & Sanitation" lockup at the
  top, a "Workspaces" label, icons in soft rounded tiles, and the current page shown with a soft
  tint, a filled icon tile and a **sun-yellow marker** on the rail edge (the yellow balances the
  blues). The footer is a user card (avatar with a yellow ring, name, "My profile") with a compact
  collapse button. A soft gradient and faint water-wave lines sit behind it. Before this it had a
  big centred badge and a solid light-blue block for the current page.
- **What it shows:** the user's workspaces from `frappe.boot.allowed_workspaces`, the same list,
  order, icons and **permissions** as Frappe's own sidebar. Hidden workspaces are skipped.
  Child workspaces (e.g. Finance → Payables, Receivables, Financial Reports) sit under an
  expand arrow. Private workspaces appear under "Personal".
- **Which item is highlighted:**
  1. on a workspace page, that workspace
  2. on a list/form/report, the workspace for that document's or report's **module** (e.g.
     Employee Advance → HR, General Ledger → Finance), via `frappe.boot.module_wise_workspaces`
  3. otherwise, the workspace the user last opened
- **Old icon names** (e.g. `octicon octicon-graph` on Budget Planning) no longer exist in
  Frappe's icon set. The menu shows the standard folder icon instead of a blank.
- **Desktop:** fixed on the left, 248 px. The top bar and page shift right. The small logo in the
  top bar and Frappe's workspace sidebar are hidden (the menu replaces them), and the breadcrumb's
  leading ">" is removed. The collapse button (bottom right) shrinks it to icons (76 px). The choice and
  the open groups are remembered **per browser** (localStorage).
- **Tablet/phone:** hidden. A ☰ button in the top bar slides it in, and tapping outside or
  navigating closes it.
- **Editing workspaces still works:** on a workspace page click **Edit**. Frappe's own workspace
  sidebar reappears next to the menu, with its controls: drag to reorder, "⋯" for
  hide/delete/duplicate, and hidden workspaces shown greyed. It hides again after Save/Discard
  (CSS: `.layout-main-section.edit-mode` in `rail.css`).
- **The menu stays in sync:** Frappe re-fetches the workspace list every time a workspace page
  (re)loads, including right after **Save**. `ui_rail.js` wraps that fetch
  (`frappe.views.Workspace.prototype.get_pages`) and rebuilds the menu from the fresh list, so
  hidden, deleted, renamed or reordered workspaces show up at once, without a full page reload.
  (Discard doesn't re-fetch: nothing changed, so nothing to update.)
- **To change it:** looks in `rail.css`, colours in `variables.css` (`--ui-sidebar-*`), behaviour
  in `ui_rail.js`. **To turn it off**, remove `app_include_js` from `hooks.py`, remove
  `@import "./rail";` from `ui_desk.bundle.scss`, then `bench build --app nkana_ui` and
  `bench --site d-code.localhost clear-cache`.
- **List pages at laptop width:** the menu (248 px) plus Frappe's list filter panel ("Filter By /
  Assigned To…", ~260 px) leave less room for the list, so long names can get cut off.
  **Decision (2026-10-01): leave it as it is.** When more room is needed, use **Collapse menu**
  (76 px, remembered) or the page's ☰ to hide the filter panel.

### Workspace pages, desk step 3
- **Section panels:** a heading followed by shortcuts ("My Workspace", "Your Shortcuts"…)
  gets a soft blue rounded panel. Frappe's workspace editor owns the blocks,
  so `ui_workspace.js` **doesn't move them**: it measures the group and draws the panel *behind*
  it. It redraws when the page resizes or changes, and **removes the panels while the page is
  in Edit mode**, so editing works exactly as before. The block after a panel gets a little
  extra space (`.ui-ws-after-panel`).
- **Shortcut pills:** full column width with a round light-blue icon, the label, the yellow count
  and a quiet ↗ arrow. Long labels end in "…" rather than overflowing.
- **Which icon a shortcut gets** (details and how to change them in **§12 Icons**):
  1. the shortcut's own **Icon** field, if set
  2. otherwise a match on its label (e.g. "salary" → money, "attendance" → clock,
     "task" → checks, "employee" → people, "leaderboard" → certificate)
  3. otherwise an icon for its type (DocType, Report, Page, Dashboard, URL)

  Icons are added in normal view only, not in Edit mode.
- **Laptop widths (≤1500 px) with the side menu open:** shortcuts show **3 per row** instead
  of 4, so labels like "Employee Record" fit. Wide screens and a collapsed menu keep 4 per
  row. In Edit mode, the column sizes chosen in the editor apply.
- **Not part of the theme:** the "Employee Self Service" cards on Home come from the ESS
  dashboard HTML block, which has its own styles. It could be aligned (icon circles) separately.
- **Noticed while testing (2026-10-01):** the "Budget Planning" workspace was deleted from the
  user's browser via workspace Edit at 20:16. If unintended, restore it from *Deleted Documents*.

### Forms, desk step 4
- **Form styling:**
  - the title gets a small aqua accent bar (`--ui-title-accent`)
  - the status pill ("Not Saved", "Active", "Case Closed"…) shows a coloured dot (Frappe hides it by default)
  - each **section heading becomes a soft blue bar** (without numbers, see below)
  - field labels are stronger, inputs rounded, with a blue focus ring
- **Section numbers (① ② ③) were tried and removed (2026-10-01).** They followed a mockup
  that numbered "1 Employee Information, 2 Gratuity Details, 3 Justification…".
  - *First version* numbered every titled section. On forms like **Disciplinary**, where each tab
    shows one section at a time, every tab showed a lone "①".
  - *Second version* (`ui_form.js`) numbered only tabs with 2+ visible sections.
  - *Decision:* the user chose to **turn numbering off everywhere**. Numbers suit forms filled in
    top to bottom, but add little on record forms people browse (Employee) or on workflow forms
    where sections come and go.
  - *To bring it back:* the code is in git history: commit `8592eaf` (`ui_form.js` + the
    `counter-*` / `::before` rules in `form.css`).
- **Column labels** (a labelled Column Break) are styled as sub-headings: blue, small caps-like,
  with a soft blue underline.
- **Collapsible sections** keep their arrow at the right end of the bar, and the bar darkens
  slightly on hover.
- **Pop-up dialogs** (quick entry, "New …" dialogs) are **not** changed: the rules are scoped to
  forms on the page (`.page-container .form-page`).
- **Known limitation:** the side menu highlights a workspace by the document's *module*. Some
  standard doctypes (e.g. Employee, module "Setup") belong to a module with no workspace here,
  so the menu falls back to the last workspace visited.
- **To undo all form styling:** remove `@import "./form";` from `ui_desk.bundle.scss`, then
  `bench build --app nkana_ui`.

### Lists & reports, desk step 5
- **Kept (user approved):**
  - **Paging** (20 / 100 / 500, Load more): the selected size in soft blue.
  - **Report tables** (Report View and query reports such as General Ledger) use Frappe DataTable,
    whose colours come from `--dt-*` variables. They're mapped to the Nkana roles: soft blue header,
    the border colour, blue row hover and selection, and a blue border on the cell being edited.
- **Tried and reverted the same day (user's choice):** putting lists in a white rounded card,
  restyling the list header row, and rounded/bold status pills (first with a dot, then without).
  Lists are back to Frappe's own look. The code is in commit `fbe1f14` if wanted later.
- **Wider status column:** Frappe gives every list column the same share (~71 px on a laptop with
  the side menu open), which cut status pills short ("Unp…"). The status column is always the
  **3rd** column (name, hidden tag column, status) in both header and rows. So `list.css` gives
  exactly that column **110–170 px**, only on lists that show status pills
  (`.frappe-list:has(… :nth-child(3) .indicator-pill)`). Header and rows stay aligned. The other
  columns get a little narrower. Change the width with `min-width` / `max-width` in that rule.
- **List header row** (the "Employee Name, Status, Employee, Posting Date…" row between the
  filters and the records): Frappe draws it white with light grey text, which was hard to see.
  It's now a **soft blue bar (`--ui-tint-strong`) with dark bold labels**, at the user's
  request. Frappe gives that row `.text-muted`, which forces grey with `!important`, so the
  label colours need `!important` too.
- **Long statuses: tried wrapping, reverted (user's choice, 2026-10-01).** Workflow states here are
  long: up to 42 characters in use ("CEO Approved - Pending Supervisor Approval") and 59 defined.
  Letting the pill text wrap to 2–3 lines (rows growing only when needed) showed every status in
  full, but the user preferred the original one-line look. Long statuses therefore end in "…"
  within the widened status column.
  - Code for wrapping: commit `fcf0744` (block "Long statuses wrap…" in `list.css`).
  - Other ways to show long statuses in full: shorter workflow state names (a workflow change), or
    a wider status column (raise `max-width` in the status-column rule, at the cost of other columns).

- **Report filters use the top-bar colour (decided 2026-10-01).** A paler bar for reports was
  previewed and declined. Reports keep the same filter bar as lists. (If
  ever wanted: set `--ui-filterbar-bg: var(--ui-tint)` and
  `--ui-filterbar-field-border: var(--ui-input-border)` on `body[data-route^="query-report"] .page-form`.)

- **Bold status pills in lists (2026-10-02, user's request).** Only list rows
  (`.frappe-list .list-row .indicator-pill`, weight 700); form titles, reports and the timeline
  keep Frappe's weight. Undo: delete that rule in `list.css`.

### Colour themes (2026-10-02)
- **Currently switched OFF:** everyone gets the designed Nkana Blue look, with the themes kept for
  later. One switch, `UI_THEMES_ENABLED = False` in `api.py`: the server sends Nkana Blue to everyone, hides the menu
  item and refuses to save a theme. Any saved choices stay in the database and come back when
  switched on. See §14 to reactivate.
- **Each user picks; nobody else is affected.** The choice is stored as a **user default**
  (`ui_theme`, in Frappe's DefaultValue table), not a new User field, so no custom field, no
  migrate and nothing to export. Removing the app leaves only harmless DefaultValue rows.
- **Light/Dark stays separate.** Frappe's own "Toggle Theme" still picks Light/Dark/Automatic,
  and it combines with any colour theme. In Dark mode the surfaces stay dark and only the theme's
  accents (buttons, selected menu item, tints, icon circles) change. Giving every theme a full
  dark palette would have meant 12 palettes to keep readable; this keeps it at 6.
- **Themes only re-map role tokens.** No component CSS knows about themes, so a new desk style
  automatically works in every theme as long as it uses `--ui-*` tokens (rule: no hard-coded colours).
  Two hard-coded colours were turned into tokens for this (`--ui-avatar-ink`, `--ui-card-hover-border`).
- **Dark top bars** (Nkana Navy, Deep Forest): the current breadcrumb uses
  `--ui-navbar-highlight` (a lighter highlight) because the normal one is unreadable on a dark bar,
  and the filter bar's focus ring is yellow.
- **Minimal Slate** has a white top bar, so its filter bar is pale (not white) with outlined
  fields, and the avatar circle gets a hairline.
- **Where the picker lives:** the avatar menu, right under "Toggle Theme". Not in the side menu,
  to keep the rail for navigation.
- **Small flash on a full page reload:** the theme is applied by the desk script, which runs
  after the CSS, so for a split second a reload can show Nkana Blue. Moving between pages in the
  desk never reloads, so this is rare. Removing it would mean overriding Frappe's `app.html`.
- **Theme set is a first proposal.** The user asked to "start" the picker; the 6 themes are
  easy to rename, recolour or drop (§14).

### Notification bell (2026-10-02)
- **Why:** the client said users could hardly see the bell. Cause: Frappe draws it as a thin
  outline, and its "new notifications" dot is **green** (`--green-700`), so it vanished into the
  green top bar.
- **Now (user's final choice): Frappe's own bell and dot, made more visible** (`navbar.css`,
  "Notification bell"): 22 px instead of 16 px, a thicker dark outline (a stroke in the same
  colour around Frappe's filled outline shape), and a **red** dot (`--ui-bell-dot`). Behaviour is
  Frappe's: the dot appears when something new arrives and goes when the bell is opened.
- **Tried and reverted the same day (user's choice):**
  - A red number badge counting "new since the bell was last opened". It cleared on open, so
    unread notifications seemed to disappear.
  - Then a number badge counting all unread, on a solid white bell in a charcoal circle (38 users
    would show "99+").
  - Code for both is in git: commits `8118334`, `771b875`, `4cff62f` (`ui_notifications.js`,
    `api.notification_count`).
- **Gotcha:** the bell is an SVG `<use>`, so CSS can't reach its paths directly. Only inherited
  properties get in: `stroke`, `stroke-width`, and CSS variables (`--icon-stroke`, `--green-700`).

### Splash screen (2026-10-02)
- **Nkana (2026-10-07): "The Drop".** One glowing drop falls onto dark water; a jet and droplets
  splash up, rings ripple across the surface, the water swells with drifting waves, soft light rays
  and rising bubbles, and the Nkana logo rises out of it like a bubble while a ring pulses out
  (echoing the ripples). Tagline "Enterprise Resource Planning". Water only, on purpose: the user
  wanted a concept unique to Nkana. 2.4 s, logo-only on later loads.
- **Trade-off:** it holds the screen for 5.2 s even when the desk is ready sooner (about 1 s on dev).
  So it plays **once per sign-in** (once per browser tab until 2026-10-06; the user chose sign-in,
  see §15). Later desk loads show the logo only (0.7 s), and so do users with "reduce motion"
  switched on. A click or Esc skips it. Since 2026-10-06 the full version is 2.4 s.
- **Undo:** delete `templates/includes/splash_screen.html` and Frappe's default comes back. You can
  leave `splash.css` in place, it does nothing without the template.

### Open items
- Real links for ICT Support, Privacy Notice and Terms of Use (login settings block).
- The company vision statement (`vision`) and the ICT support email (`ict_support_url`) for the login page.
- Final login photos, and a high-resolution or vector Nkana logo.
- Decide whether to keep "Login with email link".
- Not theme bugs, noticed on the way: some notifications are sent 2–3 times.

---

## 11. Change log

| Date | Change |
|---|---|
| 2026-10-07 | Login: still-photo option (`hero_style = "photo"`, `hero_photo`) next to the animated water scene; the water scene stays the default (user's choice) |
| 2026-10-07 | Login: tap photo in the water scene, tinted Nkana blue, left edge faded (`login_tap.webp`) |
| 2026-10-07 | Login: features are now Bigger / Better / Smarter with water-themed icons; footer "[Automate E logo] by [Innovative Dynamics logo]" |
| 2026-10-07 | Side menu redesign: logo lockup, "Workspaces" label, icon tiles, soft current-page tint with a sun-yellow marker (`--ui-sidebar-accent`), user card + compact collapse button, gradient and wave lines |
| 2026-10-07 | Rebranded for Nkana Water Supply and Sanitation: blue water palette, Nkana logo, "The Drop" splash, mission and slogan on the login page |
| 2026-10-06 | Splash: full animation now plays **once per sign-in** (was once per tab; logging out and back in in the same tab didn't replay it). The login page clears the flag; later loads show the logo only (§15) |
| 2026-10-06 | Splash: the full version now takes 2.4 s (was 5.2 s; the desk is ready in about 1.2 s). The login page shows only the dark background after Sign in, instead of the unstyled scene (the "black and whitish" flash) (§15) |
| 2026-10-06 | **Fix: login page broken** (login.js shown as text, could not sign in). The splash template's `</script>` closed the login page's script, because login.js embeds the splash in a JS string. The script is now left out on `/login` (§15) |
| 2026-10-02 | Desk splash screen: first animated version (since replaced by "The Drop"); full version once per tab, logo-only afterwards; click/Esc skips (§15) |
| 2026-10-02 | Fix: dropdowns cut off on short forms (e.g. Company on Chart of Accounts Importer). The form card no longer clips (`overflow: clip` → `visible`); its tab bar is rounded instead |
| 2026-10-02 | **Fix: "Log out" did nothing** (`frappe.app.logout is not a function`). `ui_workspace.js` read `frappe.get_route()[0]` in an `app_ready` handler while the route was still null; the error aborted Frappe's start-up, so `frappe.app` was never set. Guarded, and all start-up handlers (`app_ready`, `toolbar_setup`) now catch their own errors. Bug since desk step 3 (`21b9c23`) |
| 2026-10-02 | Notifications panel in narrow windows (e.g. a laptop window snapped to half the screen, under 768 px): was pushed off the left edge by Frappe's `min-width: 100vw`; now the full-width sheet below the top bar (was phones only), text uses the whole width (Frappe capped rows at 455 px / text at 360 px). Bell: no square blue focus box after a click |
| 2026-10-02 | Notification bell back to Frappe's own bell + dot (user's choice): bigger, thicker outline, red dot instead of green; number badge removed |
| 2026-10-02 | Fix: bell number bounced back after opening an unread notification (re-count raced Frappe's save) |
| 2026-10-02 | Notification bell: solid white bell in a charcoal circle; red badge with the number of UNREAD notifications (99+ max), live (`ui_notifications.js`, `api.notification_count`). Replaced the same day's "new since last opened" version |
| 2026-10-02 | Not this app: fixed the ESS dashboard greeting showing `function(uid)…` (Custom HTML Blocks "ESS HTML BLOCK" and "Employee Dashboard" used `frappe.user.full_name` without calling it; now `frappe.session.user_fullname`) |
| 2026-10-02 | Colour themes switched OFF (user's choice): everyone gets the default theme, "Colour Theme" menu item hidden; code kept for later (`UI_THEMES_ENABLED` in `api.py`, §14) |
| 2026-10-02 | Per-user colour themes: 6 themes (now Nkana Blue default, Nkana Aqua, Nkana Navy, Deep Forest, Ocean Blue, Minimal Slate), "Colour Theme" in the avatar menu, saved as a user default (§14) |
| 2026-10-02 | Lists: status pills in bold |
| 2026-10-01 | Forked from `automatee_theme`; token-based colours; fixed invisible Frappe text (`--text-light`) |
| 2026-10-01 | Responsive desk (tablet/phone breakpoints, sticky-header offset, sidebar, tabs) |
| 2026-10-01 | Installed on dev; `automatee_theme` uninstalled there |
| 2026-10-01 | Notifications panel: compact, opens below the navbar, phone sheet |
| 2026-10-01 | Login: first redesign, Plus Jakarta Sans, fits 1280×720+ without scrolling, feature pills in footer |
| 2026-10-01 | Lists: header row as a soft tinted bar with bold labels; report filters use the top-bar colour (pale version declined) |
| 2026-10-01 | Lists: reverted card/header/pill styling (user's choice); status column widened to 110–170 px; paging + report tables kept |
| 2026-10-01 | Workflow state colours: 9 extra Style choices (incl. brand colours) via fixture; current styles fetched per page load |
| 2026-10-01 | Lists: long-status wrapping reverted (user's choice); one-line statuses with "…" |
| 2026-10-01 | Desk step 5: lists/reports back in a white card; list header + pills; paging; report tables in brand colours (`list.css`) |
| 2026-10-01 | Forms: section numbering removed everywhere (user's choice); section bars stay |
| 2026-10-01 | Fix: form tab bar covered the first section while scrolling (form card `overflow: hidden` → `overflow: clip`) |
| 2026-10-01 | Forms: numbers only where a tab has 2+ visible sections (`ui_form.js`); column labels styled as sub-headings |
| 2026-10-01 | Desk step 4: forms: title accent bar, status pill dot, numbered section bars (CSS counters, per tab), rounded inputs + coloured focus |
| 2026-10-01 | Desk step 3: workspace section panels (heading + shortcuts) and shortcut pills with icon circles; 3 pills/row on laptops with the menu open |
| 2026-10-01 | Side menu: workspace **Edit** shows Frappe's sidebar (hide/delete/reorder) again; menu rebuilds from fresh data after Save |
| 2026-10-01 | Desk step 2: side menu (rail) on every desk page: logo badge, user's workspaces with groups, module-based highlighting, collapse to icons, phone slide-in (first app script, `ui_desk.bundle.js`) |
| 2026-10-01 | List filter bar → same colour as the top bar (white fields); pale and dark kept as documented alternatives |
| 2026-10-01 | List filter bar back to a pale tint with white outlined fields (dark kept as a documented alternative) |
| 2026-10-01 | List filter bar → dark with white fields and a yellow focus ring (`--ui-filterbar-*` tokens) |
| 2026-10-01 | List filter bar: white outlined fields; readable placeholder text desk-wide (was #999, ~2.5:1 contrast) |
| 2026-10-01 | Desk + login CSS now built as fingerprinted bundles (`ui_desk.bundle.scss`, `ui_login.bundle.scss`): fixes changes not showing because of browser cache |
| 2026-10-01 | Desk step 1: role-based colour tokens; coloured top bar, dark workspace menu, brand buttons, white shortcut pills with yellow counts, highlighted current breadcrumb, light form tabs, Plus Jakarta Sans |

---

## 12. Icons

There are three places, depending on which icon you want to change.

| Icon | How to change it | Code needed? |
|---|---|---|
| **Side menu** (Home, Finance, HR…) | Open any workspace page and click **Edit**. In the sidebar that appears, open the **⋯** menu on the workspace, choose **Edit**, then use the **Icon** picker and **Save**. The side menu updates at once. | No |
| **One specific shortcut** (e.g. "My Salary Slip") | Frappe's shortcut dialog (pencil in Edit mode) has **no icon field**. Instead, open the workspace record: `/app/workspace/<Workspace name>` (e.g. `/app/workspace/Home`). In the **Shortcuts** table, open the row, type an icon name in **Icon** (e.g. `es-line-payments`), and **Save**. This always beats the automatic choice. Needs the Workspace Manager role. | No |
| **The automatic choice** for shortcuts without their own icon | `public/js/ui_workspace.js`, at the top. **`LABEL_ICONS`** pairs words in the label with an icon (first match wins), e.g. `[/salary\|payslip\|…/, "es-line-payments"]`. **`TYPE_ICONS`** is the fallback per shortcut type (DocType, Report, Page, Dashboard, URL). Edit or add a line, then `bench build --app nkana_ui` and reload. | Yes |

**Valid icon names** come from Frappe's built-in icon sets. An unknown name shows a folder
(side menu) or the automatic choice (shortcuts) instead of a blank.

*Line icons (newer set; recommended for shortcuts), used with their full name:*

`es-line-activity` · `es-line-add` · `es-line-add-circle` · `es-line-add-emoji` · `es-line-add-people` · `es-
line-agent` · `es-line-agent-alt` · `es-line-alert-circle` · `es-line-alert-triangle` · `es-line-align` · `es-
line-align-center` · `es-line-align-justify` · `es-line-align-right` · `es-line-all-apps` · `es-line-archive`
· `es-line-arrow-left` · `es-line-arrow-right` · `es-line-arrow-up-right` · `es-line-article` · `es-line-
attachment` · `es-line-bold` · `es-line-book` · `es-line-bullet-list` · `es-line-calender` · `es-line-call` ·
`es-line-camera` · `es-line-certificates` · `es-line-chart` · `es-line-chat` · `es-line-chat-alt` · `es-line-
check` · `es-line-close` · `es-line-close-circle` · `es-line-cloud` · `es-line-code` · `es-line-colour` · `es-
line-compact` · `es-line-copy` · `es-line-copy-light` · `es-line-create-ticket` · `es-line-cursor` · `es-line-
customer` · `es-line-darkmode` · `es-line-dash` · `es-line-dashboard` · `es-line-decrease-indent` · `es-line-
delete` · `es-line-delete-alt` · `es-line-demand-video` · `es-line-details` · `es-line-discussions` · `es-
line-dislike` · `es-line-divider` · `es-line-dot` · `es-line-dot-horizontal` · `es-line-dot-vertical` · `es-
line-double-check` · `es-line-down` · `es-line-download` · `es-line-drag` · `es-line-duplicate` · `es-line-
edit` · `es-line-edit-alt` · `es-line-email` · `es-line-embed` · `es-line-emoji` · `es-line-expand` · `es-
line-filetype` · `es-line-file-upload` · `es-line-filter` · `es-line-folder` · `es-line-folder-alt` · `es-
line-folder-shared` · `es-line-folder-upload` · `es-line-globe` · `es-line-group` · `es-line-header-column` ·
`es-line-header-row` · `es-line-heart` · `es-line-hide` · `es-line-home` · `es-line-image` · `es-line-image-
alt1` · `es-line-inbox` · `es-line-increase-indent` · `es-line-italic` · `es-line-laptop` · `es-line-left-
chevron` · `es-line-like` · `es-line-link` · `es-line-location` · `es-line-lock` · `es-line-log-out` · `es-
line-manage` · `es-line-mark-unread` · `es-line-minimise` · `es-line-mobile` · `es-line-move` · `es-line-new-
folder` · `es-line-nextweek` · `es-line-notes` · `es-line-notifications` · `es-line-notifications-unseen` ·
`es-line-numbered-list` · `es-line-overdue` · `es-line-overflow` · `es-line-pages` · `es-line-pages-alt` ·
`es-line-payments` · `es-line-pentagon` · `es-line-people` · `es-line-pin` · `es-line-plan` · `es-line-plans`
· `es-line-preview` · `es-line-privacy-alt` · `es-line-progress` · `es-line-question` · `es-line-quiz` · `es-
line-quote` · `es-line-quotes-alt` · `es-line-reload` · `es-line-reply` · `es-line-reply-all` · `es-line-
reports` · `es-line-resizer` · `es-line-restrictions` · `es-line-right-chevron` · `es-line-search` · `es-line-
security` · `es-line-select` · `es-line-select-file` · `es-line-settings` · `es-line-share` · `es-line-
sidebar-collapse` · `es-line-sidebar-expand` · `es-line-slash` · `es-line-sort` · `es-line-sparkle` · `es-
line-square` · `es-line-star` · `es-line-status` · `es-line-storage` · `es-line-strike-through` · `es-line-
success` · `es-line-support` · `es-line-table-view` · `es-line-tag` · `es-line-teams` · `es-line-template` ·
`es-line-text-cursor` · `es-line-tick` · `es-line-ticket` · `es-line-ticket-alt` · `es-line-ticket-no-` · `es-
line-tiles` · `es-line-time` · `es-line-title` · `es-line-today` · `es-line-today-alt` · `es-line-tomorrow` ·
`es-line-unarchive` · `es-line-underline` · `es-line-unlock` · `es-line-unpin` · `es-line-up` · `es-line-
upload` · `es-line-video` · `es-line-web` · `es-line-web-link` · `es-line-weekend` · `es-line-wifi-off` · `es-
line-youtube` · `es-line-zap`

*Classic icons (used by most workspaces), written **without** the `icon-` prefix (e.g. `hr`,
`accounting`, `users`):*

`accounting` · `add` · `add-round` · `agriculture` · `arrow-down-left` · `arrow-down-right` · `arrow-left` ·
`arrow-right` · `arrow-up-right` · `assets` · `assign` · `attachment` · `both` · `branch` · `buying` ·
`calendar` · `call` · `card` · `change` · `chart` · `check` · `clap` · `clipboard` · `close` · `close-alt` ·
`collapse` · `color-energy-points` · `color-monthly-rank` · `color-rank` · `color-review-points` · `comment` ·
`criticize` · `crm` · `crop` · `customer` · `customization` · `dashboard` · `dashboard-list` · `delete` ·
`delete-active` · `dialpad` · `dot-horizontal` · `dot-vertical` · `down` · `down-arrow` · `drag` · `drag-sm` ·
`duplicate` · `edit` · `edit-fill` · `edit-round` · `education` · `equity` · `expand` · `expand-alt` ·
`expenses` · `external-link` · `file` · `file-large` · `filter` · `filter-x` · `folder-normal` · `folder-
normal-large` · `folder-open` · `full-page` · `gantt` · `getting-started` · `group-by` · `header` · `header-1`
· `header-2` · `header-3` · `header-4` · `header-5` · `header-6` · `healthcare` · `heart` · `heart-active` ·
`help` · `hide` · `hr` · `image` · `image-view` · `income` · `insert-above` · `insert-below` · `integration` ·
`kanban` · `keyboard` · `left` · `liabilities` · `link-url` · `list` · `list-alt` · `loan` · `lock` · `mail` ·
`map` · `mark-as-read` · `menu` · `message` · `message-1` · `milestone` · `money-coins-1` · `month-view` ·
`move` · `non-profit` · `notification` · `notification-with-indicator` · `number-card` · `onboarding` ·
`organization` · `pen` · `permission` · `primitive-dot` · `printer` · `project` · `project-1` · `project-2` ·
`projects` · `quality` · `quality-3` · `quantity-1` · `read-status` · `refresh` · `remove` · `reply` · `reply-
all` · `restriction` · `retail` · `review` · `right` · `scan` · `search` · `select` · `sell` · `setting` ·
`setting-gear` · `share` · `share-people` · `shortcut` · `shrink` · `sidebar-collapse` · `sidebar-expand` ·
`small-add` · `small-down` · `small-file` · `small-message` · `small-up` · `solid-error` · `solid-info` ·
`solid-success` · `solid-warning` · `sort` · `sort-ascending` · `sort-descending` · `spacer` · `star` ·
`stock` · `support` · `table` · `tag` · `text` · `tick` · `today` · `tool` · `unhide` · `unlock` · `unread-
status` · `up` · `up-arrow` · `up-line` · `upload` · `upload-lg` · `users` · `view` · `website` · `workflow`

---

## 13. Workflow state colours

**Choosing a colour (no code):**
1. Open the list of states **without a colour**:
   `/app/workflow-state?style=["is","not set"]` (250 of 307 on 2026-10-01). Or open any state
   from `/app/workflow-state`.
2. Open a state, pick a **Style**, and **Save**.
3. Reload the list or form that shows it. The pill uses the new colour (no cache clearing needed).

States that already have a style keep it. Nothing changes until you pick something.

**The choices:**

| Style | Pill colour | Source |
|---|---|---|
| Primary / Info / Success / Warning / Danger / Inverse | blue / light blue / green / orange / red / black | Frappe |
| Yellow / Purple / Pink / Cyan / Dark Grey | Frappe's built-in pill colours of those names | added by this app |
| Nkana Blue / Nkana Aqua / Nkana Yellow / Nkana Navy | Nkana brand colours (light + dark mode) | added by this app |
| (empty) | grey | Frappe default |

**How it works:**
- **Extra dropdown choices:** a **Property Setter** on Workflow State → `style` (options + help
  text), shipped as the app fixture `fixtures/property_setter.json`. It's created by `install-app`
  and refreshed by `migrate`.
- **Mapping:** `public/js/ui_workflow_colours.js` wraps `frappe.get_indicator` and colours a pill
  only when the pill shows the document's **workflow state**.
- **Fresh colours:** Frappe keeps each doctype's workflow states in its *cached* metadata, so on
  its own a changed colour wouldn't show until caches were cleared. The script fetches the
  current styles once per page load from `nkana_ui.api.workflow_state_styles` (state
  names and colours only, so any logged-in user may read it) and re-draws the list/form on
  screen. Until that answer arrives, Frappe's cached style is used.
- **Nkana colours:** defined in `public/css/workflow_colours.css` as `--bg-nk-*` /
  `--text-on-nk-*`, the same pattern as Frappe's own pill colours.

**Adding another colour choice:**
1. Add it to the Style options (Customize Form → Workflow State → `style` → Options, or edit the
   Property Setter).
2. Add a line to `STYLE_COLOURS` in `ui_workflow_colours.js`, using a Frappe pill colour (`green`,
   `cyan`, `blue`, `orange`, `yellow`, `gray`, `red`, `pink`, `darkgrey`, `purple`, `light-blue`)
   or a new `nk-*` class defined in `workflow_colours.css`.
3. `bench build --app nkana_ui`, then re-export the fixture.

**Tested 2026-10-01:** "CEO Approved - Pending Supervisor Approval" was given a brand colour. The
Travel Request list showed the new pill colour right away. The state was then set back to no style.

---

## 14. Colour themes

> **Status: switched OFF.** Everyone sees Nkana Blue and there is no menu item.
> **To reactivate:** set `UI_THEMES_ENABLED = True` in `api.py`, let the web workers reload
> (dev reloads by itself; production: restart the bench processes), then
> `bench --site <site> clear-cache` so cached boot data picks it up. No build is needed.

**For users:** avatar (top right) → **Colour Theme** → click a card. It changes at once and is
remembered for that user on every device. Light/Dark is still **Toggle Theme**.

**The themes:** Nkana Blue (`nkana`, default), Nkana Aqua (`copper`), Nkana Navy (`charcoal`),
Deep Forest (`forest`), Ocean Blue (`ocean`), Minimal Slate (`slate`). (The ids `copper` and
`charcoal` are kept so saved user choices still work; only the labels changed.)

**How it works:**
1. `api.set_ui_theme(theme)` saves the user default `ui_theme` (only names in `UI_THEMES`).
2. `api.boot_session` (hook `boot_session`) puts it in `frappe.boot.ui_theme` on page load.
3. `ui_themes.js` sets `<html data-ui-theme="…">` and adds the menu item + picker dialog.
4. `themes.css` re-maps the `--ui-*` role tokens for `html[data-ui-theme="…"]` (Light mode),
   `.ui-theme-swatch[data-ui-theme="…"]` (the preview card) and
   `html[data-ui-theme="…"][data-theme="dark"]` (Dark-mode accents).

**Add a theme:** (1) a block in `themes.css` (copy one, keep all three selectors), (2) an entry in
`THEMES` in `ui_themes.js`, (3) its name in `UI_THEMES` in `api.py`, then
`bench build --app nkana_ui` (the .py change needs the web workers to reload).
**Remove a theme:** delete it from all three; users who had it fall back to Nkana Blue.
**Change the default:** `DEFAULT_THEME` in `ui_themes.js` and `DEFAULT_UI_THEME` in `api.py`, and
move that theme's values into `variables.css` (the page's base values are Nkana Blue).

**Check a change:** `design/preview/themes_shot.py` (needs `.sid`) screenshots home + a list in
every theme, Light and Dark, plus the picker. It switches themes in the browser only and saves nothing.

**Set a user's theme for them (admin):** `frappe.defaults.set_user_default("ui_theme", "copper", user="someone@example.com")`.

---

## 15. Splash screen (desk loading screen)

**What it is:** the screen between logging in and the desk appearing. Frappe's default is a small
logo on a blank page. Ours overrides `templates/includes/splash_screen.html`: Frappe's template
loader checks later-installed apps first, so our copy wins. Nothing in Frappe is edited.

**Files:** `templates/includes/splash_screen.html` (scene SVG + a small script) and
`public/css/splash.css` (all the animation, in `ui_desk.bundle.css`, which loads in `<head>`, so
the scene is styled from the first paint). After a CSS change: `bench build --app nkana_ui`.

**Timeline:** the drop falls, splashes and ripples, the water swells, then the logo rises with a
pulsing ring; the full version takes 2.4 s (it was 5.2 s until 2026-10-06; it was cut because the
desk itself is ready in about 1.2 s). To change a moment, edit its `animation-delay` in `splash.css`.

**How it hides:** Frappe removes `.splash` when the desk is built. The template keeps an empty
`.splash` as a signal, and our own `#ui-splash` overlay fades out once **both** the desk is ready
and the minimum time has passed (`FULL_MS` = 2400, `SHORT_MS` = 700 in the template script).
A 15 s safety timer always removes it.

**Once per sign-in** (since 2026-10-06; was once per tab): the flag is `localStorage.ui_splash_played`.
The login page (`www/login.html`, `{% block script %}`) removes it, and the first desk load after that
plays the full scene and sets it again. Every later load (refresh, new tab, reload after an update)
shows the logo only until the next sign-in. To see the full version without signing out, run
`localStorage.removeItem("ui_splash_played")` in the browser console and refresh.
- Why not once per tab (the first version): Frappe doesn't clear the tab's `sessionStorage` on log
  out, so signing out and back in in the same tab never replayed it, while opening a link in a new
  tab did. That felt random. Every load (too slow on the 3rd refresh) and once per day (missed when
  the session survives overnight) were also considered and rejected.
- Not covered: a session that ends without the login page (e.g. an expired session that is resumed
  by "Login as" or an SSO redirect that skips `/login`) just shows the logo-only version, which is harmless.
- Undo (back to once per tab): in the template script use `sessionStorage` instead of `localStorage`,
  and remove the `removeItem` line from `www/login.html`.

**Logo:** `images/nkana_logo.png`, set directly in the template.

**Gotchas:**
- Keep every moving part on CSS animations (one clock). An SMIL animation runs on the SVG's own
  clock and drifts out of sync.
- It's the same water scene in Light and Dark mode, on purpose.
- **The login page includes this template too.** Frappe's `login.js` puts it inside a JS string
  (`document.body.innerHTML = `…``) to show it right after sign-in, and that string sits inside the
  login page's `<script>`. A literal `</script>` in our template ends that block early: the rest of
  login.js shows as text on the page and sign-in stops working. So the template's script is wrapped
  out on the login page by `{% if for_test == "login.html" %}` (`for_test` is set only by Frappe's
  login context; don't use `boot`, website pages have it too). On the login page the template
  outputs only a div with the scene's dark background (inline style, because splash.css isn't loaded
  there). Without it, the scene flashed unstyled (grey and black shapes on white) after Sign in. The
  desk splash starts on the same background, so the hand-over is seamless. Keep every `<script>`
  in the desk branch.
- Screenshots: `design/preview/splash_frames.py <WxH> [times…]` (needs `.sid`). Never open a second
  tab in the script: a background tab freezes the animation and the frames look stuck.
  `splash_timing.py` shows when the desk becomes ready.

