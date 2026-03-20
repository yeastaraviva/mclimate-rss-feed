import requests
import hashlib
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

BASE_URL = "https://mclimate.eu"
BLOG_API = "https://mclimate.eu/blogs/blog/posts.json"


def fetch_posts():
    print("Fetching MClimate blog posts via Shopify API...")
    try:
        response = requests.get(
            BLOG_API,
            params={"limit": 50},
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()
        data = response.json()
        posts = data.get("articles", [])
        print(f"  ✓ Found {len(posts)} posts")
        return posts
    except Exception as e:
        print(f"  ✗ Error fetching posts: {e}")
        return []


def generate_feed(posts):
    fg = FeedGenerator()
    fg.title("MClimate Blog")
    fg.link(href=f"{BASE_URL}/bl
