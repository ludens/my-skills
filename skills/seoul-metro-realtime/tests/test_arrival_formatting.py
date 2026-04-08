from datetime import datetime, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from get_arrivals import (
    adjust_arrival_seconds,
    build_summary_for_station,
    extract_arrival_rows,
    fetch_realtime_arrivals,
    format_arrivals_summary,
    load_api_key,
)


class DummyResponse:
    def __init__(self, payload: dict[str, object]):
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, object]:
        return self._payload


class DummyClient:
    def __init__(self, payload: dict[str, object]):
        self.payload = payload
        self.requested_url: str | None = None

    def __enter__(self) -> "DummyClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def get(self, url: str) -> DummyResponse:
        self.requested_url = url
        return DummyResponse(self.payload)


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


def test_load_api_key_reads_dotenv(tmp_path: Path):
    env_file = tmp_path / ".env"
    env_file.write_text("SEOUL_OPEN_API_KEY=test-key\n", encoding="utf-8")

    assert load_api_key([env_file]) == "test-key"


def test_extract_arrival_rows_returns_empty_for_info_200():
    payload = {
        "errorMessage": {"status": 200, "code": "INFO-200", "message": "해당하는 데이터가 없습니다."}
    }

    assert extract_arrival_rows(payload) == []


def test_build_summary_for_station_adjusts_and_sorts_arrivals():
    now = datetime(2026, 4, 8, 10, 5, 30, tzinfo=timezone.utc)
    rows = [
        {
            "subwayId": "1001",
            "trainLineNm": "인천행",
            "barvlDt": "180",
            "btrainSttus": "일반",
            "lstcarAt": "0",
            "recptnDt": "2026-04-08 10:03:30",
        },
        {
            "subwayId": "1063",
            "trainLineNm": "문산행",
            "barvlDt": "240",
            "btrainSttus": "급행",
            "lstcarAt": "1",
            "recptnDt": "2026-04-08 10:05:00",
        },
    ]

    output = build_summary_for_station("서울역", rows, now)

    assert output.startswith("서울 실시간 도착정보")
    assert "인천행: 1분 후 도착" in output
    assert "문산행: 3분 후 도착 (급행, 막차)" in output


def test_fetch_realtime_arrivals_normalizes_station_name_before_request(monkeypatch):
    payload = {"ok": True}
    dummy_client = DummyClient(payload)

    def fake_client(*args, **kwargs):
        return dummy_client

    monkeypatch.setattr("get_arrivals.httpx.Client", fake_client)

    result = fetch_realtime_arrivals("secret-key", "서울역")

    assert result == payload
    assert dummy_client.requested_url is not None
    assert dummy_client.requested_url.endswith("/서울")
