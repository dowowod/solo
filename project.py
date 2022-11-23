from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import googletrans
from googletrans import Translator
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
URL = 'https://www.washingtonpost.com/world/?itid=hp_top_nav_world'
driver.get(url= URL)
driver.implicitly_wait(time_to_wait=10)

elem = driver.find_element(By.TAG_NAME, "body")
a= 0
for i in range(5):
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.1)
    try :
        driver.find_element(By.CSS_SELECTOR,'#__next > div:nth-child(4) > div > main > article > div > div.center.w-100 > div > button').click()
        for i in range(30):
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.1)
    except :
        pass

translator = Translator()
result = []
html = driver.find_elements(By.CSS_SELECTOR,
'#__next > div:nth-child(4) > div > main > article > div > div > div > div.story-headline.pr-sm')
for i in html :
    try :
        c = i.text
        d = c.split('\n')
        if len(d) !=4 :
            pass
        n = i.find_element(By.CSS_SELECTOR,
        '#__next > div:nth-child(4) > div > main > article > div > div > div > div.story-headline.pr-sm > span.font-xxxs.font-light.font--meta-text.lh-sm.gray-dark.dot-xxs-gray-dark')
        e = len(n.text)
        f = d[3]
        str1 = translator.translate(d[0],dest='ko',src="auto")
        str2 = translator.translate(d[1],dest='ko',src="auto")
        str3 = translator.translate(d[2],dest='ko',src="auto")
        str4 = translator.translate(f[:-e],dest='ko',src="auto")
        result.append([d[0]] + [d[1]] +[d[2]] +[f[:-e]] + [f[-e:]] + [str1.text] + [str2.text] + [str3.text]+ [str4.text]+ [f[-e:]])
    except :
        pass
driver.close()
tbl = pd.DataFrame(result, columns=('region','title','main','reporter','day','지역','제목','메인','기자','날짜'))
tbl.to_csv(r'C:\Users\mit\Desktop\solo\news.csv',encoding='utf-8-sig',mode='w',index='true')
