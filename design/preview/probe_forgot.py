import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
o=Options(); o.add_argument("-headless")
d=webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0,0,1366,768)
d.get("http://127.0.0.1:8000/login#forgot"); time.sleep(2)
print(d.execute_script("return {forgotVisible: getComputedStyle(document.querySelector('section.for-forgot')).display, loginVisible: getComputedStyle(document.querySelector('section.for-login')).display, scrollH: document.documentElement.scrollHeight, vh: innerHeight}"))
d.save_screenshot("probe_forgot.png")
d.get("http://127.0.0.1:8000/login#login-with-email-link"); time.sleep(2)
print(d.execute_script("return {emailLinkVisible: getComputedStyle(document.querySelector('section.for-login-with-email-link')).display}"))
d.quit()
