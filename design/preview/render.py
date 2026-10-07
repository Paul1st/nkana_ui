"""Render www/login.html outside Frappe for visual previews (stubs Frappe's web.html + context)."""
import sys
from jinja2 import Environment, DictLoader, FileSystemLoader, ChoiceLoader
APP = "/home/automate/frappe-bench/apps/nkana_ui/nkana_ui"
web = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="/assets/frappe/dist/css/website.bundle.QBE6OIMM.css">
{% block head_include %}{% endblock %}</head><body>
<div class="page-content-wrapper"><main class="{% if not full_width %}container my-4{% endif %}"><div class="page_content">
{% block page_content %}{% endblock %}</div></main></div>{% block script %}{% endblock %}</body></html>"""
env = Environment(loader=ChoiceLoader([FileSystemLoader(APP + "/www"),
    DictLoader({"templates/web.html": web, "templates/includes/login/login.js": "/* frappe login.js */"})]))
env.globals.update(_=lambda s, *a: s, include_style=lambda n: '<link rel="stylesheet" href="/assets/frappe/dist/css/login.bundle.PBLRJU7Y.css">')
variant = sys.argv[1] if len(sys.argv) > 1 else "navy"
src = open(APP + "/www/login.html").read().replace('{% set login_variant = "navy" %}', '{%% set login_variant = "%s" %%}' % variant)
html = env.from_string(src, globals=env.globals).render(full_width=True, login_label="Email", disable_signup=1)
open(f"root/login_{variant}.html", "w").write(html)
