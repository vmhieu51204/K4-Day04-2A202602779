---
name: format_incident_report
track: core
kind: local_formatter
requires_env: []
inputs: [findings, template, incident_title]
outputs: [markdown, finding_count]
side_effect: false
---
# format_incident_report

Định dạng các findings đã được thu thập từ các tool khác. Tool này không kiểm tra thiết bị,
không xem trạng thái dịch vụ, không tìm kiếm knowledge base hay tạo ticket.
