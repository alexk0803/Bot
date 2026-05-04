# AI News & GitHub Trending Discord Bot

AI 관련 뉴스와 GitHub 트렌딩 레포를 Discord로 알려주는 봇입니다.

- **매일 오전 7시(KST)**: AI 뉴스 + GitHub 트렌딩 요약
- **매 30분**: 긴급/파급력 큰 뉴스 즉시 알림

---

## 1. 사전 준비

- GitHub 계정
- Discord 서버 (관리자 권한 필요)

---

## 2. Discord Webhook 생성

1. Discord 앱에서 알림을 받을 **채널**을 우클릭 → **채널 편집**
2. 왼쪽 메뉴에서 **연동** (Integrations) 클릭
3. **웹후크** (Webhooks) → **새 웹후크** (New Webhook) 클릭
4. 이름을 원하는 대로 설정 (예: `AI News Bot`)
5. **웹후크 URL 복사** 버튼 클릭 → URL을 메모장에 저장
   - 형식: `https://discord.com/api/webhooks/123456789/abcdefg...`

---

## 3. GitHub 레포지토리 설정

### 3-1. 레포 생성 및 Push

```bash
# 이 프로젝트 폴더에서
cd Claude_bot

# GitHub에 새 레포 생성 (gh CLI 사용 시)
gh repo create ai-news-bot --private --source=. --push

# 또는 수동으로
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git add .
git commit -m "Add AI news bot"
git push -u origin main
```

### 3-2. Webhook URL을 Secret으로 등록

1. GitHub에서 레포 페이지 접속
2. 상단 탭에서 **Settings** 클릭
3. 왼쪽 메뉴에서 **Secrets and variables** → **Actions** 클릭
4. **New repository secret** 버튼 클릭
5. 다음과 같이 입력:
   - **Name**: `DISCORD_WEBHOOK_URL`
   - **Secret**: 2단계에서 복사한 웹후크 URL 붙여넣기
6. **Add secret** 클릭

---

## 4. 동작 확인

### 4-1. 수동 실행 (처음 테스트)

1. GitHub 레포 → **Actions** 탭 클릭
2. 왼쪽에서 **AI Daily Summary** 또는 **Breaking AI News Check** 선택
3. **Run workflow** 버튼 클릭 → **Run workflow** 확인
4. 실행 완료 후 Discord 채널에 메시지가 오는지 확인

### 4-2. 자동 스케줄

Push가 완료되면 자동으로 스케줄이 등록됩니다:

| 워크플로우 | 실행 주기 | 설명 |
|---|---|---|
| `daily_summary.yml` | 매일 KST 07:00 | AI 뉴스 + GitHub 트렌딩 요약 |
| `breaking_news.yml` | 매 30분 | 긴급 뉴스 감지 시 즉시 알림 |

> **참고**: GitHub Actions cron은 정확한 시간에 실행되지 않을 수 있습니다 (최대 5~15분 지연 가능).

### 4-3. 로컬 테스트

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

# 일일 요약 테스트
python src/daily_summary.py

# 긴급 뉴스 체크 테스트
python src/breaking_check.py
```

---

## 5. 커스터마이징

### 키워드 수정

`config.py`에서 수정 가능합니다:

- **`AI_KEYWORDS`**: AI 관련 뉴스를 필터링하는 키워드 목록
- **`URGENT_KEYWORDS`**: 긴급 뉴스로 분류하는 키워드 목록
- **`HN_MIN_SCORE_DAILY`**: 일일 요약에 포함할 최소 HN 점수 (기본: 50)
- **`HN_MIN_SCORE_URGENT`**: 긴급 뉴스로 간주할 HN 점수 (기본: 200)

### 알림 주기 변경

`.github/workflows/breaking_news.yml`의 cron 표현식을 수정합니다:

```yaml
# 매 30분 (기본)
- cron: "*/30 * * * *"

# 매 15분으로 변경
- cron: "*/15 * * * *"

# 매 1시간으로 변경
- cron: "0 * * * *"
```

---

## 6. 문제 해결

| 증상 | 확인 사항 |
|---|---|
| Discord에 메시지가 안 옴 | Settings → Secrets에 `DISCORD_WEBHOOK_URL`이 올바르게 등록되었는지 확인 |
| Actions가 실행되지 않음 | 레포에 `.github/workflows/` 파일이 push되었는지 확인. Actions 탭에서 워크플로우가 활성화되어 있는지 확인 |
| "AI 뉴스 0건" | 일시적으로 AI 관련 뉴스가 HN 상위에 없는 경우. `config.py`에서 `HN_MIN_SCORE_DAILY`를 낮추면 더 많이 수집 |
| 오탐 (AI 무관 뉴스 수신) | `config.py`의 `AI_KEYWORDS`에서 너무 짧거나 범용적인 키워드 제거 |
