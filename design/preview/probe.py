import sys, time, json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
BASE = "http://127.0.0.1:8000"
def driver(w, h):
    o = Options(); o.add_argument("-headless")
    d = webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver"))
    d.set_window_rect(0, 0, w, h); return d

def login_probe(w, h):
    d = driver(w, h); d.get(BASE + "/login"); time.sleep(1.5)
    r = d.execute_script("""
      const de=document.documentElement, vh=innerHeight;
      const out={vh, scrollH: de.scrollHeight, bodyMargin: getComputedStyle(document.body).marginTop+'/'+getComputedStyle(document.body).paddingTop};
      out.tall=[...document.querySelectorAll('body *')].map(e=>{const b=e.getBoundingClientRect();return [e.tagName+'.'+[...e.classList].slice(0,2).join('.'), Math.round(b.top), Math.round(b.bottom)]}).filter(x=>x[2]>vh+1).slice(0,8);
      const pn=document.querySelector('.nk-login__panel'); const p=pn.getBoundingClientRect(); out.card=[Math.round(p.top),Math.round(p.height)]; out.cardScrolls=pn.scrollHeight>pn.clientHeight+1; out.cardContent=pn.scrollHeight; out.parts=['.nk-login__brand','section.for-login','.nk-login__help'].map(q=>{const e=document.querySelector(q);return q.split('__').pop()+':'+Math.round(e.getBoundingClientRect().height)}); delete out.tall;
      return out;""")
    d.save_screenshot(f"probe_login_{w}x{h}.png"); d.quit(); return r

def notif_probe(w, h):
    d = driver(w, h); d.get(BASE + "/login"); d.add_cookie({"name": "sid", "value": open(".sid").read().strip(), "path": "/"})
    d.get(BASE + "/app"); time.sleep(6)
    bell = d.find_element(By.CSS_SELECTOR, ".dropdown-notifications > .nav-link, .dropdown-notifications [data-toggle='dropdown'], .notifications-icon")
    d.execute_script("arguments[0].click()", bell); time.sleep(2)
    r = d.execute_script("""
      const m=document.querySelector('.notifications-list'); const b=m.getBoundingClientRect(); const cs=getComputedStyle(m);
      return {vw:innerWidth, vh:innerHeight, rect:[Math.round(b.left),Math.round(b.top),Math.round(b.width),Math.round(b.height)], minH:cs.minHeight, width:cs.width, items:document.querySelectorAll('.notifications-list .notification-item').length,
              navbarH: Math.round(document.querySelector('.navbar').getBoundingClientRect().height), fontSize: getComputedStyle(document.body).fontSize}""")
    d.save_screenshot(f"probe_notif_{w}x{h}.png"); d.quit(); return r

what = sys.argv[1]
for size in sys.argv[2:]:
    w, h = map(int, size.split("x"))
    print(what, size, json.dumps(login_probe(w, h) if what == "login" else notif_probe(w, h)))
