from dotenv import load_dotenv
load_dotenv()

import os, feedparser, anthropic, requests
from datetime import datetime, timezone, timedelta

FEEDS = [
    # English — AI & Tech
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://techcrunch.com/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    # English — Business & Economy
    "https://feeds.reuters.com/reuters/businessNews",
    "https://feeds.bbci.co.uk/news/business/rss.xml",
    # Japanese — Tech
    "https://rss.itmedia.co.jp/rss/2.0/news_bursts.xml",
    "https://rss.itmedia.co.jp/rss/2.0/ait.xml",
    "https://gigazine.net/news/rss_2.0/",
    "https://ascii.jp/rss.xml",
    # Japanese — General / Science & Tech (NHK, free)
    "https://www3.nhk.or.jp/rss/news/cat4.xml",
]

def fetch_recent_articles(hours=24):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    articles = []
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            published = entry.get("published_parsed")
            if published:
                pub_dt = datetime(*published[:6], tzinfo=timezone.utc)
                if pub_dt >= cutoff:
                    articles.append({
                        "title": entry.get("title", ""),
                        "summary": entry.get("summary", "")[:300],
                        "link": entry.get("link", ""),
                        "source": feed.feed.get("title", "Unknown"),
                    })
    return articles

def generate_report(articles):
    if not articles:
        return "本日は新しいニュースが見つかりませんでした。"

    article_text = "\n\n".join([
        f"【{a['source']}】{a['title']}\n{a['summary']}\nURL: {a['link']}"
        for a in articles
    ])

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": f"""以下のニュース記事（AI・テック・ビジネス分野、英語・日本語混在）を読んで、日本語でデイリーレポートを作成してください。

形式：
1. 📌 **今日のハイライト**（3行以内で全体サマリー）
2. 🤖 **AI・テックニュース TOP3**（各2〜3文で解説＋URLリンク）
3. 💼 **ビジネス・経済ニュース TOP3**（各2〜3文で解説＋URLリンク）
4. 🇯🇵 **日本のニュース TOP3**（ITmedia・Gigazine・ASCII・NHKなど日本語ソースから選出、各2〜3文で解説＋URLリンク）
5. 💡 **注目トレンド・キーワード**（箇条書きで3〜5個）

---
{article_text}"""
        }]
    )
    return response.content[0].text

DISCORD_LIMIT = 1900

def post_to_discord(report):
    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]
    today = datetime.now(timezone(timedelta(hours=9))).strftime("%Y年%m月%d日")
    full_message = f"## 📰 デイリーニュースレポート｜{today}\n\n{report}"

    chunks = []
    while len(full_message) > DISCORD_LIMIT:
        split_at = full_message.rfind("\n", 0, DISCORD_LIMIT)
        if split_at == -1:
            split_at = DISCORD_LIMIT
        chunks.append(full_message[:split_at])
        full_message = full_message[split_at:].lstrip()
    chunks.append(full_message)

    for chunk in chunks:
        requests.post(webhook_url, json={"content": chunk})

if __name__ == "__main__":
    print("記事を収集中...")
    articles = fetch_recent_articles()
    print(f"{len(articles)}件の記事を取得")
    print("レポートを生成中...")
    report = generate_report(articles)
    print("Discordに投稿中...")
    post_to_discord(report)
    print("完了！")
