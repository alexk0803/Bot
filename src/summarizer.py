"""Gemini API를 사용하여 기사 내용을 한��어로 요약."""

import re
import requests
from bs4 import BeautifulSoup
from config import GEMINI_API_KEY, SUMMARY_MAX_CHARS

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False


def _init_gemini():
    """Gemini 클라이언트를 초기화."""
    if not HAS_GEMINI or not GEMINI_API_KEY:
        return None
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel("gemini-2.0-flash")


_model = _init_gemini()


def fetch_article_text(url):
    """URL에서 기사 본문 텍스트�� 추출."""
    if not url:
        return ""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (AI-News-Bot)"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()

        article = soup.find("article")
        container = article if article else soup.find("body")
        if not container:
            return ""

        paragraphs = container.find_all("p")
        text_parts = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 30:
                text_parts.append(text)

        return " ".join(text_parts)[:3000]  # Gemini에 보낼 최대 길이 제한
    except Exception:
        return ""


def summarize_with_gemini(text, title=""):
    """Gemini API로 한국어 3줄 요약을 생성."""
    if not _model or not text:
        return None

    prompt = (
        "다음 뉴스 기사를 한국어로 요약해줘.\n"
        "규칙:\n"
        "- 핵심 내용을 3줄 이내의 bullet point로 정리\n"
        "- 각 줄은 '- '로 시작\n"
        "- 전문 용어는 원문 그대로 유지\n"
        "- 불필요한 서론 없이 바로 요약\n\n"
        f"제목: {title}\n\n"
        f"본문:\n{text}"
    )

    try:
        response = _model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"  [Gemini 요약 실패] {e}")
        return None


def fallback_summary(text, max_chars=SUMMARY_MAX_CHARS):
    """Gemini 사용 불가 시 앞부분 추출 방식으로 폴백."""
    if not text:
        return "요약을 가져올 수 없습니다."

    text = re.sub(r"\s+", " ", text).strip()

    if len(text) <= max_chars:
        return text

    truncated = text[:max_chars]
    last_period = max(truncated.rfind("."), truncated.rfind("!"), truncated.rfind("?"))
    if last_period > max_chars // 2:
        return truncated[: last_period + 1]
    return truncated.rsplit(" ", 1)[0] + "..."


def get_summary(url, title=""):
    """URL에서 기사를 가져와 요약을 반환. Gemini 우선, 실패 시 폴백."""
    text = fetch_article_text(url)
    if not text:
        return "요약을 가져올 수 없습니다."

    # Gemini로 요약 시도
    gemini_result = summarize_with_gemini(text, title)
    if gemini_result:
        return gemini_result

    # 폴백: 텍스트 앞부분 추출
    return fallback_summary(text)
