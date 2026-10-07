"""Screenshot desk routes with the temporary session in .sid.
Usage: shoot.py <WxH> <name>=<route> [<name>=<route> ...]"""
import sys, time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
w, h = map(int, sys.argv[1].split("x"))
o = Options(); o.add_argument("-headless")
d = webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0, 0, w, h)
d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name": "sid", "value": open(".sid").read().strip(), "path": "/"})
for arg in sys.argv[2:]:
    name, route = arg.split("=", 1)
    d.get("http://127.0.0.1:8000" + route); time.sleep(6)
    d.save_screenshot(f"desk_{name}_{w}x{h}.png"); print("saved", name)
d.quit()
