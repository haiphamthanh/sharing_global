Tuyệt vời! Dưới đây là bản **hoàn chỉnh** cho **hướng đơn giản khởi đầu**: mỗi `service` (agent) là một CLI độc lập, được orchestrator gọi bằng `subprocess`.

---

## ✅ 1. Cấu trúc thư mục gợi ý

```plaintext
auto_process_manager/
├── orchestrator.py             # Điều phối gọi các agent
├── services/
│   ├── finance_jira_service/
│   │   ├── main.py             # Entry point
│   │   ├── config.py           # Cấu hình
│   │   └── modules/
│   │       └── processor.py    # Tác vụ xử lý
│   └── ecommerce_ticket_service/
│       ├── main.py
│       ├── config.py
│       └── modules/
│           └── processor.py
```

---

## ✅ 2. Nội dung từng file

### `services/finance_jira_service/config.py`

```python
CONFIG = {
    "project": "finance_jira",
    "preprocess_version": "v1",
    "db_index": "db/process_v1.index"
}
```

### `services/finance_jira_service/modules/processor.py`

```python
def run_pipeline(config):
    print(f"[finance_jira] 🔧 Đang chạy pipeline version: {config['preprocess_version']}")
    print(f"[finance_jira] 💾 Load DB index: {config['db_index']}")
    # Giả lập xử lý
    print("[finance_jira] ✅ Xử lý xong")
```

### `services/finance_jira_service/main.py`

```python
from config import CONFIG
from modules.processor import run_pipeline

def main():
    print("[finance_jira] 🚀 Bắt đầu agent...")
    run_pipeline(CONFIG)

if __name__ == "__main__":
    main()
```

> Các file trong `ecommerce_ticket_service/` tương tự, chỉ đổi `project` và thông tin xử lý.

---

## ✅ 3. orchestrator.py – Điều phối đơn giản

```python
import subprocess

def run_agent(service_path):
    print(f"\n▶️ Running agent: {service_path}")
    subprocess.run(["python", f"{service_path}/main.py"])

if __name__ == "__main__":
    print("🧠 Auto Process Manager Orchestrator\n")

    agents = [
        "services/finance_jira_service",
        "services/ecommerce_ticket_service"
    ]

    for agent in agents:
        run_agent(agent)

    print("\n✅ All agents finished!")
```

---

## ✅ 4. Cách chạy

```bash
cd auto_process_manager
python orchestrator.py
```

### Kết quả in ra ví dụ:

```
🧠 Auto Process Manager Orchestrator

▶️ Running agent: services/finance_jira_service
[finance_jira] 🚀 Bắt đầu agent...
[finance_jira] 🔧 Đang chạy pipeline version: v1
[finance_jira] 💾 Load DB index: db/process_v1.index
[finance_jira] ✅ Xử lý xong

▶️ Running agent: services/ecommerce_ticket_service
[ecommerce_ticket] 🚀 Bắt đầu agent...
[ecommerce_ticket] 🔧 Đang chạy pipeline version: v2
[ecommerce_ticket] 💾 Load DB index: db/process_v2.index
[ecommerce_ticket] ✅ Xử lý xong

✅ All agents finished!
```

---

Bạn có muốn mình tạo thêm:

* Script bash tự tạo các file/folder ở trên?
* Bổ sung khả năng truyền tham số (dùng argparse)?
* Chạy song song bằng `multiprocessing`?

Hoặc muốn chuyển sang chế độ "chạy theo từng tác vụ được giao từ orchestrator"?
