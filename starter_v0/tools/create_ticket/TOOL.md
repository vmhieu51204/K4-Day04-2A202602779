---
name: create_ticket
track: bonus
kind: action
provider: local_ticket_store
requires_env: []
inputs: [summary, priority, asset_id, confirmed]
outputs: [status, ticket_id, path]
side_effect: local_file_write
requires_confirmation: true
---
# create_ticket

Tạo một ticket hỗ trợ giả lập dưới thư mục `tickets/`. Tool sẽ trả về trạng thái
`needs_confirmation` và không ghi gì nếu `confirmed` chưa được đặt là true một cách rõ ràng.
Tool từ chối asset ID không hợp lệ và các summary chứa credentials, token, mã MFA hoặc recovery code.
