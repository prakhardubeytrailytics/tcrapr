#!/bin/bash

# Start virtual display
echo "🎬 Starting virtual display on :99"
Xvfb :99 -screen 0 1920x1080x24 &

# Run Python script
echo "🚀 Running TikTok scraper..."
python scrape_shop.py
