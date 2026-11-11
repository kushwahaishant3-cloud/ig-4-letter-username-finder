# IG 4-Letter Username Finder

A beginner-friendly Python terminal application that generates unique usernames consisting of exactly four lowercase English letters (`a`–`z`).

**Generated usernames are candidates only; they are not confirmed to be available.** The app does not query Instagram or automate account creation or username checks. Verification is manual through Instagram's own interface.

## Instagram availability checks

Instagram does not provide an official, permitted API endpoint specifically for checking the availability of arbitrary usernames. This application therefore opens Instagram's sign-up page for you to check manually. It does not use private endpoints, scraping, session cookies, login automation, CAPTCHA bypass, proxies, or automated requests to Instagram. A saved result is your manual observation, not an official availability confirmation.

## Requirements

- Python 3.9 or newer
- No external packages

## Installation and running

Download the project as a ZIP from the green **Code** button on GitHub and extract it, or clone it with Git:

```bash
git clone https://github.com/kushwahaishant3-cloud/ig-4-letter-username-finder-app.git
cd ig-4-letter-username-finder-app
```

Windows (PowerShell):

```powershell
py main.py
```

Linux:

```bash
python3 main.py
```

Android Termux:

```bash
pkg install python
git clone https://github.com/kushwahaishant3-cloud/ig-4-letter-username-finder-app.git
cd ig-4-letter-username-finder-app
python main.py
```

## Usage

Choose an option from the menu:

1. **Generate usernames** — enter how many unique candidates to generate.
2. **Manually verify a username** — select a generated candidate, check it yourself in Instagram's sign-up interface, then record it as `Available`, `Taken`, or `Unknown`.
3. **Show generated usernames** — display generated candidates.
4. **Exit**

The review workflow skips usernames that already have a saved status. The app can generate at most 26⁴ (456,976) distinct usernames.

## Files created

- `usernames.txt` — generated usernames, one per line. Duplicates are avoided across runs.
- `verification_results.csv` — manual status and UTC timestamp for each reviewed username.

These data files are created beside the application the first time you use it, and are excluded from Git by `.gitignore`.
