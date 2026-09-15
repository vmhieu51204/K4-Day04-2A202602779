from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from tools._shared import ROOT, err

# Thư mục lưu các ticket được tạo lúc chạy thật
TICKET_DIR = ROOT / "tickets"
# File mock data dự phòng
MOCK_TICKETS_FILE = ROOT / "helpdesk_data" / "mock_tickets.json"

# RÀO CHẮN BẢO MẬT (Security Guardrail):
# Chỉ cho phép định dạng chuẩn LAB-XXXXXXXX (8 ký tự Hex, không phân biệt hoa thường).
# Loại bỏ triệt để nguy cơ Path Traversal (../) hoặc chèn mã độc.
TICKET_ID_PATTERN = re.compile(r"^LAB-[A-F0-9]{8}$", re.IGNORECASE)


def lookup_ticket_status(ticket_id: str = "") -> dict[str, Any]:
    """
    Tra cứu tiến độ và chi tiết của một ticket hỗ trợ IT dựa trên mã ticket_id.
    """
    # 1. Kiểm tra kiểu dữ liệu đầu vào
    if not isinstance(ticket_id, str):
        return {"tool": "lookup_ticket_status", "error": "invalid_ticket_id_type"}

    normalized_id = ticket_id.strip().upper()
    if not normalized_id:
        return {"tool": "lookup_ticket_status", "error": "missing_ticket_id"}

    # 2. Kiểm tra định dạng Regex bảo mật
    if not TICKET_ID_PATTERN.fullmatch(normalized_id):
        return {
            "tool": "lookup_ticket_status",
            "error": "invalid_ticket_id_format",
            "message": "Ticket ID must match format LAB-XXXXXXXX (8 hex characters), e.g., LAB-9B1D2E4F.",
        }

    try:
        # 3. Tầng 1: Kiểm tra xem ticket có vừa được tạo trong thư mục tickets/ không
        live_ticket_path = TICKET_DIR / f"{normalized_id}.json"
        if live_ticket_path.is_file():
            data = json.loads(live_ticket_path.read_text(encoding="utf-8"))
            return {
                "tool": "lookup_ticket_status",
                "status": "found",
                "source": "live_tickets",
                "ticket": {
                    "ticket_id": data.get("ticket_id", normalized_id),
                    "summary": data.get("summary", ""),
                    "priority": data.get("priority", "medium"),
                    "status": data.get("status", "open"),
                    "asset_id": data.get("asset_id"),
                    "created_at": data.get("created_at"),
                    "resolution_notes": data.get("resolution_notes", "Đã ghi nhận trên hệ thống xử lý sự cố."),
                },
            }

        # 4. Tầng 2: Tra cứu trong mock database (mock_tickets.json)
        if MOCK_TICKETS_FILE.is_file():
            mock_data = json.loads(MOCK_TICKETS_FILE.read_text(encoding="utf-8"))
            for ticket in mock_data.get("tickets", []):
                if ticket.get("ticket_id", "").strip().upper() == normalized_id:
                    return {
                        "tool": "lookup_ticket_status",
                        "status": "found",
                        "source": "mock_database",
                        "ticket": ticket,
                    }

        # 5. Nếu không tìm thấy ở cả 2 nơi
        return {
            "tool": "lookup_ticket_status",
            "status": "not_found",
            "ticket_id": normalized_id,
            "message": f"Không tìm thấy ticket nào có mã {normalized_id} trong hệ thống.",
        }

    except Exception as exc:
        return err("lookup_ticket_status", exc)
