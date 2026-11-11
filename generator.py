"""Generate unique random four-letter lowercase usernames."""

import random
import sys
from typing import Set

from storage import append_generated_usernames

TOTAL_COMBINATIONS = 26**4


def _number_to_username(number: int) -> str:
    """Convert a number in [0, 26**4) to a four-letter username."""
    letters = ["a"] * 4
    for position in range(3, -1, -1):
        number, remainder = divmod(number, 26)
        letters[position] = chr(ord("a") + remainder)
    return "".join(letters)


def _username_to_number(username: str) -> int:
    """Convert a valid four-letter username to its numeric representation."""
    number = 0
    for letter in username:
        number = number * 26 + ord(letter) - ord("a")
    return number


def generate_usernames(existing: Set[str], count: int) -> list[str]:
    """Generate and save `count` unique usernames absent from `existing`."""
    used_numbers = {
        _username_to_number(username)
        for username in existing
        if len(username) == 4 and all("a" <= letter <= "z" for letter in username)
    }
    available = [
        number for number in range(TOTAL_COMBINATIONS)
        if number not in used_numbers
    ]
    if count > len(available):
        raise ValueError("Requested count exceeds the number of unused usernames.")

    selected = random.sample(available, count)
    generated: list[str] = []
    progress_step = max(1, count // 100)

    for index, number in enumerate(selected, start=1):
        generated.append(_number_to_username(number))
        if index == count or index % progress_step == 0:
            percent = int(index * 100 / count)
            sys.stdout.write(f"\rGenerating: {percent:3d}% ({index:,}/{count:,})")
            sys.stdout.flush()

    print()
    append_generated_usernames(generated)
    return generated
