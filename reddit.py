from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import random
from utils import random_sleep
import logging


def get_element(driver: webdriver.Remote, by: str, value: str) -> WebElement | None:
    try:
        random_sleep()  # Random sleep to mimic human behavior
        return driver.find_element(by, value)
    except Exception as e:
        logging.error(f"Error finding element by {by} with value '{value}': {e}")
        return None
    

def get_all_elements(driver: webdriver.Remote, by: str, value: str) -> list[WebElement]:
    try:
        random_sleep()  # Random sleep to mimic human behavior
        return driver.find_elements(by, value)
    except Exception as e:
        logging.error(f"Error finding elements by {by} with value '{value}': {e}")
        return []
    

def login_to_reddit(driver: webdriver.Remote, username: str, password: str) -> None:
    driver.get("https://reddit.com")
    login_button = get_element(driver, By.XPATH, "/html/body/shreddit-app/reddit-header-large/reddit-header-action-items/header/nav/div[3]/span[3]/faceplate-tracker/rpl-tooltip/a/span/span")
    if login_button:
        login_button.click()
        random_sleep()
        email_input = get_element(driver, By.NAME, "username")
        password_input = get_element(driver, By.NAME, "password")
        if email_input and password_input:
            email_input.send_keys(username)
            random_sleep()
            password_input.send_keys(password)
            random_sleep()
            login_submit = get_element(driver, By.XPATH, '//*[@id="login"]/auth-flow-modal/div[2]/faceplate-tracker/button')
            if login_submit:
                login_submit.click()
                random_sleep(2, 5)
            else:
                logging.error("Login submit button not found.")
        else:
            logging.error("Email or password input field not found.")
    else:
        logging.error("Login button not found.")    


def get_all_posts(driver: webdriver.Remote) -> list[WebElement]:
    return get_all_elements(driver, By.TAG_NAME, "shreddit-post")


def get_random_post(driver: webdriver.Remote) -> WebElement | None:
    posts = get_all_posts(driver)
    if posts:
        return random.choice(posts)
    else:
        logging.error("No posts found.")
        return None
    

def get_random_post_comments_greater_than(driver: webdriver.Remote, min_comments: int) -> WebElement | None:
    posts = get_all_posts(driver)
    # filtered_posts = [post for post in posts if int(post.get_attribute("comment-count")) > min_comments]
    filtered_posts = []
    for post in posts:
        try:
            comment_count_text = post.get_attribute("comment-count")
            if not comment_count_text:
                logging.warning(f"Post {post.get_attribute('post-title')} has no comment count attribute.")
                continue
            comment_count = int(comment_count_text)
            if comment_count > min_comments:
                filtered_posts.append(post)
        except (ValueError, TypeError):
            logging.error(f"Error converting comment count for post: {post.get_attribute('post-title')}")
    if filtered_posts:
        return random.choice(filtered_posts)
    else:
        logging.error(f"No posts found with more than {min_comments} comments.")
        return None