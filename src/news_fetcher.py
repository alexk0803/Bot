"""Hacker News API에서 AI 관련 뉴스를 수집."""

import re
import requests
from config import AI_KEYWORDS, HN_MIN_SCORE_DAILY

HN_API = "https://hacker-news.firebaseio.com/v0"


def fetch_top_story_ids(limit=100):
    """HN Top Stories ID 목록을 가져온다."""
    resp = requests.get(f"{HN_API}/topstories.json", timeout=10)
    resp.raise_for_status()
    return resp.json()[:limit]


def fetch_item(item_id):
    """HN 아이템 상세 정보를 가져온다."""
    resp = requests.get(f"{HN_API}/item/{item_id}.json", timeout=10)
    resp.raise_for_status()
    return resp.json()


def is_ai_related(title):
    """제목에 AI 관련 키워드가 포함되어 있는지 확인.

    짧은 키워드(3글자 이하)는 단어 경계 매칭을 적용하여
    "Spirit Air"의 "ai" 같은 오탐을 방지.
    """
    title_lower = title.lower()
    for kw in AI_KEYWORDS:
        if len(kw) <= 3:
            if re.search(r'\b' + re.escape(kw) + r'\b', title_lower):
                return True
        else:
            if kw in title_lower:
                return True
    return False


def fetch_ai_news(min_score=HN_MIN_SCORE_DAILY, limit=100):
    """AI 관련 HN 뉴스를 필터링하여 반환.

    Returns:
        list[dict]: 각 항목은 {id, title, url, score, hn_url} 키를 가짐.
    """
    story_ids = fetch_top_story_ids(limit)
    results = []

    for sid in story_ids:
        item = fetch_item(sid)
        if not item or item.get("type") != "story":
            continue

        title = item.get("title", "")
        score = item.get("score", 0)

        if score >= min_score and is_ai_related(title):
            results.append({
                "id": item["id"],
                "title": title,
                "url": item.get("url", ""),
                "score": score,
                "hn_url": f"https://news.ycombinator.com/item?id={item['id']}",
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results
