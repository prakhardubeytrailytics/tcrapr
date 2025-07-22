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





# import asyncio
# import os
# import threading
# from playwright.async_api import async_playwright
# from http.server import SimpleHTTPRequestHandler
# import socketserver

# SELLER = "CiiN"
# SHOP_URL = f"https://www.tiktok.com/@{SELLER}/shop"
# OUTPUT_HTML = "shop_page.html"

# async def scrape_shop_data():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         context = await browser.new_context(
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
#         )
#         page = await context.new_page()

#         print(f"⏳ Visiting: {SHOP_URL}")
#         await page.goto(SHOP_URL, timeout=60000, wait_until="load")

#         print("⏳ Waiting for full load (including lazy-loaded products)...")
#         await page.wait_for_timeout(15000)

#         html = await page.content()

#         # 💥 PRINT entire HTML content to log
#         print("\n🧾 ====== FULL HTML CONTENT START ======\n")
#         print(html)
#         print("\n🧾 ====== FULL HTML CONTENT END ======\n")

#         # Save to file
#         with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
#             f.write(html)
#         print(f"💾 HTML saved as: {OUTPUT_HTML}")

#         await browser.close()


# def start_server():
#     port = int(os.environ.get("PORT", 8080))
#     os.chdir(".")
#     handler = SimpleHTTPRequestHandler
#     with socketserver.TCPServer(("", port), handler) as httpd:
#         print(f"🌐 Visit: http://localhost:{port}/")
#         print(f"📥 Download: [shop_page.html]")
#         httpd.serve_forever()


# if __name__ == "__main__":
#     threading.Thread(target=start_server, daemon=True).start()
#     asyncio.run(scrape_shop_data())





# import asyncio
# import os
# import threading
# import zipfile
# import json
# from http.server import SimpleHTTPRequestHandler
# import socketserver
# from playwright.async_api import async_playwright


# # TikTok shop URL (Vietnam region)
# TIKTOK_SHOP_URL = "https://www.tiktok.com/@luckystar.vnnn/shop"


# async def scrape_tiktok_shop():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         context = await browser.new_context(
#             locale="en-US",
#             user_agent=(
#                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                 "AppleWebKit/537.36 (KHTML, like Gecko) "
#                 "Chrome/114.0.0.0 Safari/537.36"
#             ),
#             geolocation={"latitude": 14.0583, "longitude": 108.2772},
#             permissions=["geolocation"]
#         )

#         page = await context.new_page()

#         print(f"⏳ Visiting: {TIKTOK_SHOP_URL}")
#         await page.goto(TIKTOK_SHOP_URL, timeout=60000, wait_until="load")

#         print("⏳ Waiting for dynamic shop content...")
#         await page.wait_for_timeout(5000)

#         print("🔄 Scrolling to load all products...")
#         for _ in range(20):
#             await page.mouse.wheel(0, 3000)
#             await page.wait_for_timeout(1500)

#         html_content = await page.content()

#         print("🔍 Extracting product data...")
#         products = await page.evaluate("""
#             () => {
#                 const items = [];
#                 const cards = document.querySelectorAll('[data-e2e="product-card"]');
#                 cards.forEach(card => {
#                     const title = card.querySelector('[data-e2e="product-card-name"]')?.innerText;
#                     const price = card.querySelector('[data-e2e="product-card-price"]')?.innerText;
#                     const link = card.querySelector('a')?.href;
#                     if (title && price && link) {
#                         items.push({ title, price, link });
#                     }
#                 });
#                 return items;
#             }
#         """)

#         print(f"🛍️ Found {len(products)} products.")
#         for i, p in enumerate(products[:10]):
#             print(f"{i+1}. {p['title']} - {p['price']} - {p['link']}")

#         # Save product data
#         with open("products.json", "w", encoding="utf-8") as f:
#             json.dump(products, f, ensure_ascii=False, indent=2)

#         await page.screenshot(path="shop_page.png", full_page=True)
#         with open("shop_page.html", "w", encoding="utf-8") as f:
#             f.write(html_content)

#         with zipfile.ZipFile("shop_data.zip", "w") as zipf:
#             zipf.write("products.json")
#             zipf.write("shop_page.html")
#             zipf.write("shop_page.png")

#         print("✅ Data saved: products.json, shop_page.html, shop_page.png, shop_data.zip")
#         await browser.close()


# def start_server():
#     port = int(os.environ.get("PORT", 8080))
#     os.chdir(".")
#     handler = SimpleHTTPRequestHandler
#     with socketserver.TCPServer(("", port), handler) as httpd:
#         print(f"\n🌐 Visit: http://localhost:{port}/")
#         print("📥 Download links:")
#         print(f"   ➤ http://localhost:{port}/products.json")
#         print(f"   ➤ http://localhost:{port}/shop_page.html")
#         print(f"   ➤ http://localhost:{port}/shop_page.png")
#         print(f"   ➤ http://localhost:{port}/shop_data.zip")
#         httpd.serve_forever()


# if __name__ == "__main__":
#     threading.Thread(target=start_server, daemon=True).start()
#     asyncio.run(scrape_tiktok_shop())


# import os
# import json
# import shutil
# import zipfile
# import asyncio
# from flask import Flask, send_from_directory
# from playwright.async_api import async_playwright

# # === Settings ===
# SHOP_URL = "https://www.tiktok.com/@luckystar.vnnn/shop"
# OUTPUT_DIR = "scraped_data"

# # === Scraper ===
# async def scrape_shop():
#     os.makedirs(OUTPUT_DIR, exist_ok=True)

#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         context = await browser.new_context(viewport={"width": 1280, "height": 800})
#         page = await context.new_page()

#         print(f"⏳ Visiting: {SHOP_URL}")
#         await page.goto(SHOP_URL, timeout=60000)

#         # Scroll to load products
#         print("🔄 Scrolling to load all products...")
#         prev_height = None
#         while True:
#             await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#             await asyncio.sleep(2)
#             curr_height = await page.evaluate("() => document.body.scrollHeight")
#             if curr_height == prev_height:
#                 break
#             prev_height = curr_height

#         print("🔍 Extracting product data...")
#         products = await page.evaluate("""
#             () => {
#                 const anchors = Array.from(document.querySelectorAll('a[href*="/product/"]'));
#                 const items = anchors.map(a => ({
#                     title: a.innerText.trim(),
#                     link: a.href
#                 })).filter(p => p.title && p.link);
#                 return Array.from(new Set(items.map(JSON.stringify))).map(JSON.parse); // remove duplicates
#             }
#         """)

#         print(f"🛍️ Found {len(products)} products.")

#         # Save JSON
#         json_path = os.path.join(OUTPUT_DIR, "products.json")
#         with open(json_path, "w", encoding="utf-8") as f:
#             json.dump(products, f, ensure_ascii=False, indent=2)

#         # Save HTML
#         html = await page.content()
#         with open(os.path.join(OUTPUT_DIR, "shop_page.html"), "w", encoding="utf-8") as f:
#             f.write(html)

#         # Save screenshot
#         await page.screenshot(path=os.path.join(OUTPUT_DIR, "shop_page.png"), full_page=True)

#         # Zip everything
#         zip_path = os.path.join(OUTPUT_DIR, "shop_data.zip")
#         with zipfile.ZipFile(zip_path, "w") as zipf:
#             for filename in ["products.json", "shop_page.html", "shop_page.png"]:
#                 zipf.write(os.path.join(OUTPUT_DIR, filename), filename)

#         await browser.close()

# # === Flask App ===
# app = Flask(__name__)

# @app.route('/')
# def index():
#     return f'''
#         <h2>📥 Download links:</h2>
#         <ul>
#             <li><a href="/products.json">products.json</a></li>
#             <li><a href="/shop_page.html">shop_page.html</a></li>
#             <li><a href="/shop_page.png">shop_page.png</a></li>
#             <li><a href="/shop_data.zip">shop_data.zip</a></li>
#         </ul>
#     '''

# @app.route('/<path:filename>')
# def download_file(filename):
#     return send_from_directory(OUTPUT_DIR, filename)

# # === Run everything ===
# if __name__ == "__main__":
#     print("🎬 Starting virtual display on :99")
#     print("🚀 Running TikTok scraper...\n")
#     asyncio.run(scrape_shop())
#     print("\n🌐 Visit: http://localhost:8080/")
#     app.run(host="0.0.0.0", port=8080)




import os, json, zipfile, asyncio
from flask import Flask, send_from_directory
from playwright.async_api import async_playwright
from playwright_stealth import stealth


SHOP_URL = os.getenv("SHOP_URL", "https://www.tiktok.com/@thienanshop193/shop")
OUTPUT_DIR = "scraped"

async def scrape_shop():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(args=[
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled"
        ], headless=True)
        context = await browser.new_context(
            locale="en-US",
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/114.0.0.0 Safari/537.36"),
            geolocation={"latitude": 14.0583, "longitude": 108.2772},
            permissions=["geolocation"],
            viewport={"width":1280,"height":800}
        )

        page = await context.new_page()
        await stealth(page)

        print(f"⏳ Visiting: {SHOP_URL}")
        await page.goto(SHOP_URL, timeout=60000, wait_until="load")

        print("🔄 Scrolling to load all products...")
        last = None
        while True:
            await page.mouse.wheel(0, 3000)
            await asyncio.sleep(2)
            height = await page.evaluate("() => document.body.scrollHeight")
            if height == last:
                break
            last = height

        print("🔍 Extracting product data...")
        products = await page.evaluate("""
            () => Array.from(
                new Set([...document.querySelectorAll('a[href*="/product/"]')]
                  .map(a => a.href))
            ).map(link => ({ link }));
        """)

        print(f"🛍️ Found {len(products)} products.")
        with open(os.path.join(OUTPUT_DIR, "products.json"), "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)

        content = await page.content()
        with open(os.path.join(OUTPUT_DIR, "shop_page.html"), "w", encoding="utf-8") as f:
            f.write(content)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "shop_page.png"), full_page=True)

        with zipfile.ZipFile(os.path.join(OUTPUT_DIR, "shop_data.zip"), "w") as z:
            for fn in ["products.json","shop_page.html","shop_page.png"]:
                z.write(os.path.join(OUTPUT_DIR, fn), fn)

        await browser.close()

app = Flask(__name__)

@app.route('/')
def index():
    files = ["products.json","shop_page.html","shop_page.png","shop_data.zip"]
    links = "".join([f'<li><a href="{name}">{name}</a></li>' for name in files])
    return f"<h2>Download links:</h2><ul>{links}</ul>"

@app.route('/<path:filename>')
def serve(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == "__main__":
    asyncio.run(scrape_shop())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
