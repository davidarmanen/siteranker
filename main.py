from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent


with open("proxy.txt") as f:
    proxy_list = f.readlines()

with open("sites.txt") as f:
    site_list = f.readlines()

def main():
    site_count = 0
    error_2 = 0
    for i in proxy_list:
        useragent = UserAgent()
        useragent = useragent.random
        s = Service("C:/bin/chromedriver.exe")
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={useragent}")
        options.add_argument(f"--proxy-server={i}")
        driver = webdriver.Chrome(service = s,options=options)
        driver.get("https://pr-cy.ru/")
        time.sleep(10)
        for i in range(3):
            try:
                driver.find_element(By.XPATH, "//a[contains(text(),'Проверка посещаемости')]").click()
            except:
                break
            time.sleep(5)
            try:
                input1 = driver.find_element(By.XPATH, "//body/div[@id='app']/div[2]/div[1]/div[1]/div[3]/input[1]")
            except:
                break
            input1.send_keys(site_list[site_count])
            button1 = driver.find_element(By.XPATH, '//button[text()="Проверить"]')
            button1.click()
            time.sleep(3)
            try:
                text1 = driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[3]/div[1]").text
                arr = text1.split("≈", 1)
                with open("out.txt", "a") as f:
                    f.write(site_list[site_count] + arr[1] + "\n")
            except:
                error_2 += 1
                if error_2 == 2:
                    error_2 = 0
                    site_count += 1
                break
            time.sleep(5)
            input1.send_keys(Keys.CONTROL + "a")
            input1.send_keys(Keys.DELETE)
            site_count += 1
            if i == 3:
                break
        driver.close()

main()