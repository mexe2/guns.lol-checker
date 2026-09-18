import random
import string
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "https://guns.lol/register?ref=header"
OUTPUT_FILE = Path("successful-guns.lol.txt")

CHARS = string.ascii_lowercase + string.digits + "._"


def generate_username():
    return "".join(random.choices(CHARS, k=4))


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(URL)
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    field = page.locator(
        'input[name="username"], '
        'input[placeholder*="Username" i], '
        'input[placeholder*="username" i]'
    ).first

    field.wait_for(state="visible")

    while True:
        username = generate_username()
        print(f"\ngenerated: {username}")

        field.fill(username)

        answer = input(
            "ENTER = save | "
            "n = next | "
            "q = quit: "
        ).lower()

        if answer == "q":
            break

        if answer == "":
            with OUTPUT_FILE.open("a", encoding="utf-8") as f:
                f.write(username + "\n")

            print(f"saved: {username}")

    browser.close()

print(f"\ncompleted. successful names are in: {OUTPUT_FILE}")
