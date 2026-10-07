import time, json, sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
o=Options(); o.add_argument("-headless")
d=webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0,0,1366,768)
d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name":"sid","value":open(".sid").read().strip(),"path":"/"})
for r in sys.argv[1:]:
    d.get("http://127.0.0.1:8000"+r); time.sleep(7)
    print(r, json.dumps(d.execute_script("""
    const fl=document.querySelector('.form-layout'); const chain=[]; let e=document.querySelector('.form-section .section-head'); for(let i=0;i<7&&e;i++,e=e.parentElement) chain.push(e.className.slice(0,60));
    const secs=[...document.querySelectorAll('.form-section')].slice(0,14).map(s=>[s.className.replace('row form-section','').trim().slice(0,45), !!s.offsetParent, (s.querySelector(':scope > .section-head')||{}).textContent?.trim().slice(0,28)||null]);
    const ttl=document.querySelector('.page-head .title-area'); 
    return {chain, tabs: document.querySelectorAll('.form-tabs-list .nav-link').length, panes: [...document.querySelectorAll('.tab-pane')].slice(0,3).map(p=>p.className), secs, titleArea: ttl && ttl.outerHTML.replace(/\\s+/g,' ').slice(0,500)}""")))
d.quit()
