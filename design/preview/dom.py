"""Dump compact DOM/class info for selectors on a desk route. Usage: dom.py <route> <selector> [...]"""
import sys, time, json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
o = Options(); o.add_argument("-headless")
d = webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0, 0, 1366, 768)
d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name": "sid", "value": open(".sid").read().strip(), "path": "/"})
d.get("http://127.0.0.1:8000" + sys.argv[1]); time.sleep(6)
for sel in sys.argv[2:]:
    r = d.execute_script("""const e=document.querySelector(arguments[0]); if(!e) return null;
      const cs=getComputedStyle(e); return {html:e.outerHTML.replace(/\\s+/g,' ').slice(0,420), bg:cs.backgroundColor, color:cs.color, h:Math.round(e.getBoundingClientRect().height)}""", sel)
    print("##", sel, json.dumps(r)[:640])
d.quit()
