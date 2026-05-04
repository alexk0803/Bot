"""기사 내용을 가져와 간단히 요약."""

import re
import requests
from bs4 import BeautifulSoup
from config import SUMMARY_MAX_CHARS


def fetch_article_text(url):
    """URL에서 기사 본문 텍스트를 추출."""
    if not url:
        return ""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (AI-News-Bot)"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # script, style 태그 제거
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()

        # 본문 추출 시도: article > p 태그 우선
        article = soup.find("article")
        container = article if article else soup.find("body")
        if not container:
            return ""

        paragraphs = container.find_all("p")
        text_parts = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 30:  # 너무 짧은 문단 무시
                text_parts.append(text)

        return " ".join(text_parts)
    except Exception:
        return ""


def summarize_text(text, max_chars=SUMMARY_MAX_CHARS):
    """텍스트를 지정된 길이로 요약 (앞부분 추출 방식)."""
    if not text:
        return "요약을 가져올 수 없습니다."

    # 불필요한 공백 정리
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) <= max_chars:
        return text

    # 문장 단위로 자르기
    truncated = text[:max_chars]
    last_period = max(truncated.rfind("."), truncated.rfind("!"), truncated.rfind("?"))
    if last_period > max_chars // 2:
        return truncated[: last_period + 1]
    return truncated.rsplit(" ", 1)[0] + "..."


def get_summary(url):
    """URL에서 기사를 가져와 요약을 반환."""
    text = fetch_article_text(url)
    return summarize_text(text)
