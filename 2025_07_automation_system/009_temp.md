Rất hợp lý! Mô hình **Agent độc lập + Storage trung tâm** sẽ giúp hệ thống:

* **Mở rộng dễ dàng** theo chiều ngang (scale agent riêng lẻ)
* **Tái sử dụng dữ liệu** hiệu quả giữa các agent
* **Tự động hóa luồng dữ liệu** theo thời gian
* **Không phụ thuộc thứ tự pipeline**

---

## ✅ Kiến trúc mới: Agent độc lập – giao tiếp qua `storage`

```
agents/
├── agentA/        ← Ví dụ: data_fetcher (chạy định kỳ)
│   ├── agent.py
│   └── config.yaml
├── agentB/        ← Ví dụ: embedding_agent
│   ├── agent.py
│   └── config.yaml
...
storage/
├── agentA_output/    ← output từ agentA (JSON, CSV, v.v.)
├── agentB_output/    ← output từ agentB
```

---

## ✅ Mỗi agent phải định nghĩa:

| Thành phần          | Mục tiêu                                          |
| ------------------- | ------------------------------------------------- |
| `config.yaml`       | Chứa input\_path (thư mục lấy dữ liệu từ storage) |
| `output_path`       | Thư mục agent sẽ ghi kết quả                      |
| `run()`             | Đọc input từ storage → xử lý → ghi output         |
| `schedule` (nếu có) | Đối với agent chạy định kỳ (ví dụ 5 phút/lần)     |

---

## ✅ Ví dụ agent đọc từ `storage/agentA_output/`, ghi sang `storage/agentB_output/`

📄 `agents/agentB/agent.py`

```python
import os
import json
import yaml

class AgentB:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.input_dir = self.config["input_dir"]
        self.output_dir = self.config["output_dir"]
        os.makedirs(self.output_dir, exist_ok=True)

    def run(self):
        input_file = os.path.join(self.input_dir, "latest.json")
        if not os.path.exists(input_file):
            print(f"No input found at {input_file}")
            return

        with open(input_file) as f:
            data = json.load(f)

        result = self.process(data)

        output_file = os.path.join(self.output_dir, "output.json")
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)

        print(f"✅ AgentB saved result to {output_file}")

    def process(self, data):
        # Giả lập xử lý
        return {"processed": True, "input": data}
```

📄 `agents/agentB/config.yaml`

```yaml
input_dir: storage/agentA_output
output_dir: storage/agentB_output
```

---

## ✅ Agent định kỳ (chạy mỗi 5 phút)

📄 `agents/data_fetcher/agent.py`

```python
import time, os, json
from datetime import datetime

class DataFetcherAgent:
    def __init__(self, output_dir="storage/agentA_output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def run_once(self):
        # Fetch dữ liệu mock
        data = {"timestamp": datetime.now().isoformat(), "value": 42}
        out_file = os.path.join(self.output_dir, "latest.json")
        with open(out_file, "w") as f:
            json.dump(data, f)
        print(f"[{datetime.now()}] ✅ DataFetcher wrote to {out_file}")

    def run_forever(self, interval_sec=300):
        while True:
            self.run_once()
            time.sleep(interval_sec)
```

📄 Cách gọi:

```python
if __name__ == "__main__":
    agent = DataFetcherAgent()
    agent.run_forever()
```

---

## ✅ Lợi ích mô hình mới

| Ưu điểm               | Giải thích                                           |
| --------------------- | ---------------------------------------------------- |
| Không phụ thuộc       | Mỗi agent chạy riêng, không chờ nhau                 |
| Đơn giản hóa pipeline | Không cần `depends_on`, không cần shared context     |
| Dễ scale              | Dùng cronjob, Docker, hoặc serverless cho từng agent |
| Kiểm soát chặt I/O    | Input/output qua `storage`, có thể theo dõi và debug |

---

## ✅ Gợi ý tiếp theo

Bạn có thể:

* Tạo `AgentRunner` để chạy 1 agent bằng dòng lệnh (CLI)
* Ghi log và timestamp cho mỗi lần agent chạy
* Dùng `.lock` file để tránh trùng lặp
* Ghi `meta.json` để track version/timestamp của output

---

Bạn muốn mình:

1. Tái cấu trúc lại project mẫu hiện tại theo mô hình này?
2. Tạo sẵn 3 agent mẫu (1 fetcher + 2 xử lý)?
3. Viết sẵn script để launch từng agent tự động hoặc bằng cronjob?

Mình có thể giúp setup toàn bộ theo mô hình này. Bạn chọn bước nào trước?
