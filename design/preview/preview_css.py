"""Screenshot a desk route with extra CSS injected (preview only, nothing saved).
Usage: preview_css.py <route> <css-file> <out-prefix> [light|dark ...]"""
import sys, time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
route, cssfile, out = sys.argv[1:4]; themes = sys.argv[4:] or ["light"]
css = open(cssfile).read()
o = Options(); o.add_argument("-headless")
d = webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0, 0, 1366, 768)
d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name": "sid", "value": open(".sid").read().strip(), "path": "/"})
d.get("http://127.0.0.1:8000" + route); time.sleep(6)
d.execute_script("const s=document.createElement('style'); s.textContent=arguments[0]; document.head.appendChild(s);", css)
for t in themes:
    d.execute_script("document.documentElement.setAttribute('data-theme', arguments[0])", t); time.sleep(1)
    d.save_screenshot(f"{out}_{t}.png"); print("saved", f"{out}_{t}.png")
d.quit()
