// ui_themes.js – per-user colour themes.
//
// Each user picks a colour theme from the avatar menu ("Colour Theme", next to Frappe's
// "Toggle Theme"). The choice is saved on the server as the user's default `ui_theme`
// (nkana_ui.api.set_ui_theme), arrives in frappe.boot.ui_theme on every page load, and
// is put on <html data-ui-theme="…">. The colours themselves are in public/css/themes.css.
// Light/Dark mode stays Frappe's own setting and works with every colour theme.

const DEFAULT_THEME = "nkana";

// Order shown in the picker. Names must match themes.css and UI_THEMES in api.py.
const THEMES = [
	{ name: "nkana", label: __("Nkana Blue"), description: __("The standard Nkana look: light-blue top bar, navy menu.") },
	{ name: "copper", label: __("Nkana Aqua"), description: __("Aqua top bar and buttons, navy menu.") },
	{ name: "charcoal", label: __("Nkana Navy"), description: __("Dark top bar with blue accents.") },
	{ name: "forest", label: __("Deep Forest"), description: __("Dark-green top bar, white text.") },
	{ name: "ocean", label: __("Ocean Blue"), description: __("Light-blue top bar, navy menu, blue buttons.") },
	{ name: "slate", label: __("Minimal Slate"), description: __("Quiet white top bar with grey-blue accents.") },
];

function known(name) {
	return THEMES.some((t) => t.name === name) ? name : DEFAULT_THEME;
}

function apply_theme(name) {
	document.documentElement.setAttribute("data-ui-theme", known(name));
}

// Apply as early as possible: this file runs before the desk is drawn
apply_theme(frappe.boot && frappe.boot.ui_theme);

frappe.provide("frappe.ui");

frappe.ui.UIThemePicker = class UIThemePicker {
	constructor() {
		this.current = known(frappe.boot.ui_theme);
		this.dialog = new frappe.ui.Dialog({ title: __("Colour Theme") });
		this.dialog.$body.append(`
			<p class="text-muted small mb-3">
				${__("Pick the colours you like. Only you see your choice.")}
				${__("For Light or Dark mode use {0} in this menu.", [`<b>${__("Toggle Theme")}</b>`])}
			</p>`);
		this.$grid = $(`<div class="ui-theme-grid" role="radiogroup"></div>`).appendTo(this.dialog.$body);
		THEMES.forEach((theme) => this.$grid.append(this.option_html(theme)));
		this.$grid.on("click", ".ui-theme-option", (e) => this.select($(e.currentTarget).attr("data-theme-name")));
	}

	option_html(theme) {
		const selected = theme.name === this.current;
		return $(`
			<button type="button" class="ui-theme-option ${selected ? "selected" : ""}"
				role="radio" aria-checked="${selected}" data-theme-name="${theme.name}">
				<div class="ui-theme-swatch" data-ui-theme="${theme.name}" aria-hidden="true">
					<div class="sw-rail"><i></i><i></i><i></i></div>
					<div class="sw-bar"><i></i></div>
					<div class="sw-body">
						<div class="sw-panel"><span class="sw-icon"></span><span class="sw-icon"></span><span class="sw-badge"></span></div>
						<div class="sw-btn"></div>
					</div>
				</div>
				<div class="ui-theme-name">
					<span class="ui-theme-tick">${frappe.utils.icon("tick", "xs")}</span>
					${theme.label}
				</div>
				<div class="ui-theme-desc">${theme.description}</div>
			</button>`);
	}

	select(name) {
		if (name === this.current) return;
		const previous = this.current;
		this.mark(name);
		apply_theme(name);

		frappe
			.xcall("nkana_ui.api.set_ui_theme", { theme: name })
			.then(() => {
				frappe.boot.ui_theme = name;
				frappe.show_alert({ message: __("Colour theme changed"), indicator: "green" }, 3);
			})
			.catch(() => {
				// Not saved: go back to what the server has
				this.mark(previous);
				apply_theme(previous);
			});
	}

	mark(name) {
		this.current = name;
		this.$grid.find(".ui-theme-option").each((i, el) => {
			const on = el.getAttribute("data-theme-name") === name;
			el.classList.toggle("selected", on);
			el.setAttribute("aria-checked", on);
		});
	}

	show() {
		this.dialog.show();
	}
};

// "Colour Theme" in the avatar menu, right after Frappe's "Toggle Theme"
function add_menu_item() {
	// Picker switched off on the server (UI_THEMES_ENABLED in api.py): no menu item
	if (!frappe.boot.ui_themes_enabled) return;
	const $menu = $("#toolbar-user");
	if (!$menu.length || $menu.find(".ui-theme-menu-item").length) return;

	const $item = $(`<button class="btn-reset dropdown-item ui-theme-menu-item">${__("Colour Theme")}</button>`);
	$item.on("click", () => new frappe.ui.UIThemePicker().show());

	const $toggle = $menu.find('[onclick*="ThemeSwitcher"]').first();
	if ($toggle.length) $item.insertAfter($toggle);
	else $menu.prepend($item);
}

// "toolbar_setup" fires inside Frappe's start-up: never let an error here abort it
function safe_add_menu_item() {
	try {
		add_menu_item();
	} catch (e) {
		console.error("ui_themes:", e);
	}
}

$(document).on("toolbar_setup", safe_add_menu_item);
$(safe_add_menu_item);
