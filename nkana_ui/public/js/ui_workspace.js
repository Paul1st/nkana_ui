// ui_workspace.js – workspace page touches (section panels, shortcut icons).
//
// 1. Section panels: a heading followed by shortcuts ("My Workspace", "Your Shortcuts", …) gets a
//    soft blue rounded panel drawn BEHIND that group. The editor's blocks are never moved
//    (Frappe's workspace editor owns them), so Edit/Save keep working. Panels are recalculated
//    when the page resizes or redraws, and removed while the page is in edit mode.
// 2. Shortcut icons: every shortcut pill starts with a round icon. It uses the shortcut's own
//    icon if one is set, otherwise one matched from its label, otherwise one for its type.
// Styles: public/css/workspace.css.

// ── 2. Shortcut icons ────────────────────────────────────────────────────────

// First match wins; checked against the lower-cased label
const LABEL_ICONS = [
	[/leader|rank|award|recogni/, "es-line-certificates"],
	[/salary|payslip|pay slip|payroll|wage/, "es-line-payments"],
	[/advance|loan|petty|expense|claim|payment|money|cash|gratuity|allowance|budget/, "es-line-payments"],
	[/attendance|check.?in|timesheet|overtime|shift/, "es-line-time"],
	[/leave|holiday|calendar|plan/, "es-line-calender"],
	[/reminder|notification|alert/, "es-line-notifications"],
	[/task|todo|to do|assignment|action/, "es-line-double-check"],
	[/profile|account|my details/, "es-line-customer"],
	[/employee|staff|people|team|member|directory/, "es-line-people"],
	[/travel|trip|vehicle|transport|fleet|mileage/, "es-line-location"],
	[/report|ledger|statement|summary/, "es-line-reports"],
	[/dashboard|analytics|kpi|performance|appraisal/, "es-line-chart"],
	[/contract|policy|document|letter|notice|disciplinary/, "es-line-notes"],
	[/requisition|request|order|purchase|procure|material|stock|item|asset/, "es-line-article"],
	[/project/, "es-line-folder"],
	[/support|help|ticket|issue/, "es-line-support"],
	[/setting|config/, "es-line-settings"],
];

const TYPE_ICONS = {
	DocType: "es-line-filetype",
	Report: "es-line-reports",
	Page: "es-line-pages",
	Dashboard: "es-line-dashboard",
	URL: "es-line-web-link",
};

function icon_exists(name) {
	if (!name || /\s/.test(name)) return false;
	return !!document.getElementById(name.startsWith("es-") ? name : "icon-" + name);
}

function shortcut_icon(widget) {
	if (icon_exists(widget.icon)) return widget.icon;
	const label = (widget.label || "").toLowerCase();
	const match = LABEL_ICONS.find(([re]) => re.test(label));
	if (match) return match[1];
	return TYPE_ICONS[widget.type] || "es-line-filetype";
}

const ShortcutWidget = frappe.widget && frappe.widget.widget_factory && frappe.widget.widget_factory.shortcut;
if (ShortcutWidget) {
	const set_actions = ShortcutWidget.prototype.set_actions;
	ShortcutWidget.prototype.set_actions = function () {
		set_actions.apply(this, arguments);
		if (this.in_customize_mode || !this.widget || this.widget.find(".ui-sc-icon").length) return;
		const $head = this.widget.find(".widget-head").first();
		$(`<span class="ui-sc-icon" aria-hidden="true">${frappe.utils.icon(shortcut_icon(this), "sm")}</span>`)
			.prependTo($head);
		this.widget.addClass("has-ui-icon");
	};
}

// ── 1. Section panels ────────────────────────────────────────────────────────

const PANEL_PAD = 14; // how far the panel extends around its blocks (px)

function in_edit_mode(editor) {
	return !!$(editor).closest(".layout-main-section").hasClass("edit-mode");
}

function draw_panels(editor) {
	$(editor).children(".ui-ws-panel").remove();
	$(editor).find(".ui-ws-after-panel").removeClass("ui-ws-after-panel");
	const redactor = editor.querySelector(".codex-editor__redactor");
	if (!redactor || in_edit_mode(editor) || !editor.offsetParent) return;

	// Groups: a heading block followed by one or more shortcut blocks
	const groups = [];
	let current = null;
	for (const block of redactor.children) {
		if (block.querySelector(".ce-header")) {
			current = { head: block, items: [] };
			groups.push(current);
		} else if (current && block.querySelector(".shortcut-widget-box")) {
			current.items.push(block);
		} else {
			current = null;
		}
	}

	const base = editor.getBoundingClientRect();
	groups
		.filter((g) => g.items.length)
		.forEach((g) => {
			const rects = [g.head, ...g.items].map((b) => b.getBoundingClientRect());
			const top = Math.min(...rects.map((r) => r.top)) - base.top;
			const left = Math.min(...rects.map((r) => r.left)) - base.left;
			const right = Math.max(...rects.map((r) => r.right)) - base.left;
			const bottom = Math.max(...rects.map((r) => r.bottom)) - base.top;
			$(`<div class="ui-ws-panel" aria-hidden="true"></div>`)
				.css({
					top: top - PANEL_PAD / 2,
					left: left - PANEL_PAD,
					width: right - left + PANEL_PAD * 2,
					height: bottom - top + PANEL_PAD * 1.5,
				})
				.prependTo(editor);
			$(g.head).addClass("ui-ws-panel-head");
			// push the next block down so it doesn't touch the panel
			$(g.items[g.items.length - 1]).next(".ce-block").addClass("ui-ws-after-panel");
		});
}

// Watch the visible workspace editor: redraw on content changes, resizes and edit-mode toggles
const watched = new WeakSet();
let redraw_timer = null;

function schedule(editor) {
	clearTimeout(redraw_timer);
	redraw_timer = setTimeout(() => draw_panels(editor), 120);
}

function watch(editor) {
	if (watched.has(editor)) return schedule(editor);
	watched.add(editor);
	const redactor = editor.querySelector(".codex-editor__redactor");
	const section = $(editor).closest(".layout-main-section")[0];
	const mo = new MutationObserver((records) => {
		// ignore our own panel insertions
		if (records.every((r) => [...r.addedNodes, ...r.removedNodes].every((n) => n.classList && n.classList.contains("ui-ws-panel")))) return;
		schedule(editor);
	});
	redactor && mo.observe(redactor, { childList: true, subtree: true });
	section && mo.observe(section, { attributes: true, attributeFilter: ["class"] });
	if (window.ResizeObserver) new ResizeObserver(() => schedule(editor)).observe(editor);
	schedule(editor);
}

function find_editor(tries = 25) {
	const editor = $(".page-container:visible .codex-editor").get(0);
	if (editor) return watch(editor);
	if (tries > 0) setTimeout(() => find_editor(tries - 1), 200);
}

// "app_ready" fires INSIDE Frappe's start-up (new frappe.Application()). An error thrown here
// aborts the start-up, so frappe.app is never set and things like "Log out" stop working.
// The route can still be null at this moment, hence the guard, and the try/catch as a backstop.
$(document).on("app_ready", () => {
	const on_route = () => {
		try {
			if ((frappe.get_route() || [])[0] === "Workspaces") find_editor();
		} catch (e) {
			console.error("ui_workspace:", e);
		}
	};
	frappe.router.on("change", on_route);
	on_route();
});
