from contextlib import contextmanager
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, visibility_of, staleness_of
import time
import pyttsx3
import zipfile
import glob
import os
import json

with open('config/microsoft_config.json') as f:
    config = json.load(f)

speakengine = pyttsx3.init()

def say(message: str, repeat: int=1) -> None:
    for i in range(repeat):
        speakengine.say(message)
        speakengine.runAndWait()

def spawn_browser() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    return webdriver.Chrome(options=options)

@contextmanager
def wait_for_page_load(driver: webdriver.Chrome, timeout: int=30):
    old_page = driver.find_element_by_tag_name('html')
    yield
    WebDriverWait(driver, timeout).until(
        staleness_of(old_page)
    )

def wait_for_presence_of_element_by_css_selector(driver: webdriver.Chrome, selector: str, timeout: int=15):
    try:
        element = WebDriverWait(driver, timeout).until(
            presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        return element
    except WebDriverException as e:
        driver.quit()

def wait_for_visibility_of_element(driver, element, timeout=15):
    try:
        element = WebDriverWait(driver, timeout).until(
            visibility_of(element)
        )
        return element
    except WebDriverException as e:
        breakpoint()
        driver.quit()

driver = spawn_browser()
driver.get('https://www.microsoft.com/store/onerf/signin?EEL=False&pcexp=True&ru=https%3A%2F%2Fwww.microsoft.com%2Fen-US%2Fstore%2Fcart')
# driver.get('https://www.microsoft.com/en-US/store/buy/checkout')
# wait_for_presence_of_element_by_css_selector(driver, '#mectrl_main_trigger').click()
time.sleep(2)
username_element = wait_for_presence_of_element_by_css_selector(driver, "input[name='loginfmt']")
wait_for_visibility_of_element(driver, username_element)
# username_element = driver.find_element_by_css_selector("input[name='loginfmt']")
username_element.send_keys(config['username'])
driver.find_element_by_css_selector("input[type='submit']").click()
time.sleep(2)
password_element = wait_for_presence_of_element_by_css_selector(driver, "input[name='passwd']")
wait_for_visibility_of_element(driver, password_element)
password_element.send_keys(config['password'])
driver.find_element_by_css_selector("input[name='KMSI']").click()
driver.find_element_by_css_selector("input[type='submit']").click()
time.sleep(2)
driver.find_element_by_xpath("//*[@id='store-cart-root']/div/div/div/section[2]/div/div/button").click()
time.sleep(5)
placeOrderFn = f"""
setInterval(function(){{document.getElementsByClassName("btn theme-default btn-primary cli-purchase ember-view")[0].click()}}, {config['retryInterval']});
"""
driver.execute_script(placeOrderFn)

while True:
    time.sleep(15)
    try:
        password_element = driver.find_element_by_css_selector("input[name='passwd']")
        wait_for_visibility_of_element(driver, password_element)
        password_element.send_keys(config['password'])
        driver.find_element_by_css_selector("input[type='submit']").click()
        time.sleep(5)
        driver.execute_script(placeOrderFn)
    except WebDriverException as e:
        pass

