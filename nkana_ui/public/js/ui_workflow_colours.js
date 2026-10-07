// ui_workflow_colours.js – colours for workflow state pills.
//
// Pick a state's colour in Workflow State → Style. Besides Frappe's six (Primary, Info, Success,
// Warning, Danger, Inverse) this app adds Yellow, Purple, Pink, Cyan, Dark Grey and the Nkana colours
// to that dropdown (fixture: fixtures/property_setter.json).
//
// Frappe keeps each doctype's workflow states (with their styles) in its cached metadata, so a
// changed colour wouldn't show until caches are cleared. Instead, the current styles are fetched
// once per page load (nkana_ui.api.workflow_state_styles) and used for every workflow
// pill. Until they arrive, Frappe's cached style is used. Nkana colours: public/css/workflow_colours.css.

const STYLE_COLOURS = {
	// Frappe's own
	Primary: "blue",
	Info: "light-blue",
	Success: "green",
	Warning: "orange",
	Danger: "red",
	Inverse: "black",
	// added by this app
	Yellow: "yellow",
	Purple: "purple",
	Pink: "pink",
	Cyan: "cyan",
	"Dark Grey": "darkgrey",
	"Nkana Blue": "nk-blue",
	"Nkana Aqua": "nk-aqua",
	"Nkana Yellow": "nk-yellow",
	"Nkana Navy": "nk-navy",
};

let current_styles = null; // { state name: style } once loaded

function style_of(state) {
	if (current_styles) return current_styles[state] || "";
	return (locals["Workflow State"] && locals["Workflow State"][state]?.style) || "";
}

if (frappe.get_indicator) {
	const get_indicator = frappe.get_indicator;
	frappe.get_indicator = function (doc, doctype) {
		const indicator = get_indicator.apply(this, arguments);
		try {
			if (!indicator || !doc) return indicator;
			const fieldname = frappe.workflow.get_state_fieldname(doctype || doc.doctype);
			const state = fieldname && doc[fieldname];
			// only when the pill shown IS the workflow state (its filter is "<field>,=,<state>")
			if (state && indicator[2] === `${fieldname},=,${state}`) {
				indicator[1] = STYLE_COLOURS[style_of(state)] || "gray";
			}
		} catch (e) {
			// never break Frappe's own indicator
		}
		return indicator;
	};
}

$(document).on("app_ready", () => {
	frappe
		.xcall("nkana_ui.api.workflow_state_styles")
		.then((styles) => {
			current_styles = styles || {};
			// redraw what's on screen with the current colours
			if (window.cur_list && cur_list.refresh) cur_list.refresh();
			if (window.cur_frm && cur_frm.doc && !cur_frm.is_new() && cur_frm.page) cur_frm.refresh_header();
		})
		.catch(() => {
			// keep Frappe's cached styles
		});
});
