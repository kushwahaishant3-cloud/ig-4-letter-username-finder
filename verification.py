"""Manual-only username verification workflow."""

from datetime import datetime, timezone
import webbrowser
from typing import Dict, Set

from storage import VALID_STATUSES, is_valid_username, save_verifications

INSTAGRAM_SIGNUP_URL = "https://www.instagram.com/accounts/emailsignup/"


def manually_verify(
    generated_usernames: Set[str],
    results: Dict[str, dict[str, str]],
) -> None:
    if not generated_usernames:
        print("\nGenerate some usernames first.")
        return

    pending = sorted(generated_usernames - set(results))
    if not pending:
        print("\nEvery generated username already has a saved status.")
        return

    print("\nManual verification")
    print("Generated usernames are not confirmed available.")
    print(f"Unreviewed candidates: {len(pending):,}")
    username = input("Enter a generated username to review (or press Enter to cancel): ")
    username = username.strip().lower()

    if not username:
        return
    if not is_valid_username(username) or username not in generated_usernames:
        print("That is not a valid username from usernames.txt.")
        return
    if username in results:
        print(f"{username} already has a saved status: {results[username]['status']}.")
        return

    print("\nInstagram's sign-up page will open in your browser.")
    print("Check the username yourself in Instagram's interface; this app does not")
    print("submit forms, make availability requests, or automate Instagram.")
    try:
        opened = webbrowser.open(INSTAGRAM_SIGNUP_URL)
        if not opened:
            print(f"Could not open a browser automatically. Visit: {INSTAGRAM_SIGNUP_URL}")
    except webbrowser.Error as error:
        print(f"Could not open a browser: {error}")
        print(f"Open this address manually: {INSTAGRAM_SIGNUP_URL}")

    print("\nAfter checking manually, choose a status:")
    print("A. Available")
    print("T. Taken")
    print("U. Unknown / could not determine")
    selection = input("Status (A/T/U): ").strip().lower()
    status_by_choice = {"a": "Available", "t": "Taken", "u": "Unknown"}
    status = status_by_choice.get(selection)

    if status not in VALID_STATUSES:
        print("Invalid selection. No result was saved.")
        return

    results[username] = {
        "status": status,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    save_verifications(results)
    print(f"Saved {username}: {status} to verification_results.csv.")
