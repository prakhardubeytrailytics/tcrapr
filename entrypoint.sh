#!/bin/bash
echo "🎬 Starting virtual display on :99"
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99

echo "🚀 Running scraper and server..."
python scrape_shop.py

wait
