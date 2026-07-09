from dotenv import load_dotenv
from scraper import scrape_offers
import os
import requests


load_dotenv()
discordBotURL = os.getenv("DISCORD_BOT_URL")
numberNewOffers = scrape_offers().get("🏆most Recent 🏆", [])
print(f"Number of new offers: {len(numberNewOffers)}")

payload = {
    "content": f"{len(numberNewOffers)} New offer(s) are available! Check them out here: https://github.com/Lou162/vie-tracker",
}
response = requests.post(discordBotURL, json=payload)