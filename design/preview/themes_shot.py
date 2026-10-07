"""Screenshot every colour theme (light + dark) on a few desk pages, plus the picker dialog.
Usage: themes_shot.py  (needs .sid). Switches themes client-side only; saves nothing."""
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
THEMES = ["nkana", "copper", "charcoal", "forest", "ocean", "slate"]
o = Options(); o.add_argument("-headless")
d = webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0, 0, 1366, 768)
d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name": "sid", "value": open(".sid").read().strip(), "path": "/"})
for page, route in [("home", "/app/home"), ("list", "/app/travel-request")]:
    d.get("http://127.0.0.1:8000" + route); time.sleep(7)
    for mode in ["light", "dark"]:
        for t in THEMES:
            d.execute_script(f"document.documentElement.setAttribute('data-theme','{mode}');"
                             f"document.documentElement.setAttribute('data-ui-theme','{t}')")
            time.sleep(0.4); d.save_screenshot(f"th_{page}_{mode}_{t}.png")
d.execute_script("document.documentElement.setAttribute('data-theme','light');"
                 "document.documentElement.setAttribute('data-ui-theme','nkana')")
print("menu item:", d.execute_script("return $('#toolbar-user .ui-theme-menu-item').length + ' after ' + $('#toolbar-user .ui-theme-menu-item').prev().text().trim()"))
d.execute_script("$('#toolbar-user .ui-theme-menu-item').click()"); time.sleep(1.5)
d.save_screenshot("th_dialog_light.png")
d.execute_script("document.documentElement.setAttribute('data-theme','dark')"); time.sleep(0.4)
d.save_screenshot("th_dialog_dark.png")
print("bold:", d.execute_script("let p=document.querySelector('.frappe-list .list-row .indicator-pill');return p&&getComputedStyle(p).fontWeight"))
d.quit()
