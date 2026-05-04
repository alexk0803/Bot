"""사용자 정의 키워드 워치 - 10분마다 실행."""

import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import WATCH_KEYWORDS, WATCH_MIN_SCORE, WATCH_CACHE_FILE
from src.news_fetcher import fetch_top_story_ids, fetch_item
from src.summarizer import get_summary
from src.discord_sender import send_keyword_alert


def load_watch_cache():
    """이미 전송한 키워드 알림 ID 목록을 로드."""
    if os.path.exists(WATCH_CACHE_FILE):
        with open(WATCH_CACHE_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_watch_cache(sent_ids):
    """전송한 키워드 알림 ID 목록을 저장."""
    with open(WATCH_CACHE_FILE, "w") as f:
        json.dump(list(sent_ids), f)


def find_matched_keywords(title):
    """제목에서 매칭되는 워치 키워드 목록을 반환."""
    title_lower = title.lower()
    matched = []
    for kw in WATCH_KEYWORDS:
        if len(kw) <= 3:
            if re.search(r'\b' + re.escape(kw) + r'\b', title_lower):
                matched.append(kw)
        else:
            if kw in title_lower:
                matched.append(kw)
    return matched


def main():
    print("키워드 워치 체크 중...")

    sent_ids = load_watch_cache()
    story_ids = fetch_top_story_ids(limit=80)
    new_alerts = 0

    for sid in story_ids:
        if sid in sent_ids:
            continue

        item = fetch_item(sid)
        if not item or item.get("type") != "story":
            continue

        title = item.get("title", "")
        score = item.get("score", 0)

        if score < WATCH_MIN_SCORE:
            continue

        matched = find_matched_keywords(title)
        if not matched:
            continue

        url = item.get("url", "")
        hn_url = f"https://news.ycombinator.com/item?id={item['id']}"
        summary = get_summary(url)

        news_item = {
            "id": item["id"],
            "title": title,
            "url": url,
            "score": score,
            "hn_url": hn_url,
            "matched_keywords": matched,
            "summary": summary,
        }

        print(f"  [키워드 매치] {title}")
        print(f"    키워드: {', '.join(matched)}")
        send_keyword_alert(news_item)
        sent_ids.add(sid)
        new_alerts += 1

    save_watch_cache(sent_ids)

    if new_alerts:
        print(f"키워드 알림 {new_alerts}건 전송 완료!")
    else:
        print("새로운 키워드 매치 뉴스 없음.")


if __name__ == "__main__":
    main()
