"""Click through a form's tabs; screenshot each and list visible section headings + numbers."""
import sys, time, json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
o=Options(); o.add_argument("-headless")
d=webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0,0,1366,1500)
d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name":"sid","value":open(".sid").read().strip(),"path":"/"})
d.get("http://127.0.0.1:8000"+sys.argv[1]); time.sleep(8)
n=d.execute_script("return document.querySelectorAll('.form-tabs-list .nav-link').length")
for i in range(n):
    name=d.execute_script("const l=document.querySelectorAll('.form-tabs-list .nav-link')[arguments[0]]; l.click(); return l.textContent.trim()", i); time.sleep(1.2)
    info=d.execute_script("""return [...document.querySelectorAll('.page-container .form-page .tab-pane.active .form-section')].filter(s=>s.offsetParent).map(s=>{const h=s.querySelector(':scope > .section-head'); return h? (getComputedStyle(h,'::before').content+' '+h.textContent.trim().slice(0,30)) : '(no heading)'})""")
    print(f"[{name}]", info)
    d.save_screenshot(f"{sys.argv[2]}_tab{i}.png")
d.quit()
