from datetime import datetime, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from get_arrivals import adjust_arrival_seconds, format_arrivals_summary, load_api_key


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
