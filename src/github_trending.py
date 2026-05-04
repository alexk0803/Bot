"""GitHub Trending 페이지에서 AI 관련 레포를 스크래핑."""

import requests
from bs4 import BeautifulSoup
from config import AI_KEYWORDS, GITHUB_TRENDING_URL


def fetch_trending_repos():
    """GitHub Trending 페이지를 파싱하여 레포 목록을 반환.

    Returns:
        list[dict]: 각 항목은 {name, url, description, stars_today, language} 키를 가짐.
    """
    headers = {"User-Agent": "Mozilla/5.0 (AI-News-Bot)"}
    resp = requests.get(GITHUB_TRENDING_URL, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    repos = []

    for article in soup.select("article.Box-row"):
        # 레포 이름
        h2 = article.select_one("h2 a")
        if not h2:
            continue
        repo_path = h2.get("href", "").strip("/")
        name = repo_path.replace("/", " / ")

        # 설명
        p = article.select_one("p")
        description = p.get_text(strip=True) if p else ""

        # 언어
        lang_span = article.select_one("[itemprop='programmingLanguage']")
        language = lang_span.get_text(strip=True) if lang_span else ""

        # 오늘의 스타 수
        stars_today = ""
        for span in article.select("span.d-inline-block.float-sm-right"):
            stars_today = span.get_text(strip=True)

        repos.append({
            "name": name,
            "url": f"https://github.com/{repo_path}",
            "description": description,
            "stars_today": stars_today,
            "language": language,
        })

    return repos


def filter_ai_repos(repos):
    """AI 관련 레포만 필터링."""
    results = []
    for repo in repos:
        text = f"{repo['name']} {repo['description']}".lower()
        if any(kw in text for kw in AI_KEYWORDS):
            results.append(repo)
    return results


def fetch_ai_trending():
    """AI 관련 트렌딩 레포를 가져온다."""
    repos = fetch_trending_repos()
    return filter_ai_repos(repos)
