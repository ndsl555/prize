from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import random

start = time.time()
browser = webdriver.Edge()
account = "pe.iji6847"
password = "10217633"

#自動登入
account_locator = (By.XPATH, 
    "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input")
password_locator = (By.XPATH, 
    "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input")
login_locator = (By.XPATH, 
    "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]")
browser.get("https://www.instagram.com")
account_input = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located(account_locator), 
    "找不到帳號輸入"
)

password_input = browser.find_element(by=By.XPATH, value="/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input")
account_input.send_keys(account)
password_input.send_keys(password)

login_button = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located(login_locator), 
    "找不到登入按鈕"
)
login_button.click()

time.sleep(3)

#跳轉到指定的抽獎頁面
browser.get("https://www.instagram.com/p/CWcNMmhvvDn/")

#當留言數過多時，需要先把整個網頁加載完畢
btn_more_status = True
btn_more_locator = (By.XPATH, 
"/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/li/div/button")

while btn_more_status:
    try:
        btn_more = WebDriverWait(browser, 1).until(
            EC.presence_of_element_located(btn_more_locator) 
        )
        btn_more.click()
    except:
        btn_more_status = False

#載入完成，分析當前頁面
soup = BeautifulSoup(browser.page_source, "html")
lottery = []
for result in soup.find_all("ul", class_="Mr508"):
    #定位留言者
    tager = result.find("a", class_="sqdOP yWX7d _8A5w5 ZIAjV").text
    #定位留言，有標記兩個即符合
    determine = result.find_all("a", class_="notranslate")
    if len(determine) >= 2:
        lottery.append(f'@{tager}')
    
print(f"所有符合資格的人\n{lottery}")
print(f"中獎者\n{random.sample(lottery, 3)}")
end = time.time()
print(f"統計耗時{round(end - start, 3)}s")
#time.sleep(10)


browser.close()
os.system('pause')