from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from dotenv import load_dotenv
import os
import random
from utils import random_sleep
import reddit
import logging


def get_driver(url: str) -> webdriver.Remote:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Remote(url, options=options)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            # logging.FileHandler("reddit_bot.log"),
            logging.StreamHandler()
        ]
    )


def main():
    load_dotenv()
    setup_logging()
    url = os.getenv("url")
    username = os.getenv("reddit_username")
    password = os.getenv("reddit_password")
    if not url or not username or not password:
        logging.error("Missing environment variables: url, reddit_username, reddit_password")
        return
    driver = get_driver(url)
    try:
        reddit.login_to_reddit(driver, username, password)
        sleep(500)
        driver.get("https://www.reddit.com/r/AskReddit/")
        post = reddit.get_random_post(driver)
        if post:
            # print(f"Found a post: {post.get_attribute('post-title')}")
            logging.info(f"Found a post: {post.get_attribute('post-title')}")
        else:
            logging.error("No posts found.")
        sleep(600)
        print("Login successful!")
    except Exception as e:
        print(f"An error occurred during login: {e}")
    finally:
        driver.quit()
    

if __name__ == '__main__':
    main()