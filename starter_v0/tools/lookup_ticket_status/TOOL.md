---
name: lookup_ticket_status
track: bonus
kind: local_status
provider: local_ticket_store
requires_env: []
inputs: [ticket_id]
outputs: [status, ticket]
side_effect: false
---
# lookup_ticket_status

Tra cứu trạng thái, mức độ ưu tiên, tóm tắt sự cố và tiến độ xử lý của một IT
ticket đã có dựa vào `ticket_id` (định dạng chuẩn `LAB-XXXXXXXX`).

Tool tra hai tầng: ưu tiên ticket mới tạo trong `tickets/`, sau đó fallback sang
database giả lập `helpdesk_data/mock_tickets.json`. Guardrail regex
`^LAB-[A-F0-9]{8}$` chặn path traversal và command injection.

## Smoke test

Chạy từ `starter_v0/`:

```powershell
python tools/lookup_ticket_status/smoke_test.py
```

PASS khi mọi dòng in ra `[PASS]` và exit code bằng 0.
