Hoàn hảo! Dưới đây là thiết kế chi tiết cho agent **Fetcher** với khả năng:

---

## ✅ Chức năng của Fetcher Agent:

| Chức năng                                                                | Mô tả |
| ------------------------------------------------------------------------ | ----- |
| 📥 Quét output folder của các agent khác đã đăng ký                       |       |
| 📁 Ghi dữ liệu gom về vào thư mục `storage/fetcher_output/`               |       |
| 🧠 Đánh dấu file đã xử lý (tránh lặp) bằng file `.done` hoặc database nhỏ |       |
| 🔁 Hỗ trợ chạy định kỳ (mỗi 5 phút hoặc theo yêu cầu)                     |       |

---

## 🗂️ Cấu trúc

```
agents/
├── fetcher/
│   ├── agent.py
│   ├── config.yaml
│   └── processed.json  ← lưu tên file đã thu thập
```

---

## 📄 `fetcher/config.yaml`

```yaml
targets:
  - name: EmbeddingAgent
    folder: storage/agentB_output
  - name: VectorSearchAgent
    folder: storage/agentC_output
output_dir: storage/fetcher_output
processed_file: agents/fetcher/processed.json
```

---

## 📄 `fetcher/agent.py`

```python
import os, json, yaml
from datetime import datetime

class FetcherAgent:
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "config.yaml")
        with open(path) as f:
            self.config = yaml.safe_load(f)

        self.targets = self.config["targets"]
        self.output_dir = self.config["output_dir"]
        self.processed_file = self.config["processed_file"]

        os.makedirs(self.output_dir, exist_ok=True)
        self._load_processed()

    def _load_processed(self):
        if os.path.exists(self.processed_file):
            self.processed = json.load(open(self.processed_file))
        else:
            self.processed = {}

    def _save_processed(self):
        with open(self.processed_file, "w") as f:
            json.dump(self.processed, f, indent=2)

    def run_once(self):
        collected = []

        for target in self.targets:
            folder = target["folder"]
            name = target["name"]
            if name not in self.processed:
                self.processed[name] = []

            for file in os.listdir(folder):
                full_path = os.path.join(folder, file)
                if file.endswith(".json") and file not in self.processed[name]:
                    with open(full_path) as f:
                        content = json.load(f)

                    output_file = os.path.join(
                        self.output_dir,
                        f"{name}_{file.replace('.json','')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
                    )
                    with open(output_file, "w") as f:
                        json.dump(content, f, indent=2)

                    print(f"✅ Collected {file} from {name} → {output_file}")
                    self.processed[name].append(file)
                    collected.append(output_file)

        self._save_processed()
        if not collected:
            print("⚠️ No new files to collect.")

    def run_forever(self, interval_sec=300):
        import time
        while True:
            self.run_once()
            time.sleep(interval_sec)
```

---

## ✅ Cách sử dụng

```bash
python agents/fetcher/agent.py  # Chạy 1 lần
hoặc
agent = FetcherAgent(); agent.run_forever(300)  # Chạy mỗi 5 phút
```

---

## ✅ Gợi ý mở rộng

| Tính năng                                   | Mô tả                                 |
| ------------------------------------------- | ------------------------------------- |
| `.lock` file                                | Đảm bảo chỉ 1 tiến trình fetcher chạy |
| Ghi log `meta.json` cho mỗi file fetch được |                                       |
| Lọc file theo thời gian/cấu trúc tên        |                                       |

---

## ✅ Tóm tắt luồng hoạt động

1. Đọc `config.yaml` để biết thư mục của các agent
2. Quét thư mục, kiểm tra `.json` chưa thu thập
3. Ghi vào `storage/fetcher_output/` (đặt tên theo agent)
4. Cập nhật `processed.json` để tránh trùng lặp

---

Bạn có muốn mình:

* Tích hợp fetcher này vào hệ thống project mẫu đang xây?
* Đóng gói thành 1 script độc lập (`fetcher_runner.py`)?
* Sinh log file riêng cho mỗi lần fetch?

Bạn chọn phần nào trước để mình code tiếp?
