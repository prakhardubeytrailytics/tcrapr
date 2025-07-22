# import asyncio
# from playwright.async_api import async_playwright
# import pandas as pd

# SELLER = "CiiN"
# SHOP_URL = f"https://www.tiktok.com/@{SELLER}/shop"

# async def scrape_shop_html():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(
#             headless=False,
#             args=["--no-sandbox", "--disable-setuid-sandbox"]
#         )
#         context = await browser.new_context(
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
#         )
#         page = await context.new_page()

#         print("⏳ Opening shop page...")
#         try:
#             response = await page.goto(SHOP_URL, timeout=60000, wait_until="load")
#             if not response or response.status != 200:
#                 print(f"❌ Failed to load shop page, status: {response.status if response else 'No Response'}")
#                 await browser.close()
#                 return
#         except Exception as e:
#             print(f"❌ Error navigating to shop page: {e}")
#             await browser.close()
#             return

#         print("⏳ Waiting 20s for CAPTCHA or full load...")
#         await page.wait_for_timeout(20000)

#         html = await page.content()
#         print("✅ Page HTML fetched.")

#         with open("shop_page.html", "w", encoding="utf-8") as f:
#             f.write(html)
#             print("💾 HTML saved to shop_page.html")

#         await browser.close()

# asyncio.run(scrape_shop_html())



import asyncio
from playwright.async_api import async_playwright
from http.server import SimpleHTTPRequestHandler
import socketserver
import threading
import os

SELLER = "CiiN"
SHOP_URL = f"https://www.tiktok.com/@{SELLER}/shop"
HTML_FILENAME = "shop_page.html"

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

        with open(HTML_FILENAME, "w", encoding="utf-8") as f:
            f.write(html)
            print(f"💾 HTML saved to {HTML_FILENAME}")

        await browser.close()

def start_server():
    port = int(os.environ.get("PORT", 8080))  # Railway exposes PORT env var
    handler = SimpleHTTPRequestHandler
    os.chdir(".")  # Serve current dir

    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🌐 Serving {HTML_FILENAME} at http://localhost:{port}/{HTML_FILENAME}")
        httpd.serve_forever()

if __name__ == "__main__":
    # Start web server in background
    threading.Thread(target=start_server, daemon=True).start()

    # Run scraper
    asyncio.run(scrape_shop_html())
