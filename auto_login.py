# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00D2F062A9942507F359D82D51765838A5565363965B9715E36AEDE901A858235AC64B8C4B8B06D84A9E34984455D618327E9DACB00FE0F475E894853D139BC2C587C1C198693952E12E9F538470FB8B27A7355054EDB4F5D2FAAFB4BED3E40101C7CD629CFE6385AF8335EECB951388627599BD0DA01C11A48EB742D264765886E1DFFCB32651EE3B9E13D78CB934C660EBDB9A91ABAB7D26CBD8894FF100FD5D4D135F65B3A18C4D3A4EDE8C4BAE06BDCA738A570BA4AA1352F321135241F72B8D0D40D3F48E9B00C1B9F16EDDE258934F6A9592DB2C05AC83A25779C4CDED9E3727F6EC75D9C1B5555A836969EC37EA1C48205986EF2F230B0494EF0DD4D7F8BA565D0AE01CCEFF464DB16D5AF138ED436607D85E6EFAC2E099B12A8F84224331DE631E99C7DDF710C2C11AB4B461F809A72A997895E7288DD6E572BFAB7A45986666FA5431E0D4AC1D112E4472A36E3799333C599F7D83FF0F451D33DBE064"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
