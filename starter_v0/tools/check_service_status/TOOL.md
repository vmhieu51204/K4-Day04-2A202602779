---
name: check_service_status
track: core
kind: local_status
provider: mock_status_page
requires_env: []
inputs: [service, environment]
outputs: [service, environment, status, incident]
side_effect: false
---
# check_service_status

Đọc trang trạng thái mô phỏng cố định cho một dịch vụ dùng chung và môi trường tương ứng.
Tool này không chẩn đoán thiết bị cá nhân của nhân viên.
