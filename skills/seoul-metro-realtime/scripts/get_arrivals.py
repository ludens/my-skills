from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from pathlib import Path
import os
import sys

import httpx
from dotenv import load_dotenv

LINE_NAME_BY_ID = {
    "1001": "1호선",
    "1063": "경의중앙선",
}


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


def main() -> int:
    if len(sys.argv) < 2:
        print('사용법: uv run python scripts/get_arrivals.py "서울역"')
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
