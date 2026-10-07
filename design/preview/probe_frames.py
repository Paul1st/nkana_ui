import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
o=Options(); o.add_argument("-headless")
d=webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0,0,1366,768)
d.get("http://127.0.0.1:8000/login"); time.sleep(2)
for f in ("white","dark"):
    d.execute_script("const r=document.querySelector('.nk-login'); r.className=r.className.replace(/nk-login--frame-\\w+/, 'nk-login--frame-'+arguments[0]);", f)
    time.sleep(0.5); d.save_screenshot(f"frame_{f}.png")
d.quit()
