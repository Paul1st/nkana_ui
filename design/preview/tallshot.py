"""Screenshot a whole form (tall window) in light + dark. Usage: tallshot.py <route> <name>"""
import sys, time, json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
o=Options(); o.add_argument("-headless")
d=webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0,0,1366,2600)
d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name":"sid","value":open(".sid").read().strip(),"path":"/"})
d.get("http://127.0.0.1:8000"+sys.argv[1]); time.sleep(8)
print(json.dumps(d.execute_script("""return [...document.querySelectorAll('.page-container .form-page .form-section')].filter(s=>s.offsetParent).map(s=>{const h=s.querySelector(':scope > .section-head'); return [h? h.textContent.trim().slice(0,30):null, h? getComputedStyle(h,'::before').content:null, h? h.className:null, s.className.replace('row form-section card-section','').trim()]})""")))
for t in ("light","dark"):
    d.execute_script("document.documentElement.setAttribute('data-theme', arguments[0])", t); time.sleep(0.5)
    d.save_screenshot(f"{sys.argv[2]}_{t}.png")
d.quit()
