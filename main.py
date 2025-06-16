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
import ai

BASE_URL = "https://old.reddit.com"

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
    ollama_url = os.getenv("ollama_url")
    if not url or not username or not password or not ollama_url:
        logging.error("Missing environment variables: url, reddit_username, reddit_password")
        return
    ollama_client = ai.get_ollama_client(ollama_url)
    driver = get_driver(url)
    try:
        driver.get(BASE_URL)
        reddit.login_to_reddit(driver, username, password)
        sleep(5)
        driver.get(f"{BASE_URL}/r/AskReddit/")
        post = reddit.get_random_post_comments_greater_than(driver, 100)
        if post:
            post_url = post.get_attribute("data-url")
            if post_url:
                if not post_url.startswith("http"):
                    post_url = f"{BASE_URL}{post_url}"
                logging.info(f"Found a post: {post.get_attribute('data-url')}")
                driver.get(post_url)
                sleep(2)
                comments = reddit.get_random_comments(driver, 10)
                if not comments:
                    logging.error("No comments found on the post.")
                    return
                logging.info(f"Found {len(comments)} comments on the post.")
                logging.info(f"Comments: {[comment for comment in comments]}")
                post_title, comments = reddit.get_post_tile_and_comments(driver, 10)
                sleep(1)
                if not post_title:
                    logging.error("Post title not found.")
                    return
                comment = ai.generate_comment(ollama_client, post_title, comments)
                logging.info(f"Generated comment: {comment}")

        else:
            logging.error("No posts found.")
        sleep(60)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        driver.quit()
    

if __name__ == '__main__':
    main()