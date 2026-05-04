"""Hugging Face API를 사용하여 기사 내용을 요약."""

import re
import requests
from bs4 import BeautifulSoup
from config import HF_API_TOKEN, SUMMARY_MAX_CHARS

HF_API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"


def fetch_article_text(url):
    """URL에서 기사 본문 텍스트를 추출."""
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

        return " ".join(text_parts)[:1024]  # BART 입력 제한
    except Exception:
        return ""


def summarize_with_hf(text):
    """Hugging Face Inference API로 영어 요약을 생성."""
    if not HF_API_TOKEN or not text:
        return None

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {
        "inputs": text,
        "parameters": {"max_length": 130, "min_length": 30},
    }

    try:
        resp = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if isinstance(result, list) and result:
            return result[0].get("summary_text", "").strip()
        return None
    except Exception as e:
        print(f"  [HF 요약 실패] {e}")
        return None


def fallback_summary(text, max_chars=SUMMARY_MAX_CHARS):
    """HF 사용 불가 시 앞부분 추출 방식으로 폴백."""
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
    """URL에서 기사를 가져와 요약을 반환. HF 우선, 실패 시 폴백."""
    text = fetch_article_text(url)
    if not text:
        return "요약을 가져올 수 없습니다."

    hf_result = summarize_with_hf(text)
    if hf_result:
        return hf_result

    return fallback_summary(text)
