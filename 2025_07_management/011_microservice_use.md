Dưới đây là một **Bash script** giúp bạn tạo nhanh khung thư mục microservice như đã mô tả, **không cần Docker**, chỉ tạo file/folder cơ bản để bắt đầu dự án:

---

## ✅ Bash Script: `create_microservices.sh`

```bash
#!/bin/bash

# Danh sách các service bạn muốn tạo
services=("finance_jira_service" "ecommerce_ticket_service")

# Tạo thư mục gốc
mkdir -p auto_process_manager/services
mkdir -p auto_process_manager/shared_libs/ai_agent

# Tạo shared_libs
echo "Creating shared_libs..."
touch auto_process_manager/shared_libs/logger.py
touch auto_process_manager/shared_libs/utils.py
touch auto_process_manager/shared_libs/ai_agent/command_parser.py

# Tạo từng service
for service in "${services[@]}"; do
  echo "Creating service: $service"
  base="auto_process_manager/services/$service"

  mkdir -p "$base/raw"
  mkdir -p "$base/pre_processing"
  mkdir -p "$base/db"
  mkdir -p "$base/modules"
  mkdir -p "$base/menu"

  touch "$base/main.py"
  touch "$base/config.py"
  touch "$base/raw/.keep"
  touch "$base/pre_processing/__init__.py"
  touch "$base/db/.keep"
  touch "$base/modules/__init__.py"
  touch "$base/menu/loader.py"
done

echo "✅ Microservice structure created successfully!"
```

---

## 📌 Hướng dẫn sử dụng

1. **Lưu script** trên vào file, ví dụ `create_microservices.sh`
2. Cấp quyền thực thi:

   ```bash
   chmod +x create_microservices.sh
   ```
3. **Chạy script**:

   ```bash
   ./create_microservices.sh
   ```

---

Sau khi chạy, bạn sẽ có cấu trúc thư mục như sau:

```plaintext
auto_process_manager/
├── services/
│   ├── finance_jira_service/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── raw/
│   │   ├── pre_processing/
│   │   ├── db/
│   │   ├── modules/
│   │   └── menu/
│   └── ecommerce_ticket_service/
│       ├── ...
├── shared_libs/
│   ├── logger.py
│   ├── utils.py
│   └── ai_agent/
│       └── command_parser.py
```

---

Nếu bạn muốn mở rộng thêm service khác, chỉ cần thêm tên vào mảng `services=(...)`.

Bạn muốn mình tạo luôn sẵn các file `.py` cơ bản có nội dung mẫu như `main.py` khởi chạy và `config.py` với template JSON không?
