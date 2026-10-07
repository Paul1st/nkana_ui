"""Workspace edit mode with the rail: Frappe's sidebar must appear; the rail must rebuild from fresh data.
Clicks Discard at the end, so nothing is saved."""
import time, json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
o=Options(); o.add_argument("-headless")
d=webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0,0,1366,768)
d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name":"sid","value":open(".sid").read().strip(),"path":"/"})
d.get("http://127.0.0.1:8000/app/home"); time.sleep(7)
q = lambda js: d.execute_script(js)
print("patched get_pages:", q("return frappe.views.Workspace.prototype.get_pages.toString().includes('ui_rail')"))
print("before edit: frappe sidebar visible =", q("const s=document.querySelector('.layout-side-section .desk-sidebar'); return !!(s && s.offsetParent)"))
q("document.querySelector('.btn-edit-workspace').click()"); time.sleep(3)
print("edit mode:", q("return !!document.querySelector('.layout-main-section.edit-mode')"),
      "| frappe sidebar visible =", q("const s=document.querySelector('.layout-side-section .desk-sidebar'); return !!(s && s.offsetParent)"),
      "| edit controls =", q("return document.querySelectorAll('.desk-sidebar .sidebar-item-control button, .desk-sidebar .sidebar-item-control .btn').length"))
d.save_screenshot("edit_mode.png")
# simulate a saved change (browser only): hide 'Assets' and check the rail rebuilds without it
before = q("return [...document.querySelectorAll('.ui-rail__item .ui-rail__text')].map(e=>e.textContent.trim())")
q("const p=JSON.parse(JSON.stringify(frappe.boot.allowed_workspaces)); p.find(x=>x.title==='Assets').is_hidden=1; frappe.ui_rail.set_pages(p);")
after = q("return [...document.querySelectorAll('.ui-rail__item .ui-rail__text')].map(e=>e.textContent.trim())")
print("rail rebuild: Assets before =", 'Assets' in before, "| after =", 'Assets' in after, "| active still =", q("const a=document.querySelector('.ui-rail__item.is-active'); return a && a.textContent.trim()"))
# discard (nothing saved)
q("[...document.querySelectorAll('.page-actions button, .page-head button')].find(b=>b.textContent.trim()==='Discard').click()"); time.sleep(4)
print("after discard: edit mode =", q("return !!document.querySelector('.layout-main-section.edit-mode')"),
      "| frappe sidebar visible =", q("const s=document.querySelector('.layout-side-section .desk-sidebar'); return !!(s && s.offsetParent)"),
      "| Assets back in rail =", q("return [...document.querySelectorAll('.ui-rail__item .ui-rail__text')].some(e=>e.textContent.trim()==='Assets')"))
d.quit()
