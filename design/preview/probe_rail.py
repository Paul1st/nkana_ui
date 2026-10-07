"""Check the side menu (rail) on several desk routes. Usage: probe_rail.py <WxH> <route> [...]"""
import sys, time, json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
w, h = map(int, sys.argv[1].split("x"))
o = Options(); o.add_argument("-headless")
d = webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0, 0, w, h)
d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name": "sid", "value": open(".sid").read().strip(), "path": "/"})
first = True
for route in sys.argv[2:]:
    if first:
        d.get("http://127.0.0.1:8000" + route); time.sleep(7); first = False
        d.execute_script("window.__errs=[]; window.addEventListener('error', e => window.__errs.push(String(e.message)));")
    else:  # navigate inside the app, like a user clicking around
        d.execute_script("frappe.set_route(arguments[0])", route.replace("/app/", "")); time.sleep(4)
    r = d.execute_script("""
      const rail=document.querySelector('.ui-rail'); const act=document.querySelector('.ui-rail__item.is-active');
      const nb=document.querySelector('.navbar'); const ws=document.querySelector('.layout-side-section .desk-sidebar');
      return {route: frappe.get_route_str(), rail: !!rail, railW: rail && Math.round(rail.getBoundingClientRect().width),
        items: document.querySelectorAll('.ui-rail__item').length, active: act && act.textContent.trim(),
        bodyPadL: getComputedStyle(document.body).paddingLeft, navbarLeft: Math.round(nb.getBoundingClientRect().left),
        frappeSidebarVisible: !!(ws && ws.offsetParent), errors: (window.__errs||[]).slice(0,3)}""")
    print(json.dumps(r))
    d.save_screenshot("rail_%s_%s.png" % (route.strip('/').replace('/', '_'), sys.argv[1]))
d.quit()
