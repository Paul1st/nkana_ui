import frappe


@frappe.whitelist()
def workflow_state_styles():
	"""Workflow State name → Style, for every state that has a style.

	The desk uses this (public/js/ui_workflow_colours.js) to colour workflow pills with the CURRENT
	styles. Frappe's own copy travels with each doctype's cached metadata, so a colour changed in
	Workflow State would otherwise not show until caches are cleared. State names and colours are
	not sensitive, so this is readable by any logged-in user.
	"""
	return dict(
		frappe.get_all(
			"Workflow State",
			filters={"style": ["is", "set"]},
			fields=["name", "style"],
			as_list=True,
		)
	)


# Colour themes a user can pick (public/css/themes.css, public/js/ui_themes.js). "nkana" is the default.
UI_THEMES = ("nkana", "copper", "charcoal", "forest", "ocean", "slate")
DEFAULT_UI_THEME = "nkana"

# Switched off 2026-10-02 (user's choice): everyone gets the default and the "Colour Theme" menu item
# is hidden. Saved choices are kept. Set to True (and reload the web workers) to bring the picker back.
UI_THEMES_ENABLED = False


def get_ui_theme():
	if not UI_THEMES_ENABLED:
		return DEFAULT_UI_THEME
	theme = frappe.defaults.get_user_default("ui_theme")
	return theme if theme in UI_THEMES else DEFAULT_UI_THEME


@frappe.whitelist()
def set_ui_theme(theme):
	"""Save the current user's colour theme. Stored as a user default, so no extra DB fields are needed."""
	if not UI_THEMES_ENABLED:
		frappe.throw(frappe._("Colour themes are switched off."))
	if theme not in UI_THEMES:
		frappe.throw(frappe._("Unknown colour theme: {0}").format(theme))
	frappe.defaults.set_user_default("ui_theme", theme)
	return theme


def boot_session(bootinfo):
	"""hooks.py boot_session: the desk reads frappe.boot.ui_theme on page load."""
	bootinfo.ui_theme = get_ui_theme()
	bootinfo.ui_themes_enabled = UI_THEMES_ENABLED

