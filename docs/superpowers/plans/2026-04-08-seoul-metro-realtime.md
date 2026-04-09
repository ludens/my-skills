# Seoul Metro Realtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 서울 지하철 역명을 입력받아 실시간 도착정보를 조회하고, 동명이역을 포함한 결과를 한국어로 요약하는 `seoul-metro-realtime` 스킬을 구현한다.

**Architecture:** `uv` 기반 Python 스킬 프로젝트로 구성한다. `station_lookup.py`는 역명 정규화와 CSV 후보 조회를 담당하고, `get_arrivals.py`는 `.env` 로드, `httpx` API 호출, 시차 보정, 출력 포맷을 담당한다. 테스트는 순수 함수 중심으로 분리해 네트워크 없이 대부분 검증하고, CLI와 실제 API 호출은 얇게 유지한다.

**Tech Stack:** Python 3.12+, `uv`, `httpx`, `python-dotenv`, `pytest`

---

## File Structure

- Create: `skills/seoul-metro-realtime/pyproject.toml`
- Create: `skills/seoul-metro-realtime/.gitignore`
- Create: `skills/seoul-metro-realtime/.env.example`
- Create: `skills/seoul-metro-realtime/SKILL.md`
- Create: `skills/seoul-metro-realtime/scripts/station_lookup.py`
- Create: `skills/seoul-metro-realtime/scripts/get_arrivals.py`
- Create: `skills/seoul-metro-realtime/tests/test_station_lookup.py`
- Create: `skills/seoul-metro-realtime/tests/test_arrival_formatting.py`

### Task 1: Bootstrap uv Project

**Files:**
- Create: `skills/seoul-metro-realtime/pyproject.toml`
- Create: `skills/seoul-metro-realtime/.gitignore`
- Create: `skills/seoul-metro-realtime/.env.example`
- Create: `skills/seoul-metro-realtime/docs/task-1-checklist.md`

- [ ] **Step 1: Write the failing metadata test expectation as a checklist**

Record this checklist in `skills/seoul-metro-realtime/docs/task-1-checklist.md`:

```text
- uv can resolve dependencies from pyproject.toml
- .env is ignored by git
- .env.example documents SEOUL_OPEN_API_KEY
```

- [ ] **Step 2: Create project metadata and dependencies**

```toml
[project]
name = "seoul-metro-realtime"
version = "0.1.0"
description = "Skill scripts for Seoul Metro realtime arrivals"
requires-python = ">=3.12"
dependencies = [
  "httpx>=0.27,<0.29",
  "python-dotenv>=1.0,<2.0",
]

[dependency-groups]
dev = [
  "pytest>=8.0,<9.0",
]

[tool.pytest.ini_options]
pythonpath = ["scripts"]
testpaths = ["tests"]
```

- [ ] **Step 3: Add ignore and env example files**

```gitignore
.env
.venv
__pycache__/
.pytest_cache/
```

```env
SEOUL_OPEN_API_KEY=your_api_key_here
```

- [ ] **Step 4: Resolve dependencies**

Run: `cd skills/seoul-metro-realtime && uv sync`

Expected: `Resolved` and environment created with no errors

- [ ] **Step 5: Commit**

```bash
git add skills/seoul-metro-realtime/pyproject.toml skills/seoul-metro-realtime/.gitignore skills/seoul-metro-realtime/.env.example
git commit -m "chore: bootstrap seoul metro realtime skill project"
```

If spec-review follow-up requires a separate checklist-artifact fix, allow one additional commit limited to `skills/seoul-metro-realtime/docs/task-1-checklist.md`.

### Task 2: Build Station Lookup with TDD

**Files:**
- Create: `skills/seoul-metro-realtime/scripts/station_lookup.py`
- Test: `skills/seoul-metro-realtime/tests/test_station_lookup.py`

- [ ] **Step 1: Write the failing tests**

```python
from station_lookup import find_station_candidates, normalize_station_name


def test_normalize_station_name_trims_suffix_and_whitespace():
    assert normalize_station_name("  서울역  ") == "서울"


def test_normalize_station_name_applies_alias_map():
    assert normalize_station_name("공릉역") == "공릉(서울산업대입구)"


def test_find_station_candidates_returns_multiple_lines_for_duplicate_name():
    rows = [
        {"SUBWAY_ID": "1001", "STATN_ID": "1001000133", "STATN_NM": "청량리", "호선이름": "1호선"},
        {"SUBWAY_ID": "1063", "STATN_ID": "1063075310", "STATN_NM": "청량리", "호선이름": "경의중앙선"},
    ]

    result = find_station_candidates("청량리역", rows)

    assert [item["line_name"] for item in result] == ["1호선", "경의중앙선"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd skills/seoul-metro-realtime && uv run pytest tests/test_station_lookup.py -v`

Expected: FAIL with `ModuleNotFoundError` or missing symbol errors

- [ ] **Step 3: Write minimal implementation**

```python
from __future__ import annotations

ALIAS_MAP = {
    "응암": "응암순환(상선)",
    "공릉": "공릉(서울산업대입구)",
    "남한산성입구": "남한산성입구(성남법원, 검찰청)",
    "대모산입구": "대모산",
    "천호": "천호(풍납토성)",
    "몽촌토성": "몽촌토성(평화의문)",
}


def normalize_station_name(raw_name: str) -> str:
    name = raw_name.strip()
    if name.endswith("역"):
        name = name[:-1]
    return ALIAS_MAP.get(name, name)


def find_station_candidates(raw_name: str, rows: list[dict[str, str]]) -> list[dict[str, str]]:
    normalized = normalize_station_name(raw_name)
    matches = [row for row in rows if row["STATN_NM"] == normalized or row["STATN_NM"] == raw_name.strip()]
    return [
        {
            "subway_id": row["SUBWAY_ID"],
            "station_id": row["STATN_ID"],
            "station_name": row["STATN_NM"],
            "line_name": row["호선이름"],
        }
        for row in matches
    ]
```

- [ ] **Step 4: Expand implementation to load the CSV**

```python
import csv
from pathlib import Path


def load_station_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd skills/seoul-metro-realtime && uv run pytest tests/test_station_lookup.py -v`

Expected: PASS for all three tests

- [ ] **Step 6: Commit**

```bash
git add skills/seoul-metro-realtime/scripts/station_lookup.py skills/seoul-metro-realtime/tests/test_station_lookup.py
git commit -m "feat: add seoul metro station lookup"
```

### Task 3: Parse and Format Arrival Data with TDD

**Files:**
- Create: `skills/seoul-metro-realtime/scripts/get_arrivals.py`
- Test: `skills/seoul-metro-realtime/tests/test_arrival_formatting.py`

- [ ] **Step 1: Write the failing tests**

```python
from datetime import datetime, timezone

from get_arrivals import adjust_arrival_seconds, format_arrivals_summary


def test_adjust_arrival_seconds_accounts_for_receipt_delay():
    now = datetime(2026, 4, 8, 10, 5, 30, tzinfo=timezone.utc)
    receipt = "2026-04-08 10:03:30"
    assert adjust_arrival_seconds(180, receipt, now) == 60


def test_format_arrivals_summary_groups_by_line_name():
    arrivals = [
        {"line_name": "1호선", "train_line_nm": "인천행", "seconds": 120, "status": "일반", "is_last_train": False},
        {"line_name": "경의중앙선", "train_line_nm": "문산행", "seconds": 240, "status": "급행", "is_last_train": True},
    ]

    output = format_arrivals_summary("서울", arrivals)

    assert "서울 실시간 도착정보" in output
    assert "1호선" in output
    assert "인천행: 2분 후 도착" in output
    assert "경의중앙선" in output
    assert "문산행: 4분 후 도착 (급행, 막차)" in output
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd skills/seoul-metro-realtime && uv run pytest tests/test_arrival_formatting.py -v`

Expected: FAIL with missing symbol errors

- [ ] **Step 3: Write minimal implementation**

```python
from __future__ import annotations

from collections import defaultdict
from datetime import datetime


def adjust_arrival_seconds(barvl_dt: int, receipt_time: str, now: datetime) -> int:
    received = datetime.fromisoformat(receipt_time)
    if received.tzinfo is None and now.tzinfo is not None:
        received = received.replace(tzinfo=now.tzinfo)
    delay_seconds = max(0, int((now - received).total_seconds()))
    return max(0, barvl_dt - delay_seconds)


def format_arrivals_summary(station_name: str, arrivals: list[dict[str, object]]) -> str:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in arrivals:
        grouped[str(item["line_name"])].append(item)

    lines = [f"{station_name} 실시간 도착정보", ""]
    for line_name, items in grouped.items():
        lines.append(line_name)
        for item in items:
            minutes = max(0, int(item["seconds"]) // 60)
            suffix = []
            if item["status"] != "일반":
                suffix.append(str(item["status"]))
            if item["is_last_train"]:
                suffix.append("막차")
            meta = f" ({', '.join(suffix)})" if suffix else ""
            lines.append(f"- {item['train_line_nm']}: {minutes}분 후 도착{meta}")
        lines.append("")
    return "\n".join(lines).strip()
```

- [ ] **Step 4: Add API parsing helper**

```python
LINE_NAME_BY_ID = {
    "1001": "1호선",
    "1063": "경의중앙선",
}


def parse_api_arrivals(payload: list[dict[str, str]]) -> list[dict[str, object]]:
    results = []
    for item in payload:
        results.append(
            {
                "line_name": LINE_NAME_BY_ID.get(item["subwayId"], item["subwayId"]),
                "train_line_nm": item.get("trainLineNm") or item.get("arvlMsg3") or "행선지 정보 없음",
                "seconds": int(item.get("barvlDt") or 0),
                "status": item.get("btrainSttus") or "일반",
                "is_last_train": item.get("lstcarAt") == "1",
                "receipt_time": item.get("recptnDt") or "",
            }
        )
    return results
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd skills/seoul-metro-realtime && uv run pytest tests/test_arrival_formatting.py -v`

Expected: PASS for both tests

- [ ] **Step 6: Commit**

```bash
git add skills/seoul-metro-realtime/scripts/get_arrivals.py skills/seoul-metro-realtime/tests/test_arrival_formatting.py
git commit -m "feat: add arrival parsing and formatting"
```

### Task 4: Add CLI, dotenv Loading, and HTTP Fetch

**Files:**
- Modify: `skills/seoul-metro-realtime/scripts/get_arrivals.py`
- Modify: `skills/seoul-metro-realtime/scripts/station_lookup.py`
- Test: `skills/seoul-metro-realtime/tests/test_arrival_formatting.py`

- [ ] **Step 1: Write the failing integration-focused tests**

```python
from pathlib import Path

from get_arrivals import load_api_key


def test_load_api_key_reads_dotenv(tmp_path: Path):
    env_file = tmp_path / ".env"
    env_file.write_text("SEOUL_OPEN_API_KEY=test-key\n", encoding="utf-8")

    assert load_api_key([env_file]) == "test-key"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd skills/seoul-metro-realtime && uv run pytest tests/test_arrival_formatting.py::test_load_api_key_reads_dotenv -v`

Expected: FAIL with missing `load_api_key`

- [ ] **Step 3: Implement dotenv loading and HTTP fetch**

```python
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv


def load_api_key(candidate_env_files: list[Path]) -> str:
    for env_file in candidate_env_files:
        if env_file.exists():
            load_dotenv(env_file, override=False)
            key = os.getenv("SEOUL_OPEN_API_KEY")
            if key:
                return key
    raise RuntimeError("SEOUL_OPEN_API_KEY not found in .env")


def fetch_realtime_arrivals(api_key: str, station_name: str) -> dict[str, object]:
    url = f"http://swopenAPI.seoul.go.kr/api/subway/{api_key}/json/realtimeStationArrival/0/100/{station_name}"
    with httpx.Client(timeout=10.0) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.json()
```

- [ ] **Step 4: Implement CLI entrypoint**

```python
def main() -> int:
    import sys
    from pathlib import Path

    if len(sys.argv) < 2:
        print("사용법: uv run python scripts/get_arrivals.py \"서울역\"")
        return 1

    skill_root = Path(__file__).resolve().parents[1]
    env_files = [skill_root / ".env", skill_root.parent.parent / ".env"]
    raw_name = sys.argv[1]
    api_key = load_api_key(env_files)
    payload = fetch_realtime_arrivals(api_key, raw_name)
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Run tests to verify pass**

Run: `cd skills/seoul-metro-realtime && uv run pytest tests/test_arrival_formatting.py -v`

Expected: PASS including dotenv test

- [ ] **Step 6: Commit**

```bash
git add skills/seoul-metro-realtime/scripts/get_arrivals.py skills/seoul-metro-realtime/tests/test_arrival_formatting.py
git commit -m "feat: add dotenv loading and realtime fetch cli"
```

### Task 5: Wire Final Output and Error Handling

**Files:**
- Modify: `skills/seoul-metro-realtime/scripts/get_arrivals.py`
- Modify: `skills/seoul-metro-realtime/scripts/station_lookup.py`
- Test: `skills/seoul-metro-realtime/tests/test_arrival_formatting.py`

- [ ] **Step 1: Add a failing API message parsing test**

```python
from get_arrivals import extract_arrival_rows


def test_extract_arrival_rows_returns_empty_for_info_200():
    payload = {
        "errorMessage": {"status": 200, "code": "INFO-200", "message": "해당하는 데이터가 없습니다."}
    }

    assert extract_arrival_rows(payload) == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd skills/seoul-metro-realtime && uv run pytest tests/test_arrival_formatting.py::test_extract_arrival_rows_returns_empty_for_info_200 -v`

Expected: FAIL with missing `extract_arrival_rows`

- [ ] **Step 3: Implement payload extraction and user-facing errors**

```python
def extract_arrival_rows(payload: dict[str, object]) -> list[dict[str, str]]:
    if "realtimeArrivalList" in payload:
        return list(payload["realtimeArrivalList"])

    error = payload.get("errorMessage")
    if isinstance(error, dict) and error.get("code") == "INFO-200":
        return []

    if isinstance(error, dict):
        code = error.get("code", "UNKNOWN")
        message = error.get("message", "알 수 없는 오류")
        raise RuntimeError(f"{code}: {message}")

    raise RuntimeError("응답 형식을 해석할 수 없습니다.")
```

- [ ] **Step 4: Replace raw payload print with formatted summary**

```python
def build_summary_for_station(raw_name: str, rows: list[dict[str, str]], now: datetime) -> str:
    parsed = parse_api_arrivals(rows)
    normalized = [
        {
            **item,
            "seconds": adjust_arrival_seconds(int(item["seconds"]), str(item["receipt_time"]), now),
        }
        for item in parsed
    ]
    normalized.sort(key=lambda item: int(item["seconds"]))
    return format_arrivals_summary(raw_name.removesuffix("역"), normalized)
```

- [ ] **Step 5: Run full test suite**

Run: `cd skills/seoul-metro-realtime && uv run pytest -v`

Expected: PASS for station lookup, formatting, dotenv, and payload extraction tests

- [ ] **Step 6: Commit**

```bash
git add skills/seoul-metro-realtime/scripts/get_arrivals.py skills/seoul-metro-realtime/tests/test_arrival_formatting.py
git commit -m "feat: finalize arrival summaries and error handling"
```

### Task 6: Write SKILL.md and Validate the Skill

**Files:**
- Create: `skills/seoul-metro-realtime/SKILL.md`
- Modify: `skills/seoul-metro-realtime/agents/openai.yaml` if generated later

- [ ] **Step 1: Write the skill frontmatter and core instructions**

```md
---
name: seoul-metro-realtime
description: Query Seoul subway realtime arrival information for a station name using the Seoul open API. Use when Codex needs to look up train arrival times, realtime subway status for a station, or summarize arrivals across duplicate station names. Supports `.env`-managed API keys and station alias normalization for Seoul Metro names.
---

# Seoul Metro Realtime

- Load `references/서울시 지하철 실시간 도착정보 API 명세서.md` only when API field details or alias exceptions are needed.
- Use `references/실시간도착_역정보(20260108).csv` through `scripts/station_lookup.py` for station candidate lookup.
- Run `uv run python scripts/get_arrivals.py "<역명>"` from the skill root.
- If `.env` or `SEOUL_OPEN_API_KEY` is missing, tell the user how to create `skills/seoul-metro-realtime/.env`.
- Show all matching lines for duplicate station names in one answer.
```

- [ ] **Step 2: Validate basic project and tests**

Run: `cd skills/seoul-metro-realtime && uv run pytest -v`

Expected: PASS

- [ ] **Step 3: Validate skill metadata**

Run: `python /home/ludens/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/seoul-metro-realtime`

Expected: validation success with no frontmatter errors

- [ ] **Step 4: Commit**

```bash
git add skills/seoul-metro-realtime/SKILL.md skills/seoul-metro-realtime/scripts skills/seoul-metro-realtime/tests skills/seoul-metro-realtime/pyproject.toml skills/seoul-metro-realtime/.env.example skills/seoul-metro-realtime/.gitignore
git commit -m "feat: add seoul metro realtime skill"
```

## Self-Review

- Spec coverage:
  - `.env` 관리: Task 1, Task 4
  - 역명 정규화/예외 처리: Task 2
  - CSV 후보 조회와 동명이역 동시 표시: Task 2, Task 5
  - API 호출과 응답 파싱: Task 3, Task 4, Task 5
  - stale 데이터 보정: Task 3, Task 5
  - SKILL.md와 검증: Task 6
- Placeholder scan:
  - `TODO`, `TBD`, “적절히 처리” 같은 문구 없음
- Type consistency:
  - `normalize_station_name`, `find_station_candidates`, `adjust_arrival_seconds`, `parse_api_arrivals`, `format_arrivals_summary`, `load_api_key`, `extract_arrival_rows` 이름을 전 태스크에서 일관되게 사용
