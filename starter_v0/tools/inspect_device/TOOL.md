---
name: inspect_device
track: core
kind: local_inventory
provider: mock_device_inventory
requires_env: []
inputs: [asset_id, check]
outputs: [device, diagnostics]
side_effect: false
---
# inspect_device

Tra cứu một thiết bị trong kho tài sản của công ty và trả về snapshot chẩn đoán đã lưu.
Cần có asset ID hợp lệ. Các kiểu kiểm tra hỗ trợ gồm all, network, vpn, security, hardware và software.
