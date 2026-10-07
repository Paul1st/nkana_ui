import time, json, sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
o=Options(); o.add_argument("-headless")
d=webdriver.Firefox(options=o, service=Service("/snap/bin/geckodriver")); d.set_window_rect(0,0,1366,768)
d.get("http://127.0.0.1:8000/login"); d.add_cookie({"name":"sid","value":open(".sid").read().strip(),"path":"/"})
for r in sys.argv[1:]:
    d.get("http://127.0.0.1:8000"+r); time.sleep(7)
    print(r, json.dumps(d.execute_script("""const red=document.querySelector('.codex-editor__redactor');
      const st=red && getComputedStyle(red);
      return {redactor: red && red.className, display: st && st.display, wrap: st && st.flexWrap, parent: red && red.parentElement.className,
        blocks: red ? [...red.children].map(b=>[b.className, b.querySelector('.ce-header')?'header:'+b.textContent.trim().slice(0,25): (b.querySelector('.widget')? b.querySelector('.widget').className.replace('widget ','').slice(0,40) : b.textContent.trim().slice(0,20)), Math.round(b.getBoundingClientRect().width), getComputedStyle(b).paddingLeft]) : null}""")))
d.quit()
