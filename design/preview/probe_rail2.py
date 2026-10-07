import time, json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
def drv(w,h):
    o=Options(); o.add_argument("-headless")
    d=webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0,0,w,h)
    d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name":"sid","value":open(".sid").read().strip(),"path":"/"}); return d
# desktop: expand Finance, then collapse the rail, then dark mode
d=drv(1366,768); d.get("http://127.0.0.1:8000/app/home"); time.sleep(7)
d.execute_script("localStorage.removeItem('ui_rail_collapsed'); localStorage.removeItem('ui_rail_open_groups');")
d.execute_script("[...document.querySelectorAll('.ui-rail__group')].find(g=>g.querySelector('.ui-rail__text').textContent.trim()==='Finance').querySelector('.ui-rail__toggle').click()"); time.sleep(0.5)
print("finance children:", d.execute_script("return [...document.querySelectorAll('.ui-rail__group.is-open .ui-rail__children .ui-rail__text')].map(e=>e.textContent.trim())"))
d.save_screenshot("rail_expanded.png")
d.execute_script("document.querySelector('.ui-rail__collapse').click()"); time.sleep(0.6)
print("collapsed:", d.execute_script("return {railW: document.querySelector('.ui-rail').getBoundingClientRect().width, pad: getComputedStyle(document.body).paddingLeft, stored: localStorage.getItem('ui_rail_collapsed')}"))
d.save_screenshot("rail_collapsed.png")
d.execute_script("document.querySelector('.ui-rail__collapse').click(); document.documentElement.setAttribute('data-theme','dark')"); time.sleep(0.6)
d.save_screenshot("rail_dark.png"); d.quit()
# phone: open the slide-in
d=drv(500,900); d.get("http://127.0.0.1:8000/app/employee-advance"); time.sleep(7)
print("phone before:", d.execute_script("return {toggle: !!document.querySelector('.ui-rail-mobile-toggle') && document.querySelector('.ui-rail-mobile-toggle').offsetParent!==null, railX: Math.round(document.querySelector('.ui-rail').getBoundingClientRect().left), pad: getComputedStyle(document.body).paddingLeft}"))
d.save_screenshot("rail_phone_closed.png")
d.execute_script("document.querySelector('.ui-rail-mobile-toggle').click()"); time.sleep(0.6)
print("phone open:", d.execute_script("return {railX: Math.round(document.querySelector('.ui-rail').getBoundingClientRect().left), backdrop: getComputedStyle(document.querySelector('.ui-rail-backdrop')).opacity}"))
d.save_screenshot("rail_phone_open.png")
d.execute_script("document.querySelector('.ui-rail-backdrop').click()"); time.sleep(0.6)
print("phone after backdrop click:", d.execute_script("return Math.round(document.querySelector('.ui-rail').getBoundingClientRect().left)"))
d.quit()
