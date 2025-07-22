# # import asyncio
# # from playwright.async_api import async_playwright
# # import pandas as pd

# # SELLER = "CiiN"
# # SHOP_URL = f"https://www.tiktok.com/@{SELLER}/shop"

# # async def scrape_shop_html():
# #     async with async_playwright() as p:
# #         browser = await p.chromium.launch(
# #             headless=False,
# #             args=["--no-sandbox", "--disable-setuid-sandbox"]
# #         )
# #         context = await browser.new_context(
# #             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
# #         )
# #         page = await context.new_page()

# #         print("⏳ Opening shop page...")
# #         try:
# #             response = await page.goto(SHOP_URL, timeout=60000, wait_until="load")
# #             if not response or response.status != 200:
# #                 print(f"❌ Failed to load shop page, status: {response.status if response else 'No Response'}")
# #                 await browser.close()
# #                 return
# #         except Exception as e:
# #             print(f"❌ Error navigating to shop page: {e}")
# #             await browser.close()
# #             return

# #         print("⏳ Waiting 20s for CAPTCHA or full load...")
# #         await page.wait_for_timeout(20000)

# #         html = await page.content()
# #         print("✅ Page HTML fetched.")

# #         with open("shop_page.html", "w", encoding="utf-8") as f:
# #             f.write(html)
# #             print("💾 HTML saved to shop_page.html")

# #         await browser.close()

# # asyncio.run(scrape_shop_html())



# import asyncio
# from playwright.async_api import async_playwright
# from http.server import SimpleHTTPRequestHandler
# import socketserver
# import threading
# import os

# SELLER = "CiiN"
# SHOP_URL = f"https://www.tiktok.com/@{SELLER}/shop"
# HTML_FILENAME = "shop_page.html"

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

#         with open(HTML_FILENAME, "w", encoding="utf-8") as f:
#             f.write(html)
#             print(f"💾 HTML saved to {HTML_FILENAME}")

#         await browser.close()

# def start_server():
#     port = int(os.environ.get("PORT", 8080))  # Railway exposes PORT env var
#     handler = SimpleHTTPRequestHandler
#     os.chdir(".")  # Serve current dir

#     with socketserver.TCPServer(("", port), handler) as httpd:
#         print(f"🌐 Serving {HTML_FILENAME} at http://localhost:{port}/{HTML_FILENAME}")
#         httpd.serve_forever()

# if __name__ == "__main__":
#     # Start web server in background
#     threading.Thread(target=start_server, daemon=True).start()

#     # Run scraper
#     asyncio.run(scrape_shop_html())




# import asyncio
# import json
# import csv
# import os
# import threading
# from playwright.async_api import async_playwright
# from http.server import SimpleHTTPRequestHandler
# import socketserver

# SELLER = "CiiN"
# SHOP_URL = f"https://www.tiktok.com/@{SELLER}/shop"
# OUTPUT_HTML = "shop_page.html"
# OUTPUT_JSON = "products.json"
# OUTPUT_CSV = "products.csv"

# async def scrape_shop_data():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)  # headless for automation
#         context = await browser.new_context(
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
#         )
#         page = await context.new_page()

#         print(f"⏳ Visiting: {SHOP_URL}")
#         await page.goto(SHOP_URL, timeout=60000, wait_until="load")

#         print("⏳ Waiting for full load (including lazy-loaded products)...")
#         await page.wait_for_timeout(15000)  # wait for JS-based loading

#         html = await page.content()
#         with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
#             f.write(html)
#         print(f"💾 HTML saved as: {OUTPUT_HTML}")

#         # Auto-extract products from JS objects in page
#         print("🔍 Extracting products...")
#         products = await page.evaluate("""
#             () => {
#                 const data = [];
#                 const items = document.querySelectorAll('[data-e2e="product-list-item"]');

#                 for (const item of items) {
#                     const name = item.querySelector('[data-e2e="product-item-name"]')?.textContent?.trim();
#                     const price = item.querySelector('[data-e2e="product-item-price"]')?.textContent?.trim();
#                     const link = item.querySelector('a')?.href;
#                     const img = item.querySelector('img')?.src;

#                     if (name && price && link) {
#                         data.push({ name, price, link, img });
#                     }
#                 }
#                 return data;
#             }
#         """)

#         print(f"✅ {len(products)} products found.")

#         # Save as JSON
#         with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
#             json.dump(products, f, indent=2, ensure_ascii=False)
#             print(f"📁 Saved products to {OUTPUT_JSON}")

#         # Save as CSV
#         with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=["name", "price", "link", "img"])
#             writer.writeheader()
#             writer.writerows(products)
#             print(f"📁 Saved products to {OUTPUT_CSV}")

#         await browser.close()


# def start_server():
#     port = int(os.environ.get("PORT", 8080))
#     os.chdir(".")
#     handler = SimpleHTTPRequestHandler
#     with socketserver.TCPServer(("", port), handler) as httpd:
#         print(f"🌐 Visit: http://localhost:{port}/")
#         print(f"📥 Download: [shop_page.html, products.json, products.csv]")
#         httpd.serve_forever()


# if __name__ == "__main__":
#     threading.Thread(target=start_server, daemon=True).start()
#     asyncio.run(scrape_shop_data())





import asyncio
import os
import threading
from playwright.async_api import async_playwright
from http.server import SimpleHTTPRequestHandler
import socketserver

SELLER = "CiiN"
SHOP_URL = f"https://www.tiktok.com/@{SELLER}/shop"
OUTPUT_HTML = "shop_page.html"

async def scrape_shop_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print(f"⏳ Visiting: {SHOP_URL}")
        await page.goto(SHOP_URL, timeout=60000, wait_until="load")

        print("⏳ Waiting for full load (including lazy-loaded products)...")
        await page.wait_for_timeout(15000)

        html = await page.content()

        # 💥 PRINT entire HTML content to log
        print("\n🧾 ====== FULL HTML CONTENT START ======\n")
        print(html)
        print("\n🧾 ====== FULL HTML CONTENT END ======\n")

        # Save to file
        with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"💾 HTML saved as: {OUTPUT_HTML}")

        await browser.close()


def start_server():
    port = int(os.environ.get("PORT", 8080))
    os.chdir(".")
    handler = SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🌐 Visit: http://localhost:{port}/")
        print(f"📥 Download: [shop_page.html]")
        httpd.serve_forever()


if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    asyncio.run(scrape_shop_data())
