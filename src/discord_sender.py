"""Discord Webhook으로 메시지를 전송."""

from datetime import datetime, timezone, timedelta
import requests
from config import DISCORD_WEBHOOK_URL

KST = timezone(timedelta(hours=9))


def _post_webhook(payload):
    """Discord Webhook POST 공통 처리."""
    if not DISCORD_WEBHOOK_URL:
        print("[WARNING] DISCORD_WEBHOOK_URL이 설정되지 않았습니다.")
        return
    resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
    resp.raise_for_status()


def send_daily_summary(news_items, trending_repos):
    """일일 요약 메시지를 전송."""
    now = datetime.now(KST).strftime("%Y-%m-%d %H:%M KST")

    # --- 뉴스 Embed ---
    news_embeds = []
    if news_items:
        for i, item in enumerate(news_items[:10], 1):
            link = item["url"] or item["hn_url"]
            summary = item.get("summary", "")
            summary_block = f"\n\n{summary}" if summary else ""

            field_value = (
                f"[원문 보기]({link}) | [HN 댓글]({item['hn_url']})\n"
                f"Score: **{item['score']}**"
                f"{summary_block}"
            )

            news_embeds.append({
                "name": f"{i}. {item['title']}",
                "value": field_value,
                "inline": False,
            })
    else:
        news_embeds.append({
            "name": "No News",
            "value": "오늘은 주요 AI 뉴스가 없습니다.",
            "inline": False,
        })

    _post_webhook({
        "embeds": [{
            "title": "AI Daily Summary",
            "description": f"Hacker News AI 뉴스 요약 | {now}",
            "color": 0x3498DB,
            "fields": news_embeds,
            "footer": {"text": "Powered by Gemini + HN API"},
        }],
    })

    # --- GitHub Trending Embed ---
    repo_fields = []
    if trending_repos:
        for repo in trending_repos[:10]:
            desc = repo["description"][:100] + "..." if len(repo["description"]) > 100 else repo["description"]
            lang = f"`{repo['language']}`" if repo["language"] else ""
            stars = repo["stars_today"] if repo["stars_today"] else ""
            meta = " | ".join(filter(None, [lang, stars]))
            meta_line = f"\n{meta}" if meta else ""

            repo_fields.append({
                "name": repo["name"],
                "value": f"[GitHub]({repo['url']})\n{desc}{meta_line}",
                "inline": False,
            })
    else:
        repo_fields.append({
            "name": "No Trending",
            "value": "오늘은 AI 관련 트렌딩 레포가 없습니다.",
            "inline": False,
        })

    _post_webhook({
        "embeds": [{
            "title": "GitHub Trending - AI",
            "color": 0x2ECC71,
            "fields": repo_fields,
            "footer": {"text": "github.com/trending"},
        }],
    })


def send_breaking_alert(item):
    """긴급 뉴스 알림을 전송."""
    link = item["url"] or item["hn_url"]
    summary = item.get("summary", "")
    summary_block = f"\n\n{summary}" if summary else ""

    _post_webhook({
        "content": "@everyone",
        "embeds": [{
            "title": "Breaking AI News",
            "color": 0xE74C3C,
            "fields": [
                {
                    "name": item["title"],
                    "value": (
                        f"[원문 보기]({link}) | [HN 댓글]({item['hn_url']})\n"
                        f"Score: **{item['score']}**"
                        f"{summary_block}"
                    ),
                    "inline": False,
                },
            ],
            "footer": {"text": datetime.now(KST).strftime("%Y-%m-%d %H:%M KST")},
        }],
    })


def send_keyword_alert(item):
    """키워드 워치 알림을 전송."""
    link = item["url"] or item["hn_url"]
    keywords_str = ", ".join(f"`{kw}`" for kw in item["matched_keywords"])
    summary = item.get("summary", "")
    summary_block = f"\n\n{summary}" if summary else ""

    _post_webhook({
        "embeds": [{
            "title": "Keyword Alert",
            "color": 0xF39C12,
            "fields": [
                {
                    "name": item["title"],
                    "value": (
                        f"[원문 보기]({link}) | [HN 댓글]({item['hn_url']})\n"
                        f"Score: **{item['score']}** | Keywords: {keywords_str}"
                        f"{summary_block}"
                    ),
                    "inline": False,
                },
            ],
            "footer": {"text": datetime.now(KST).strftime("%Y-%m-%d %H:%M KST")},
        }],
    })
