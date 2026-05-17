# AI News Bot

AIニュースを毎朝8時（JST）に自動収集・要約してDiscordへ送信するBot。

## 概要

TechCrunch / VentureBeat / The Verge のRSSフィードから過去24時間のAI関連記事を取得し、Claude（claude-sonnet-4-6）が日本語のデイリーレポートを生成。GitHub Actionsで毎朝自動実行される。

### レポートの構成

- 📌 **今日のハイライト** — 全体を3行以内でサマリー
- 🤖 **AI・テックニュース TOP3** — 各2〜3文で解説＋URLリンク
- 💼 **ビジネス・経済ニュース TOP3** — 各2〜3文で解説＋URLリンク
- 🇯🇵 **日本のニュース TOP3** — 日本語ソースから選出、各2〜3文で解説＋URLリンク
- 📚 **資格・学習・キャリア** — IT資格・勉強会・20代後半〜30代前半向け転職情報（情報があれば）
- 💡 **注目トレンド・キーワード** — キーワードを箇条書きで3〜5個

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

### 英語（AI・テック）
| メディア | 内容 |
|---|---|
| TechCrunch | AI特化 + 全般 |
| VentureBeat | AI・機械学習 |
| The Verge | テック全般 |
| Wired | テック・カルチャー |

### 英語（ビジネス・経済）
| メディア | 内容 |
|---|---|
| Reuters | ビジネスニュース（無料） |
| BBC Business | ビジネスニュース（無料） |

### 日本語
| メディア | 内容 |
|---|---|
| ITmedia News | IT・テック全般（無料） |
| ITmedia AI+ | AI特化（無料） |
| Gigazine | テック・サイエンス（無料） |
| ASCII.jp | テック・ガジェット（無料） |
| NHK 科学・文化 | 科学技術ニュース（無料） |

### 資格・学習・キャリア
| メディア | 内容 |
|---|---|
| connpass | IT勉強会・イベント（無料） |
| IPA | 情報処理技術者試験の最新情報（無料） |
| レバテックキャリア | IT転職・キャリア情報（無料） |

> 有料記事が多い日経などは除外しています。ソースを変更・追加したい場合は `ai_news_report.py` の `FEEDS` リストを編集してください。
