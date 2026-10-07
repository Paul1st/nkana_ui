"""Workspace panels vs edit mode. Ends with Discard: nothing is saved."""
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
o=Options(); o.add_argument("-headless")
d=webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0,0,1366,768)
d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name":"sid","value":open(".sid").read().strip(),"path":"/"})
d.get("http://127.0.0.1:8000/app/home"); time.sleep(7)
q=lambda js: d.execute_script(js)
state=lambda: q("return {panels: document.querySelectorAll('.ui-ws-panel').length, icons: document.querySelectorAll('.ui-sc-icon').length, edit: !!document.querySelector('.layout-main-section.edit-mode')}")
print("view   :", state())
q("document.querySelector('.btn-edit-workspace').click()"); time.sleep(3)
print("edit   :", state()); d.save_screenshot("edit_mode_ws.png")
q("[...document.querySelectorAll('.page-actions button, .page-head button')].find(b=>b.textContent.trim()==='Discard').click()"); time.sleep(5)
print("discard:", state()); d.quit()
