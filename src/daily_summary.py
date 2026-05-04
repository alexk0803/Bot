"""일일 AI 뉴스 요약 - 매일 KST 07:00 실행."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.news_fetcher import fetch_ai_news
from src.github_trending import fetch_ai_trending
from src.summarizer import get_summary
from src.discord_sender import send_daily_summary


def main():
    print("AI 일일 요약 수집 중...")

    news = fetch_ai_news()
    print(f"  HN AI 뉴스: {len(news)}건")

    # 각 뉴스에 요약 추가
    for item in news[:15]:
        item["summary"] = get_summary(item["url"])
    print("  뉴스 요약 완료")

    trending = fetch_ai_trending()
    print(f"  GitHub 트렌딩 AI 레포: {len(trending)}건")

    send_daily_summary(news, trending)
    print("일일 요약 전송 완료!")


if __name__ == "__main__":
    main()
