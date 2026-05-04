"""긴급 AI 뉴스 체크 - 30분마다 실행."""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import SENT_CACHE_FILE
from src.news_fetcher import fetch_ai_news
from src.urgency import is_urgent
from src.summarizer import get_summary
from src.discord_sender import send_breaking_alert


def load_sent_ids():
    """이미 전송한 뉴스 ID 목록을 로드."""
    if os.path.exists(SENT_CACHE_FILE):
        with open(SENT_CACHE_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_sent_ids(sent_ids):
    """전송한 뉴스 ID 목록을 저장."""
    with open(SENT_CACHE_FILE, "w") as f:
        json.dump(list(sent_ids), f)


def main():
    print("긴급 AI 뉴스 체크 중...")

    sent_ids = load_sent_ids()
    news = fetch_ai_news(min_score=30, limit=50)
    new_alerts = 0

    for item in news:
        if item["id"] in sent_ids:
            continue
        if is_urgent(item["title"], item["score"]):
            print(f"  [긴급] {item['title']} (score: {item['score']})")
            item["summary"] = get_summary(item["url"])
            send_breaking_alert(item)
            sent_ids.add(item["id"])
            new_alerts += 1

    save_sent_ids(sent_ids)

    if new_alerts:
        print(f"긴급 알림 {new_alerts}건 전송 완료!")
    else:
        print("새로운 긴급 뉴스 없음.")


if __name__ == "__main__":
    main()
