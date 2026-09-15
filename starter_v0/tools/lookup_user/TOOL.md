---
name: lookup_user
track: core
kind: local_directory
provider: mock_employee_directory
requires_env: []
inputs: [employee_id]
outputs: [employee, assigned_assets]
side_effect: false
---
# lookup_user

Tra cứu một nhân viên giả lập theo employee ID và trả về metadata hỗ trợ cùng danh sách asset được giao.
Tool này không bao giờ trả về thông tin đăng nhập, mật khẩu hoặc bí mật.
