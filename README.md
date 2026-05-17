# AI News Bot

AIニュースを毎朝8時（JST）に自動収集・要約してDiscordへ送信するBot。

## 概要

TechCrunch / VentureBeat / The Verge のRSSフィードから過去24時間のAI関連記事を取得し、Claude（claude-sonnet-4-6）が日本語のデイリーレポートを生成。GitHub Actionsで毎朝自動実行される。

### レポートの構成

- 📌 **今日のハイライト** — 全体を3行以内でサマリー
- 🔥 **注目ニュース TOP3** — 各ニュースを2〜3文で解説＋URLリンク
- 💡 **注目技術・トレンド** — キーワードを箇条書きで3〜5個

## セットアップ

### 必要なもの

- Python 3.12+
- Anthropic APIキー
- Discord Webhook URL

### ローカルで実行する場合

```bash
pip install anthropic feedparser requests python-dotenv
```

`.env` ファイルを作成：

```
ANTHROPIC_API_KEY=your_api_key_here
DISCORD_WEBHOOK_URL=your_webhook_url_here
```

```bash
python ai_news_report.py
```

### GitHub Actionsで自動実行する場合

リポジトリの **Settings > Secrets and variables > Actions** に以下の2つを登録：

| Secret名 | 値 |
|---|---|
| `ANTHROPIC_API_KEY` | AnthropicのAPIキー |
| `DISCORD_WEBHOOK_URL` | DiscordのWebhook URL |

登録後、毎朝UTC 23:00（JST 08:00）に自動実行される。  
**Actions** タブの `AI News Daily Report` から手動実行も可能。

## ファイル構成

```
.
├── ai_news_report.py          # メインスクリプト
├── .github/workflows/
│   └── ai-news.yml            # GitHub Actions ワークフロー
├── .env                       # ローカル用の環境変数（git管理外）
└── .gitignore
```

## ニュースソース

| メディア | フィード |
|---|---|
| TechCrunch | `/category/artificial-intelligence/feed/` |
| VentureBeat | `/category/ai/feed/` |
| The Verge | `/rss/ai-artificial-intelligence/index.xml` |

ソースを変更・追加したい場合は `ai_news_report.py` の `FEEDS` リストを編集する。
