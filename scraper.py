def fetch_posts():
    print("Fetching MClimate blog posts via Shopify API...")
    try:
        response = requests.get(
            BLOG_API,
            params={"limit": 50},
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        print(f"  Status code: {response.status_code}")
        print(f"  Response preview: {response.text[:500]}")
        response.raise_for_status()
        data = response.json()
        posts = data.get("articles", [])
        print(f"  ✓ Found {len(posts)} posts")
        return posts
    except Exception as e:
        print(f"  ✗ Error fetching posts: {e}")
        return []
