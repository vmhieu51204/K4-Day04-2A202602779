"""Standalone unit smoke test for the lookup_ticket_status bonus tool.

Run from starter_v0/:

    python tools/lookup_ticket_status/smoke_test.py

No provider key or network access is required. The test uses only mock data and
a temporary directory, so the real tickets/ folder is never written.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import TOOL_FUNCTIONS
from tools.lookup_ticket_status import tool as lookup_tool


def check(name: str, condition: bool, detail: object = "") -> bool:
    status = "PASS" if condition else "FAIL"
    suffix = "" if condition else f" -> {detail!r}"
    print(f"[{status}] {name}{suffix}")
    return condition


def main() -> int:
    results: list[bool] = []
    lookup = TOOL_FUNCTIONS["lookup_ticket_status"]

    results.append(check(
        "tool registered in TOOL_FUNCTIONS",
        lookup is lookup_tool.lookup_ticket_status,
    ))

    found = lookup("LAB-9B1D2E4F")
    results.append(check(
        "mock ticket found by exact id",
        found.get("status") == "found"
        and found.get("source") == "mock_database"
        and found.get("ticket", {}).get("ticket_id") == "LAB-9B1D2E4F",
        found,
    ))
    results.append(check(
        "ticket id is normalized (case-insensitive)",
        lookup("lab-9b1d2e4f").get("status") == "found",
    ))

    with tempfile.TemporaryDirectory() as tmp:
        live_dir = Path(tmp)
        live_id = "LAB-DEADBEEF"
        (live_dir / f"{live_id}.json").write_text(
            json.dumps({"ticket_id": live_id, "summary": "smoke", "priority": "high", "status": "open"}),
            encoding="utf-8",
        )
        original_dir = lookup_tool.TICKET_DIR
        lookup_tool.TICKET_DIR = live_dir
        try:
            live = lookup(live_id)
        finally:
            lookup_tool.TICKET_DIR = original_dir
    results.append(check(
        "live ticket found in tickets/",
        live.get("status") == "found" and live.get("source") == "live_tickets",
        live,
    ))

    results.append(check(
        "non-ticket id rejected",
        lookup("LT-204").get("error") == "invalid_ticket_id_format",
    ))
    results.append(check(
        "path traversal rejected",
        lookup("../../etc/passwd").get("error") == "invalid_ticket_id_format",
    ))
    results.append(check(
        "empty id rejected",
        lookup("").get("error") == "missing_ticket_id",
    ))
    results.append(check(
        "non-string id rejected",
        lookup(None).get("error") == "invalid_ticket_id_type",
    ))
    results.append(check(
        "valid-but-unknown id returns not_found",
        lookup("LAB-00000000").get("status") == "not_found",
    ))

    passed = sum(1 for item in results if item)
    total = len(results)
    print(f"\n{passed}/{total} checks passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
