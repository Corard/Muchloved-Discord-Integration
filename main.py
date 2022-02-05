import selenium
import traceback
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from discord_webhook import DiscordWebhook, DiscordEmbed
import time


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36')
options.add_argument('--log-level=3')

driver = webdriver.Chrome(options=options)

DONATION_URL = ""
WEBHOOK_URL = ""

webhook = DiscordWebhook(url=WEBHOOK_URL)


while True:
    time.sleep(5)
    try:
        driver.get(url)
        latest_url = driver.find_element(By.CSS_SELECTOR, "a.text-dark").get_attribute("href")


        with open('latest.txt') as f:
            recent = f.read()
        
        if latest_url == recent:
            pass

        else:
            try:
                driver.get(latest_url)
                try:
                    name = driver.find_element(By.CSS_SELECTOR, "span.d-inline-block.text-break").text
                except selenium.common.exceptions.NoSuchElementException:
                    name = "Name Hidden"
                try:
                    message = driver.find_element(By.CSS_SELECTOR, "p.font-weight-light.pre-wrap.break-word").text
                except selenium.common.exceptions.NoSuchElementException:
                    message = "No Message Was Attached"
                try:
                    amount = driver.find_element(By.CSS_SELECTOR, "span.donation-amount").text
                except selenium.common.exceptions.NoSuchElementException:
                    amount = "Amount Hidden"

                #print(f"{name}\n{message}\n{amount}")
                embed = DiscordEmbed(title=f"{name} has donated {amount}", description=f"{message}", color="ffffff")
                embed.set_author(name="New Donation")
                embed.add_embed_field(name="‎", value=f"[Make a Donation Here]({DONATION_URL})")
                webhook.add_embed(embed)
                try:
                    response = webhook.execute()
                except Exception as e:
                    print(f"> {e}")
                    traceback.print_exc()
            except Exception as e:
                print(f">> {e}")
                traceback.print_exc()
            with open('latest.txt', 'w') as w:
                w.write(latest_url)

    except Exception as e:
        print(f">>> {e}")
        traceback.print_exc()
