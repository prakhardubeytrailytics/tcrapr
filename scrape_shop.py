import asyncio
from playwright.async_api import async_playwright
import pandas as pd

SELLER = "CiiN"
SHOP_URL = f"https://www.tiktok.com/@{SELLER}/shop"

async def scrape_shop_html():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print("⏳ Opening shop page...")
        try:
            response = await page.goto(SHOP_URL, timeout=60000, wait_until="load")
            if not response or response.status != 200:
                print(f"❌ Failed to load shop page, status: {response.status if response else 'No Response'}")
                await browser.close()
                return
        except Exception as e:
            print(f"❌ Error navigating to shop page: {e}")
            await browser.close()
            return

        print("⏳ Waiting 20s for CAPTCHA or full load...")
        await page.wait_for_timeout(20000)

        html = await page.content()
        print("✅ Page HTML fetched.")

        with open("shop_page.html", "w", encoding="utf-8") as f:
            f.write(html)
            print("💾 HTML saved to shop_page.html")

        await browser.close()

asyncio.run(scrape_shop_html())
