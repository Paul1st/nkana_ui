// ui_rail.js – the navy side menu ("rail") shown on every desk page.
//
// Built from frappe.boot.allowed_workspaces: the same workspaces, order, icons and permissions
// as Frappe's own workspace sidebar. Desktop: fixed on the left (collapsible to icons).
// Tablet/phone: hidden, slides in from a ☰ button added to the top bar.
// Styles: public/css/rail.css.

const STORE = {
	collapsed: "ui_rail_collapsed",
	open_groups: "ui_rail_open_groups",
	last_workspace: "ui_rail_last_workspace",
};

// Pages that show a DocType: route[1] is the DocType name
const DOCTYPE_VIEWS = ["List", "Form", "Tree", "Report", "Kanban", "Calendar", "Gantt", "Image", "Map", "Dashboard"];

function store_get(key, fallback) {
	try {
		const v = localStorage.getItem(key);
		return v === null ? fallback : JSON.parse(v);
	} catch (e) {
		return fallback;
	}
}

function store_set(key, value) {
	try {
		localStorage.setItem(key, JSON.stringify(value));
	} catch (e) {
		// private mode / storage blocked: the rail still works, it just won't remember
	}
}

class UIRail {
	constructor() {
		this.pages = this.visible(frappe.boot.allowed_workspaces);
		if (!this.pages.length || $(".ui-rail").length) return;

		this.open_groups = new Set(store_get(STORE.open_groups, []));
		this.render();
		this.set_collapsed(store_get(STORE.collapsed, false));
		this.add_mobile_toggle();
		this.update_active();

		frappe.router.on("change", () => {
			this.close_mobile();
			this.update_active();
			// List/Form meta (module) may load just after the route changes
			setTimeout(() => this.update_active(), 400);
		});
	}

	visible(pages) {
		return (pages || []).filter((p) => !p.is_hidden && p.title !== "Welcome Workspace");
	}

	// Called with fresh data whenever Frappe re-fetches the workspace list (page load, and after
	// Save in workspace edit mode), so hiding/deleting/reordering shows up in the menu at once.
	set_pages(pages) {
		if (!this.$rail || !pages) return;
		frappe.boot.allowed_workspaces = pages;
		this.pages = this.visible(pages);
		this.render_nav();
		this.update_active();
	}

	// Some workspaces still name old icons (e.g. "octicon octicon-graph") that are no longer in
	// Frappe's icon sprite and would render blank: fall back to the standard folder icon.
	icon_name(name) {
		if (!name) return "folder-normal";
		const id = name.startsWith("es-") ? name : "icon-" + name;
		return /\s/.test(name) || !document.getElementById(id) ? "folder-normal" : name;
	}

	url(page) {
		return "/app/" + (page.public ? "" : "private/") + frappe.router.slug(page.title);
	}

	key(page) {
		return (page.public ? "pub:" : "priv:") + page.title;
	}

	// ── Rendering ──────────────────────────────────────────────────────────

	render() {
		const user = frappe.session.user;
		const full_name = frappe.session.user_fullname || user;
		this.$rail = $(`
			<aside class="ui-rail" aria-label="${__("Main menu")}">
				<a class="ui-rail__brand" href="/app" title="${__("Home")}">
					<img src="/assets/nkana_ui/images/nkana_logo.png"
						alt="${__("Nkana Water Supply and Sanitation Company")}" width="44" height="39">
					<span class="ui-rail__brand-text">
						<span class="ui-rail__brand-name">${__("Nkana ERP")}</span>
						<span class="ui-rail__brand-sub">${__("Water & Sanitation")}</span>
					</span>
				</a>
				<nav class="ui-rail__nav"></nav>
				<div class="ui-rail__foot">
					<a class="ui-rail__user" href="/app/user/${encodeURIComponent(user)}"
						title="${frappe.utils.escape_html(full_name)}">
						${frappe.avatar(user, "avatar-medium")}
						<span class="ui-rail__user-text">
							<span class="ui-rail__user-name">${frappe.utils.escape_html(full_name)}</span>
							<span class="ui-rail__user-sub">${__("My profile")}</span>
						</span>
					</a>
					<button type="button" class="btn-reset ui-rail__collapse">
						<span class="ui-rail__collapse-icon"></span>
					</button>
				</div>
			</aside>
			<div class="ui-rail-backdrop"></div>
		`);

		this.render_nav();

		this.$rail.find(".ui-rail__collapse").on("click", () => this.set_collapsed(!this.collapsed));
		this.$rail.filter(".ui-rail-backdrop").on("click", () => this.close_mobile());

		$("body").append(this.$rail).addClass("has-ui-rail");
	}

	render_nav() {
		const $nav = this.$rail.find(".ui-rail__nav").empty();
		const pub = this.pages.filter((p) => p.public);
		const priv = this.pages.filter((p) => !p.public);
		this.add_section($nav, __("Workspaces"), pub);
		if (priv.length) this.add_section($nav, __("Personal"), priv);
	}

	add_section($nav, label, pages) {
		if (label) $nav.append(`<div class="ui-rail__label">${frappe.utils.escape_html(label)}</div>`);
		pages
			.filter((p) => !p.parent_page)
			.forEach((p) => $nav.append(this.make_item(p, pages)));
	}

	make_item(page, pages) {
		const children = pages.filter((c) => c.parent_page === page.title);
		const title = __(page.title);
		const icon = page.public
			? frappe.utils.icon(this.icon_name(page.icon), "md")
			: `<span class="ui-rail__dot"></span>`;

		const $group = $(`<div class="ui-rail__group" data-key="${frappe.utils.escape_html(this.key(page))}">
			<div class="ui-rail__row">
				<a class="ui-rail__item" href="${this.url(page)}" title="${frappe.utils.escape_html(title)}">
					<span class="ui-rail__icon">${icon}</span>
					<span class="ui-rail__text">${frappe.utils.escape_html(title)}</span>
				</a>
			</div>
		</div>`);

		if (children.length) {
			const open = this.open_groups.has(this.key(page));
			const $toggle = $(`<button type="button" class="btn-reset ui-rail__toggle"
				aria-label="${__("Show {0} pages", [frappe.utils.escape_html(title)])}" aria-expanded="${open}">
				${frappe.utils.icon("es-line-down", "xs")}
			</button>`);
			const $children = $(`<div class="ui-rail__children"></div>`);
			children.forEach((c) => $children.append(this.make_item(c, pages)));
			$group.find(".ui-rail__row").first().append($toggle);
			$group.append($children).toggleClass("is-open", open);
			$toggle.on("click", () => this.toggle_group($group, page));
		}
		return $group;
	}

	toggle_group($group, page, force) {
		const open = force === undefined ? !$group.hasClass("is-open") : force;
		$group.toggleClass("is-open", open);
		$group.find("> .ui-rail__row .ui-rail__toggle").attr("aria-expanded", open);
		open ? this.open_groups.add(this.key(page)) : this.open_groups.delete(this.key(page));
		store_set(STORE.open_groups, [...this.open_groups]);
	}

	// ── Active page ────────────────────────────────────────────────────────

	find_page(title, is_public) {
		const slug = frappe.router.slug(title || "");
		return this.pages.find((p) => frappe.router.slug(p.title) === slug && !!p.public === is_public);
	}

	current_page() {
		const route = frappe.get_route() || [];

		// Workspace pages: ["Workspaces", "Home"] or ["Workspaces", "private", "My Page"]
		if (route[0] === "Workspaces") {
			const is_private = route[1] === "private";
			const page = this.find_page(is_private ? route[2] : route[1], !is_private);
			if (page) store_set(STORE.last_workspace, this.key(page));
			return page;
		}

		// DocType pages and query reports: use the workspace(s) of their module
		let module = null;
		if (DOCTYPE_VIEWS.includes(route[0]) && route[1]) {
			module = locals.DocType?.[route[1]]?.module;
		} else if (route[0] === "query-report" && route[1]) {
			module = locals.Report?.[route[1]]?.module;
		}
		if (module) {
			const names = (frappe.boot.module_wise_workspaces || {})[module] || [];
			const page = names.map((n) => this.find_page(n, true)).find(Boolean);
			if (page) return page;
		}

		// Anything else: the workspace the user last opened
		const last = store_get(STORE.last_workspace, null);
		return this.pages.find((p) => this.key(p) === last);
	}

	update_active() {
		const page = this.current_page();
		this.$rail.find(".ui-rail__item.is-active").removeClass("is-active").removeAttr("aria-current");
		if (!page) return;

		const $group = this.$rail.find(`.ui-rail__group[data-key="${CSS.escape(this.key(page))}"]`).first();
		$group.find("> .ui-rail__row > .ui-rail__item").addClass("is-active").attr("aria-current", "page");

		// Make sure the active item is visible: open its parent groups
		$group.parents(".ui-rail__group").each((_, el) => {
			const $parent = $(el);
			if (!$parent.hasClass("is-open")) {
				const parent_page = this.pages.find((p) => this.key(p) === $parent.attr("data-key"));
				if (parent_page) this.toggle_group($parent, parent_page, true);
			}
		});
	}

	// ── Collapse (desktop) & slide-in (mobile) ─────────────────────────────

	set_collapsed(collapsed) {
		this.collapsed = !!collapsed;
		$("body").toggleClass("ui-rail-collapsed", this.collapsed);
		this.$rail
			.find(".ui-rail__collapse")
			.attr("aria-expanded", !this.collapsed)
			.attr("title", this.collapsed ? __("Expand menu") : __("Collapse menu"))
			.attr("aria-label", this.collapsed ? __("Expand menu") : __("Collapse menu"));
		this.$rail
			.find(".ui-rail__collapse-icon")
			.html(frappe.utils.icon(this.collapsed ? "es-line-sidebar-expand" : "es-line-sidebar-collapse", "sm"));
		store_set(STORE.collapsed, this.collapsed);
	}

	add_mobile_toggle() {
		const $btn = $(`<button type="button" class="btn-reset ui-rail-mobile-toggle" aria-label="${__("Open menu")}">
			${frappe.utils.icon("menu", "md")}
		</button>`);
		$btn.on("click", () => $("body").toggleClass("ui-rail-open"));
		$(".navbar .container").first().prepend($btn);
	}

	close_mobile() {
		$("body").removeClass("ui-rail-open");
	}
}

// Keep the menu in step with workspace edits: Frappe's workspace page re-fetches the list on
// every (re)load, including right after "Save" in edit mode. Pass the fresh list to the menu.
if (frappe.views && frappe.views.Workspace) {
	const get_pages = frappe.views.Workspace.prototype.get_pages;
	frappe.views.Workspace.prototype.get_pages = function () {
		return get_pages.apply(this, arguments).then((data) => {
			frappe.ui_rail && frappe.ui_rail.set_pages(data && data.pages);
			return data;
		});
	};
}

// "app_ready" fires inside Frappe's start-up: an error here would abort it (no frappe.app, so
// "Log out" and more stop working). Never let the rail take the desk down with it.
$(document).on("app_ready", () => {
	try {
		if (frappe.boot && frappe.boot.allowed_workspaces) {
			frappe.ui_rail = new UIRail();
		}
	} catch (e) {
		console.error("ui_rail:", e);
	}
});
