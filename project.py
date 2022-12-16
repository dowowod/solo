from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from googletrans import Translator
import pandas as pd
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
URL = 'https://www.washingtonpost.com'
driver.get(url= URL)
driver.implicitly_wait(time_to_wait=10)


a= 0
b = input('검색을 하시겠습니까?(y/n)')
count = 1
cha = 0
if b == 'y' :
    try :
        while(1) :
            text = input('무엇을 검색하시겠습니까.(영어입력)')
            if text.encode().isalpha():
                break
        driver.find_element(By.CSS_SELECTOR,'#__next > div > div.PJLV.wpds-c-khdSlv.wpds-c-fqeRep > nav > div.wpds-c-kKPYWe.wpds-c-kKPYWe-cIACJd-variant-leftSide > div.PJLV.wpds-c-cMsOSt.chromatic-ignore > button').click()
        c = driver.find_element(By.CSS_SELECTOR,'#query')
        c.send_keys(text)
        c.send_keys(Keys.RETURN)
        elem = driver.find_element(By.TAG_NAME, "body")
        button = driver.find_element(By.CSS_SELECTOR,'#main-content > div.jsx-2309075444.search-app-container.mr-auto.ml-auto.flex.flex-column.col-8-lg > section.jsx-2865089505.search-results-wrapper > button')
        cha = 1
    except :
        pass
else :
    tags=driver.find_elements(By.CSS_SELECTOR,'#__next > div > div.PJLV.wpds-c-khdSlv.wpds-c-fqeRep > nav > ul > li > a > p')
    button = driver.find_elements(By.CSS_SELECTOR,'#__next > div:nth-child(4) > div > main > article > div > div.center.w-100 > div > button')
    tag =[]
    for t in tags :
        tag.append("{}. ".format(count)+t.text)
        count += 1
    print(tag)
    big = int(input('원하는 주제의 번호를 입력하세요'))
    tags[big-1].click()
    small = input('더 자세한 주제 원한다면 y를 입력하세요.(y/n)')
    if small == 'y' :
        elem = driver.find_element(By.TAG_NAME, "body")
        stags = driver.find_elements(By.CSS_SELECTOR,'#__next > header > div > div > nav > div > div > a')
        stag = []
        count = 1
        for s in stags :
            stag.append("{}. ".format(count)+s.text)
            count += 1
        print(stag)
        bigg = int(input('원하는 주제의 번호를 입력하세요'))
        stags[bigg-1].click()
    else :
        pass
elem = driver.find_element(By.TAG_NAME, "body")
for i in range(2):
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.1)
    try :
        button.click()
        for i in range(20):
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.1)
    except :
        pass

translator = Translator()
result = []
final = []
gi = []
if cha == 0 :
    html = driver.find_elements(By.CSS_SELECTOR,'#__next > div:nth-child(4) > div > main > article > div > div > div > div.story-headline.pr-sm')
    for i in html :
        try :
            c = i.text
            d = c.split('\n')
            if len(d) !=4 :
                pass
            n = i.find_element(By.CSS_SELECTOR,'#__next > div:nth-child(4) > div > main > article > div > div > div > div.story-headline.pr-sm > span.font-xxxs.font-light.font--meta-text.lh-sm.gray-dark.dot-xxs-gray-dark')
            e = len(n.text)
            f = d[3]
            str1 = translator.translate(d[0],dest='ko',src="auto")
            str2 = translator.translate(d[1],dest='ko',src="auto")
            result.append([d[0]] + [d[1]] +[d[2]] +[f[:-e]] + [f[-e:]] + [str1.text] + [str2.text] + [d[2]]+[f[:-e]] + [f[-e:]])
            if len(result) == 10:
                count = 1
                for j in result :
                    print("{}. ".format(count)+j[1])
                    count += 1
                while(1):
                    n = int(input('삭제할 기사를 입력하세요.(끝낼려면 "0" 입력)'))
                    if n == 0 :
                        break
                    result.pop(n-1)
                    count = 1
                    for j in result :
                        print("{}. ".format(count)+j[1])
                        count += 1
                final.extend(result)
                result = []
        except:
            pass
else :
    html = driver.find_elements(By.CSS_SELECTOR,'#main-content > div.jsx-2309075444.search-app-container.mr-auto.ml-auto.flex.flex-column.col-8-lg > section.jsx-2865089505.search-results-wrapper > article > div.content-lg.pt-xxxs.pb-xxxs.antialiased.flex.align-items.bc-gray-light > div.pr-sm.flex.flex-column.justify-between.w-100')
    for i in html :
        try :
            c = i.text
            d = c.split('\n')
            if len(d) !=4 :
                pass
            str1 = translator.translate(d[0],dest='ko',src="auto")
            str2 = translator.translate(d[1],dest='ko',src="auto")
            result.append([d[0]] + [d[1]] +[d[2]] +[d[3]] + [d[4]] + [str1.text] + [str2.text] + [d[2]]+[d[3]] + [d[4]])
            if len(result) == 10:
                count = 1
                for j in result :
                    print("{}. ".format(count)+j[1])
                    count += 1
                while(1):
                    n = int(input('삭제할 기사를 입력하세요.(끝낼려면 "0" 입력)'))
                    if n == 0 :
                        break
                    result.pop(n-1)
                    count = 1
                    for j in result :
                        print("{}. ".format(count)+j[1])
                        count += 1
                final.extend(result)
                result = []
        except:
            pass
driver.close()
tbl = pd.DataFrame(final, columns=('topic','title','main','reporter','day','주제','제목','메인','기자','날짜'))
tbl.to_csv(r'C:\Users\mit\Desktop\solo\news.csv',encoding='utf-8-sig',mode='w',index='true')