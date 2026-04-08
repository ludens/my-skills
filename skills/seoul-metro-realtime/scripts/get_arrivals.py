from __future__ import annotations

from collections import defaultdict
from datetime import datetime

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
