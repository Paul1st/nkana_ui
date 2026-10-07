import time, json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
o=Options(); o.add_argument("-headless")
d=webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0,0,1366,768)
d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name":"sid","value":open(".sid").read().strip(),"path":"/"})
d.get("http://127.0.0.1:8000/app/travel-request"); time.sleep(8)
pills=lambda: d.execute_script("return [...document.querySelectorAll('.list-row-container .indicator-pill')].slice(0,6).map(p=>[p.textContent.trim().slice(0,28), [...p.classList].filter(c=>!['indicator-pill','filterable','no-indicator-dot','ellipsis'].includes(c)).join(' '), getComputedStyle(p).backgroundColor])")
print("list:", json.dumps(pills()))
d.save_screenshot("wfc_list.png")
name=d.execute_script("const a=[...document.querySelectorAll('.list-row-container')].find(r=>r.textContent.includes('CEO Approved - Pending Supervisor')); return a && a.querySelector('[data-name]')?.getAttribute('data-name')")
if name:
    d.get("http://127.0.0.1:8000/app/travel-request/"+name); time.sleep(8)
    print("form pill:", d.execute_script("const p=document.querySelector('.page-head .indicator-pill'); return p && [p.textContent.trim(), p.className, getComputedStyle(p).backgroundColor]"))
    d.save_screenshot("wfc_form.png")
d.quit()
