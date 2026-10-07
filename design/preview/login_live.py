"""Screenshot the live /login (signed out) at given sizes and report page scroll.
Usage: login_live.py WxH [WxH ...]"""
import sys, time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
o = Options(); o.add_argument("-headless")
d = webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver"))
for size in sys.argv[1:]:
    w, h = map(int, size.split("x")); d.set_window_rect(0, 0, w, h)
    d.get("http://127.0.0.1:8000/login"); time.sleep(3)
    print(size, d.execute_script("""const t=document.querySelector('.nk-login__title'), g=document.querySelector('.nk-login__tagline');
      return {scrolls: document.documentElement.scrollHeight > innerHeight + 1, order: t.compareDocumentPosition(g) & 2 ? 'tagline above title' : 'title first',
              title_px: getComputedStyle(t).fontSize}"""))
    d.save_screenshot(f"login_live_{w}x{h}.png")
d.quit()
