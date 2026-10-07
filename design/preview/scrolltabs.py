"""Reproduce: sticky form tabs vs section bars while scrolling."""
import time, json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
o=Options(); o.add_argument("-headless")
d=webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0,0,1366,768)
d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name":"sid","value":open(".sid").read().strip(),"path":"/"})
d.get("http://127.0.0.1:8000/app/disciplinary/DP-2026-00101"); time.sleep(8)
d.execute_script("[...document.querySelectorAll('.form-tabs-list .nav-link')].find(l=>l.textContent.trim()==='Charge').click()"); time.sleep(1)
info = lambda: d.execute_script("""
 const tabs=document.querySelector('.form-tabs-list'); const head=document.querySelector('.page-head'); const nav=document.querySelector('.navbar');
 const sec=[...document.querySelectorAll('.tab-pane.active .section-head')].find(e=>e.offsetParent);
 const r=e=>{if(!e) return null; const b=e.getBoundingClientRect(); const c=getComputedStyle(e); return {top:Math.round(b.top), bottom:Math.round(b.bottom), pos:c.position, z:c.zIndex, bg:c.backgroundColor, cls:e.className.slice(0,60)}};
 return {scrollY: Math.round(scrollY), navbar:r(nav), pagehead:r(head), tabs:r(tabs), section:r(sec)}""")
for i,y in enumerate([0, 150, 260, 400]):
    d.execute_script("window.scrollTo(0, arguments[0])", y); time.sleep(0.6)
    print(json.dumps(info())); d.save_screenshot(f"scroll_{i}.png")
d.quit()
