"""File storage helpers for generated usernames and manual verification results."""

import csv
from pathlib import Path
from typing import Dict, Set

DATA_DIR = Path(__file__).resolve().parent
USERNAMES_FILE = DATA_DIR / "usernames.txt"
VERIFICATIONS_FILE = DATA_DIR / "verification_results.csv"
VALID_STATUSES = {"Available", "Taken", "Unknown"}


def is_valid_username(username: str) -> bool:
    return len(username) == 4 and all("a" <= char <= "z" for char in username)


def load_generated_usernames() -> Set[str]:
    """Load valid usernames from the text file, ignoring duplicates."""
    if not USERNAMES_FILE.exists():
        return set()

    usernames: Set[str] = set()
    with USERNAMES_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            username = line.strip().lower()
            if is_valid_username(username):
                usernames.add(username)
    return usernames


def append_generated_usernames(usernames: list[str]) -> None:
    """Append valid generated usernames to the text file."""
    with USERNAMES_FILE.open("a", encoding="utf-8", newline="\n") as file:
        for username in usernames:
            if is_valid_username(username):
                file.write(username + "\n")


def load_verifications() -> Dict[str, dict[str, str]]:
    """Load saved manual results, keyed by username."""
    if not VERIFICATIONS_FILE.exists():
        return {}

    results: Dict[str, dict[str, str]] = {}
    with VERIFICATIONS_FILE.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            username = (row.get("username") or "").strip().lower()
            status = (row.get("status") or "").strip()
            checked_at = (row.get("checked_at") or "").strip()
            if is_valid_username(username) and status in VALID_STATUSES:
                results[username] = {"status": status, "checked_at": checked_at}
    return results


def save_verifications(results: Dict[str, dict[str, str]]) -> None:
    """Write verification results to CSV, replacing the file atomically."""
    temporary_file = VERIFICATIONS_FILE.with_suffix(".csv.tmp")
    with temporary_file.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["username", "status", "checked_at"])
        writer.writeheader()
        for username in sorted(results):
            record = results[username]
            writer.writerow({
                "username": username,
                "status": record["status"],
                "checked_at": record["checked_at"],
            })
    temporary_file.replace(VERIFICATIONS_FILE)
