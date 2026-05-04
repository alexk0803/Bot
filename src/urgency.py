"""키워드 기반 긴급도 판별."""

from config import URGENT_KEYWORDS, HN_MIN_SCORE_URGENT


def is_urgent(title, score=0):
    """뉴스가 긴급한지 판별.

    조건 (OR):
    1. 제목에 긴급 키워드가 포함됨
    2. HN 점수가 임계값 이상

    Returns:
        bool
    """
    title_lower = title.lower()
    if any(kw in title_lower for kw in URGENT_KEYWORDS):
        return True
    if score >= HN_MIN_SCORE_URGENT:
        return True
    return False
