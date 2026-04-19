Tuyệt vời! Ta sẽ mở rộng theo **hướng đơn giản** nhưng có **menu tương tác** để chọn *agent* và *tác vụ* cần chạy.

---

## ✅ Mục tiêu

* Giao diện dòng lệnh có menu chọn:

  1. Agent (`finance_jira`, `ecommerce_ticket`, …)
  2. Tác vụ xử lý tương ứng (`preprocess_v1`, `preprocess_v2`, …)
* Gọi chính xác file xử lý tương ứng trong `modules/` từng service.

---

## ✅ Cấu trúc cập nhật

```plaintext
auto_process_manager/
├── orchestrator_menu.py         # Menu chính
├── services/
│   ├── finance_jira_service/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── modules/
│   │   │   ├── preprocess_v1.py
│   │   │   └── preprocess_v2.py
│   │   └── menu_config.json     # Menu khai báo các tác vụ
│   └── ecommerce_ticket_service/
│       ├── ...
```

---

## ✅ 1. `menu_config.json` trong từng service

### `services/finance_jira_service/menu_config.json`

```json
{
  "tasks": {
    "Preprocess V1": "preprocess_v1",
    "Preprocess V2": "preprocess_v2"
  }
}
```

> Mỗi mục gồm: tên hiển thị → tên file `.py` trong `modules/`.

---

## ✅ 2. Mỗi file xử lý có hàm `run(config)`

### `services/finance_jira_service/modules/preprocess_v1.py`

```python
def run(config):
    print("[finance_jira][v1] Running preprocessing...")
    print(f"Using DB: {config['db_index']}")
```

### `services/finance_jira_service/modules/preprocess_v2.py`

```python
def run(config):
    print("[finance_jira][v2] Running preprocessing...")
    print(f"Using DB: {config['db_index']}")
```

---

## ✅ 3. `orchestrator_menu.py`: Menu chọn agent + task

```python
import json
import importlib.util
import os

SERVICES_DIR = "services"

def list_services():
    return [d for d in os.listdir(SERVICES_DIR) if d.endswith("_service")]

def load_menu(service_name):
    path = os.path.join(SERVICES_DIR, service_name, "menu_config.json")
    with open(path, "r") as f:
        return json.load(f)

def load_config(service_name):
    config_path = os.path.join(SERVICES_DIR, service_name, "config.py")
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config.CONFIG

def run_task(service_name, module_name, config):
    module_path = os.path.join(SERVICES_DIR, service_name, "modules", f"{module_name}.py")
    spec = importlib.util.spec_from_file_location("task_module", module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.run(config)

def main():
    print("🧠 Auto Process Manager Menu")

    # Chọn agent
    services = list_services()
    for idx, s in enumerate(services):
        print(f"{idx + 1}. {s}")
    s_idx = int(input("Chọn agent: ")) - 1
    service_name = services[s_idx]

    # Chọn task
    menu = load_menu(service_name)
    tasks = menu["tasks"]
    task_names = list(tasks.keys())
    for idx, t in enumerate(task_names):
        print(f"{idx + 1}. {t}")
    t_idx = int(input("Chọn tác vụ: ")) - 1
    task_name = task_names[t_idx]
    task_module = tasks[task_name]

    print(f"\n▶️ Running: {service_name} → {task_name}\n")
    config = load_config(service_name)
    run_task(service_name, task_module, config)

if __name__ == "__main__":
    main()
```

---

## ✅ Cách chạy

```bash
cd auto_process_manager
python orchestrator_menu.py
```

### Ví dụ dòng lệnh:

```
🧠 Auto Process Manager Menu
1. finance_jira_service
2. ecommerce_ticket_service
Chọn agent: 1
1. Preprocess V1
2. Preprocess V2
Chọn tác vụ: 1

▶️ Running: finance_jira_service → Preprocess V1

[finance_jira][v1] Running preprocessing...
Using DB: db/process_v1.index
```

---

## 📌 Ưu điểm:

* ✅ Dễ mở rộng: chỉ cần thêm file `.py` và khai báo trong `menu_config.json`
* ✅ Không cần hardcode module trong orchestrator
* ✅ Mỗi agent tự chứa logic riêng – orchestrator chỉ “gọi đúng người”

---

Bạn có muốn mình tạo thêm tùy chọn:

* Thêm args dòng lệnh (`--service finance_jira --task preprocess_v2`)?
* Lưu log kết quả chạy?
* Chạy nhiều task liên tiếp không cần chọn lại menu?

Mình có thể mở rộng ngay nếu bạn cần!
