#!/usr/bin/env bash
echo "🎬 Starting virtual display on :99"
Xvfb :99 -screen 0 1920x1080x24 &
echo "🚀 Running scraper..."
python scrape_shop.py
