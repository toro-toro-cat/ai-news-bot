from dotenv import load_dotenv
load_dotenv()

import os, feedparser, anthropic, requests
from datetime import datetime, timezone, timedelta

FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
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
        return "本日は新しいAIニュースが見つかりませんでした。"
    
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
            "content": f"""以下のAIニュースを読んで、日本語でデイリーレポートを作成してください。

形式：
1. 📌 **今日のハイライト**（3行以内で全体サマリー）
2. 🔥 **注目ニュース TOP3**（各ニュースを2〜3文で解説＋URLリンク）
3. 💡 **注目技術・トレンド**（キーワードを箇条書きで3〜5個）

---
{article_text}"""
        }]
    )
    return response.content[0].text

def post_to_discord(report):
    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]
    today = datetime.now(timezone(timedelta(hours=9))).strftime("%Y年%m月%d日")
    payload = {
        "content": f"## 🤖 AIニュース日次レポート｜{today}\n\n{report}"
    }
    requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    print("記事を収集中...")
    articles = fetch_recent_articles()
    print(f"{len(articles)}件の記事を取得")
    print("レポートを生成中...")
    report = generate_report(articles)
    print("Discordに投稿中...")
    post_to_discord(report)
    print("完了！")