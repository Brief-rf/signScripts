import os

from playwright.sync_api import sync_playwright
from textnow.textnow_sms import TextNowBot


def run(playwright):
    username = os.environ["TEXTNOW_USERNAME"]
    password = os.environ["TEXTNOW_PASSWORD"]
    recipient = os.environ["TEXTNOW_RECIPIENT"]
    message = os.environ["TEXTNOW_MESSAGE"]

    browser = None

    try:
        browser = playwright.firefox.launch()
        page = browser.new_page()

        bot = TextNowBot(page)

        bot.log_in(None, username, password)
        bot.send_text_message(recipient, message)

        browser.close()
    except Exception:
        if browser:
            browser.close()

        raise


with sync_playwright() as playwright:
    run(playwright)
