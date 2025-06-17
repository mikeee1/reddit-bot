from time import sleep
import random


def random_sleep(min_seconds: float = 0.2, max_seconds: float = 1.0) -> None:
    """Sleep for a random duration between min_seconds and max_seconds."""
    sleep(random.uniform(min_seconds, max_seconds))


def check_comment(comment: str) -> bool:
    """Ask the user to confirm the comment."""
    print(f"Generated comment: {comment}")
    confirmation = input("Is this comment okay? (y/n): ").strip().lower()
    return confirmation == "y"