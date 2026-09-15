---
name: clarify
track: core
kind: control
requires_env: []
inputs: [question, response_type, options]
outputs: [question, response_type, options, awaiting_user]
side_effect: false
---
# clarify

Hỏi người dùng để lấy thông tin còn thiếu hoặc xác nhận cần thiết và tạm dừng cho đến lượt tiếp theo của người dùng.
`response_type` có thể là văn bản tự do, yes/no hoặc lựa chọn từ `options`.
