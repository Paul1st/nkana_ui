import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
o=Options(); o.add_argument("-headless")
d=webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0,0,1366,768)
d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name":"sid","value":open(".sid").read().strip(),"path":"/"})
d.get('http://127.0.0.1:8000/app/workflow-state?style=%5B%22is%22%2C%22not%20set%22%5D'); time.sleep(7)
print("unstyled states listed:", d.execute_script("return document.querySelector('.list-count')?.textContent.trim()"))
d.save_screenshot("wfs_list.png")
d.get("http://127.0.0.1:8000/app/workflow-state/Pending%20TLO%20Confirmation"); time.sleep(6)
d.execute_script("const s=document.querySelector('[data-fieldname=style] select'); s && s.focus();")
print("style options:", d.execute_script("return [...document.querySelectorAll('[data-fieldname=style] select option')].map(o=>o.value).filter(Boolean)"))
d.save_screenshot("wfs_form.png"); d.quit()
