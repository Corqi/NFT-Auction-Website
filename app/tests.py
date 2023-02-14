import threading

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
buttons = []


def click_button(button):
    button.click()


def init_page_get_btn(username, value):
    options = webdriver.ChromeOptions()
    options.add_argument("−−incognito")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get('http://127.0.0.1:5000/login')
    driver.find_element(By.ID, 'inputEmail').send_keys(username)
    driver.find_element(By.ID, 'inputPassword').send_keys(username)
    driver.find_element(By.XPATH, '/html/body/div/div/div/form/dl/div/button').click()
    driver.get('http://127.0.0.1:5000/auction/1')
    driver.find_element(By.ID, 'price').send_keys(str(value))
    found_button = False
    while not found_button:
        found_button = driver.find_element(By.XPATH,
                                     '/html/body/div/div[1]/div/div[2]/div[4]/div[3]/form/dl/div/button').is_displayed()
    buttons.append(driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[2]/div[4]/div[3]/form/dl/div/button'))


price = 5000000051
count = 0

users = ['admintest1', 'admintest2', 'admintest3', 'admintest4']
browThreads = []

for user in users:
    browThread = threading.Thread(target=init_page_get_btn(user, price))
    browThreads.append(browThread)

for browThread in browThreads:
    browThread.start()

for browThread in browThreads:
    browThread.join()

for button in buttons:
    threading.Thread(target=click_button, args=(button,)).start()

