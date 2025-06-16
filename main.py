from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from dotenv import load_dotenv
import os
import random
from utils import random_sleep
import reddit


def get_driver(url: str) -> webdriver.Remote:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Remote(url, options=options)


def main():
    load_dotenv()
    url = os.getenv("url")
    username = os.getenv("reddit_username")
    password = os.getenv("reddit_password")
    if not url or not username or not password:
        print("Please set the environment variables: url, username, password")
        return
    driver = get_driver(url)
    try:
        reddit.login_to_reddit(driver, username, password)
        sleep(60)
        print("Login successful!")
    except Exception as e:
        print(f"An error occurred during login: {e}")
    finally:
        driver.quit()
    

if __name__ == '__main__':
    main()