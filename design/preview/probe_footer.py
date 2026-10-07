import time, sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
o=Options(); o.add_argument("-headless")
d=webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver"))
for size in sys.argv[1:]:
    w,h=map(int,size.split('x')); d.set_window_rect(0,0,w,h); d.get("http://127.0.0.1:8000/login"); time.sleep(1.5)
    print(size, d.execute_script("""const f=document.querySelector('.nk-login__footer'); const cs=getComputedStyle(f);
      return {footerH: Math.round(f.getBoundingClientRect().height), footerW: Math.round(f.clientWidth), pad: cs.paddingLeft+'/'+cs.paddingRight, gap: cs.columnGap,
       kids: [...f.children].map(c=>[c.className.replace('nk-login__',''), Math.round(c.getBoundingClientRect().width), Math.round(c.getBoundingClientRect().top)])}"""))
d.quit()
