import requests
import hashlib
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

BASE_URL = "https://mclimate.eu"
BLOG_API = "https://mclimate.eu/blogs/blog/posts.json"


def fetch_posts():
    """
    MClimate runs on Shopify which exposes a built-in JSON API for blog posts.
    This is more reliable than scraping HTML — no CSS selectors to break.
    Fetches up to 50 most recent posts.
    """
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
    fg.link(href=f"{BASE_URL}/blogs/blog", rel="alternate")
    fg.description("Latest posts from the MClimate blog")
    fg.language("en")

    for post in posts:
        title = post.get("title", "Untitled")
        handle = post.get("handle", "")
        link = f"{BASE_URL}/blogs/blog/{handle}"
        summary = post.get("summary_html") or post.get("body_html", "")
        published_at = post.get("published_at", "")
        author = post.get("author", "MClimate")
        tags = post.get("tags", "")

        # Parse publish date if available
        try:
            pub_date = parsedate_to_datetime(published_at) if published_at else datetime.now(timezone.utc)
        except Exception:
            pub_date = datetime.now(timezone.utc)

        fe = fg.add_entry()
        fe.title(f"[Blog] {title}")
        fe.link(href=link)
        fe.description(summary[:500] if summary else "")
        fe.author({"name": author})
        fe.id(hashlib.md5(link.encode()).hexdigest())
        fe.published(pub_date)

        if tags:
            for tag in (tags if isinstance(tags, list) else tags.split(",")):
                fe.category({"term": tag.strip()})

    fg.rss_file("feed.xml")
    print("✓ feed.xml generated successfully.")


if __name__ == "__main__":
    posts = fetch_posts()
    if posts:
        generate_feed(posts)
    else:
        print("No posts found — feed not updated.")
