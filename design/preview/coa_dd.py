"""Open a Link field's dropdown on a short single-doctype form and measure whether it is clipped.
Usage: coa_dd.py [route] [fieldname] (needs .sid)"""
import sys, time, json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
route = sys.argv[1] if len(sys.argv) > 1 else "/app/chart-of-accounts-importer"
field = sys.argv[2] if len(sys.argv) > 2 else "company"
o = Options(); o.add_argument("-headless")
d = webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0,0,1366,768)
d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name": "sid", "value": open(".sid").read().strip(), "path": "/"})
d.get("http://127.0.0.1:8000" + route); time.sleep(8)
d.execute_script("document.documentElement.setAttribute('data-theme','light')")
inp = d.execute_script(f"return document.querySelector('.frappe-control[data-fieldname={field}] input')")
inp.click(); time.sleep(0.3); inp.send_keys(" "); time.sleep(2.5)
print(json.dumps(d.execute_script("""
 const ul=[...document.querySelectorAll('.awesomplete > ul')].find(u=>!u.hidden && u.offsetParent);
 if(!ul) return {open:false};
 const r=ul.getBoundingClientRect(); const out={open:true, items: ul.children.length, top:Math.round(r.top), bottom:Math.round(r.bottom)};
 let e=ul.parentElement; out.clippers=[];
 while(e && e!==document.body){const c=getComputedStyle(e); if(['hidden','clip','auto','scroll'].includes(c.overflowY)||['hidden','clip','auto','scroll'].includes(c.overflow)){const b=e.getBoundingClientRect(); out.clippers.push([e.className.toString().slice(0,60), c.overflow, Math.round(b.bottom)]);} e=e.parentElement;}
 return out""")))
d.save_screenshot("coa_dd.png"); d.quit()
