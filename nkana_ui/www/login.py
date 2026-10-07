import frappe
from frappe.www.login import get_context as frappe_login_context

no_cache = True


def get_context(context):
	# Reuse Frappe's login context (logo, LDAP, social logins, signup flags, 2FA, redirects)
	frappe_login_context(context)
	context.full_width = True
	context["title"] = "ERP | " + frappe._("Nkana Water Supply and Sanitation Company")
	return context
