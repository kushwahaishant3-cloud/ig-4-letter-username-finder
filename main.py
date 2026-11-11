"""Terminal interface for the IG 4-Letter Username Finder."""

from generator import generate_usernames
from storage import load_generated_usernames, load_verifications
from verification import manually_verify


def show_menu() -> None:
    print("\nIG 4-Letter Username Finder")
    print("-" * 30)
    print("1. Generate usernames")
    print("2. Manually verify a username")
    print("3. Show generated usernames")
    print("4. Exit")


def generate_menu() -> None:
    existing = load_generated_usernames()
    remaining = 26**4 - len(existing)

    if remaining <= 0:
        print("All possible 4-letter usernames have already been generated.")
        return

    print(f"\nAlready generated: {len(existing):,}")
    print(f"Unique candidates remaining: {remaining:,}")

    try:
        count = int(input("How many candidates should be generated? ").strip())
    except ValueError:
        print("Please enter a whole number.")
        return

    if count <= 0:
        print("Enter a number greater than zero.")
        return
    if count > remaining:
        print(f"There are only {remaining:,} unique candidates remaining.")
        return

    generated = generate_usernames(existing, count)
    print(f"Generated and saved {len(generated):,} usernames to usernames.txt.")


def show_generated_menu() -> None:
    usernames = sorted(load_generated_usernames())
    if not usernames:
        print("\nNo usernames generated yet.")
        return

    display_count = 50
    print(f"\nGenerated usernames: {len(usernames):,}")
    for username in usernames[-display_count:]:
        print(f"  {username}")
    if len(usernames) > display_count:
        print(f"  ... showing the latest {display_count} alphabetically.")


def main() -> None:
    while True:
        show_menu()
        choice = input("Choose an option (1-4): ").strip()

        try:
            if choice == "1":
                generate_menu()
            elif choice == "2":
                manually_verify(load_generated_usernames(), load_verifications())
            elif choice == "3":
                show_generated_menu()
            elif choice == "4":
                print("Goodbye.")
                break
            else:
                print("Choose 1, 2, 3, or 4.")
        except (OSError, UnicodeError) as error:
            print(f"File error: {error}")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")
