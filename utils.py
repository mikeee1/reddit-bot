from time import sleep
import random


def random_sleep(min_seconds: float = 0.2, max_seconds: float = 1.0) -> None:
    """Sleep for a random duration between min_seconds and max_seconds."""
    sleep(random.uniform(min_seconds, max_seconds))