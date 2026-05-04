import os

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
HF_API_TOKEN = os.environ.get("HF_API_TOKEN", "")

# AI 관련 필터링 키워드 (소문자)
AI_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "llm", "large language model", "gpt", "openai", "anthropic", "claude",
    "gemini", "mistral", "llama", "transformer", "neural network",
    "diffusion", "stable diffusion", "midjourney", "copilot",
    "chatgpt", "generative ai", "gen ai", "foundation model",
    "agi", "alignment", "rlhf", "fine-tuning", "finetuning",
    "hugging face", "huggingface", "pytorch", "tensorflow",
    "computer vision", "nlp", "natural language processing",
    "speech recognition", "text-to-image", "text-to-video",
    "autonomous", "self-driving", "robotics",
]

# 긴급 뉴스 키워드 (소문자) - 이 키워드가 포함되면 긴급으로 분류
URGENT_KEYWORDS = [
    "gpt-5", "gpt5", "claude 4", "claude-4", "gemini 2", "gemini-2",
    "agi", "breakthrough", "open source release", "open-source release",
    "acquisition", "acquire", "shutdown", "ban", "regulation",
    "safety incident", "leak", "data breach",
    "superintelligence", "singularity",
    "billion parameter", "trillion parameter",
    "beats human", "surpass human", "human-level",
]

# HN 점수 기준
HN_MIN_SCORE_DAILY = 50       # 일일 요약에 포함할 최소 점수
HN_MIN_SCORE_URGENT = 200     # 긴급 뉴스로 간주할 점수

# GitHub Trending 설정
GITHUB_TRENDING_URL = "https://github.com/trending"

# 사용자 정의 키워드 워치 (이 키워드가 제목에 포함되면 즉시 알림)
WATCH_KEYWORDS = [
    "gpt-5", "gpt5", "claude 4", "claude-4", "gemini 2",
    "openai", "anthropic", "google deepmind",
    "sam altman", "dario amodei",
    "apple ai", "meta ai", "microsoft ai",
]

# 키워드 워치 HN 최소 점수 (너무 낮은 점수 뉴스 필터링)
WATCH_MIN_SCORE = 20

# 캐시 파일 경로 (중복 방지용)
SENT_CACHE_FILE = "sent_ids.json"
WATCH_CACHE_FILE = "watch_sent_ids.json"

# 요약 설정
SUMMARY_MAX_CHARS = 200  # 요약 최대 글자 수
