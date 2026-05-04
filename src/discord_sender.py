"""Discord Webhook으로 메시지를 전송."""

import requests
from config import DISCORD_WEBHOOK_URL


def send_embed(title, description, color=0x3498DB, fields=None):
    """Discord Embed 메시지를 전송.

    Args:
        title: Embed 제목
        description: Embed 본문
        color: 색상 코드 (기본: 파란색)
        fields: [{"name": ..., "value": ..., "inline": bool}, ...]
    """
    if not DISCORD_WEBHOOK_URL:
        print("[WARNING] DISCORD_WEBHOOK_URL이 설정되지 않았습니다.")
        return

    embed = {
        "title": title,
        "description": description,
        "color": color,
    }
    if fields:
        embed["fields"] = fields

    payload = {"embeds": [embed]}
    resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
    resp.raise_for_status()


def send_daily_summary(news_items, trending_repos):
    """일일 요약 메시지를 전송."""
    # 뉴스 섹션
    if news_items:
        news_lines = []
        for item in news_items[:15]:
            link = item["url"] or item["hn_url"]
            news_lines.append(
                f"**[{item['title']}]({link})**\n"
                f"  Score: {item['score']} | [HN 댓글]({item['hn_url']})"
            )
        news_text = "\n\n".join(news_lines)
    else:
        news_text = "오늘은 주요 AI 뉴스가 없습니다."

    # GitHub 섹션
    if trending_repos:
        repo_lines = []
        for repo in trending_repos[:10]:
            desc = repo["description"][:80] + "..." if len(repo["description"]) > 80 else repo["description"]
            lang = f" `{repo['language']}`" if repo["language"] else ""
            stars = f" | {repo['stars_today']}" if repo["stars_today"] else ""
            repo_lines.append(
                f"**[{repo['name']}]({repo['url']})**{lang}{stars}\n"
                f"  {desc}"
            )
        repo_text = "\n\n".join(repo_lines)
    else:
        repo_text = "오늘은 AI 관련 트렌딩 레포가 없습니다."

    send_embed(
        title="AI Daily Summary",
        description=f"## Hacker News - AI\n{news_text}",
        color=0x3498DB,
    )
    send_embed(
        title="GitHub Trending - AI",
        description=repo_text,
        color=0x2ECC71,
    )


def send_breaking_alert(item):
    """긴급 뉴스 알림을 전송."""
    if not DISCORD_WEBHOOK_URL:
        print("[WARNING] DISCORD_WEBHOOK_URL이 설정되지 않았습니다.")
        return

    link = item["url"] or item["hn_url"]
    description = (
        f"**[{item['title']}]({link})**\n\n"
        f"Score: {item['score']} | [HN 댓글]({item['hn_url']})"
    )

    payload = {
        "content": "@everyone",
        "embeds": [{
            "title": "Breaking AI News",
            "description": description,
            "color": 0xE74C3C,  # 빨간색
        }],
    }
    resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
    resp.raise_for_status()
