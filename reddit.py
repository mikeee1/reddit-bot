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
    login_button = get_element(driver, By.CLASS_NAME, "login-link")
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
    return get_all_elements(driver, By.CLASS_NAME, "thing")


def get_random_post(driver: webdriver.Remote) -> WebElement | None:
    posts = get_all_posts(driver)
    not_none_posts = [post for post in posts if post is not None]
    if not_none_posts:
        random_post = random.choice(not_none_posts)
        return random_post
    else:
        logging.error("No posts found.")
        return None
    

def get_random_post_comments_greater_than(driver: webdriver.Remote, min_comments: int) -> WebElement | None:
    posts = get_all_posts(driver)
    # filtered_posts = [post for post in posts if int(post.get_attribute("comment-count")) > min_comments]
    filtered_posts = []
    for post in posts:
        try:
            comment_count_text = post.get_attribute("data-comments-count")
            if not comment_count_text:
                logging.warning(f"Post {post.get_attribute('data-url')} has no comment count attribute.")
                continue
            comment_count = int(comment_count_text)
            if comment_count > min_comments:
                filtered_posts.append(post)
        except (ValueError, TypeError):
            logging.error(f"Error converting comment count for post: {post.get_attribute('data-url')}")
    if filtered_posts:
        return random.choice(filtered_posts)
    else:
        logging.error(f"No posts found with more than {min_comments} comments.")
        return None
    
def get_post_title(driver: webdriver.Remote) -> str:
    title_element = get_element(driver, By.CSS_SELECTOR, "a.title")
    logging.debug(f"Title element found: {title_element}")
    if title_element:
        return title_element.text.strip()
    else:
        logging.error("Title element not found in post.")
        return ""
    
def get_all_comments(driver: webdriver.Remote) -> list[WebElement]:
    comments = get_all_elements(driver, By.CSS_SELECTOR, "div.comment")
    if not comments:
        logging.error("No comments found.")
    return comments


def get_random_comments(driver: webdriver.Remote, count: int) -> list[str]:
    comments = get_all_comments(driver)
    if not comments:
        logging.error("No comments found to select from.")
        return []
    
    random_comments = random.sample(comments, min(count, len(comments)))
    comment_texts = []
    for comment in random_comments:
        text = comment.find_element(By.CSS_SELECTOR, "div.md").text.strip()
        if not text:
            logging.warning("Found an empty comment.")
            continue
        if text:
            comment_texts.append(text)
    if not comment_texts:
        logging.error("No valid comments found after filtering.")
        return []
    return comment_texts
    # return [comment.text.strip() for comment in random_comments if comment.text.strip()]


def get_post_tile_and_comments(driver: webdriver.Remote, count: int) -> tuple[str, list[str]]:
    post_title = get_post_title(driver)
    if not post_title:
        logging.error("Post title not found.")
        return ("", [])
    
    comments_text = get_random_comments(driver, count)
    if not comments_text:
        logging.error("No comments found to generate text from.")
        return ("", [])
    
    return (post_title, comments_text)
    

# def get_random_comments_text(driver: webdriver.Remote, count: int) -> list[str]:
#     comments = get_random_comments(driver, count)
#     if not comments:
#         logging.error("No comments found to generate text from.")
#         return []
    
#     return [comment for comment in comments if comment.text.strip()]
    