"""Open the notification panel at given window sizes and screenshot it + report its box.
Usage: notif_half.py WxH [WxH ...]  (needs .sid)"""
import sys, time, json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
o = Options(); o.add_argument("-headless")
d = webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver"))
d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name": "sid", "value": open(".sid").read().strip(), "path": "/"})
for size in sys.argv[1:]:
    w, h = map(int, size.split("x")); d.set_window_rect(0, 0, w, h)
    d.get("http://127.0.0.1:8000/app/home"); time.sleep(7)
    d.execute_script("document.documentElement.setAttribute('data-theme','light')")
    d.execute_script("$('.dropdown-notifications .notifications-icon').click()"); time.sleep(1.5)
    info = d.execute_script("""const m=document.querySelector('.dropdown-notifications .notifications-list');
      const r=m.getBoundingClientRect(); const b=m.querySelector('.notification-list-body').getBoundingClientRect();
      return {vw: innerWidth, vh: innerHeight, left:Math.round(r.left), right:Math.round(r.right), top:Math.round(r.top), bottom:Math.round(r.bottom), width:Math.round(r.width), body_h: Math.round(b.height),
        css_pos: getComputedStyle(m).position, bell_visible: $('.dropdown-notifications').is(':visible')}""")
    print(size, json.dumps(info))
    d.save_screenshot(f"notif_{w}x{h}.png")
d.quit()
