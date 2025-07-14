Tuyệt vời! Để hỗ trợ **thu thập lại file cũ** (overwrite), ta sẽ mở rộng `config.yaml` của FetcherAgent để:

* Định nghĩa mỗi agent target có `allow_overwrite: true/false`
* Nếu `true`, fetcher sẽ không kiểm tra `processed.json`, luôn thu thập lại file (và có thể ghi đè)
* Nếu `false`, chỉ thu thập file mới như cũ

---

## ✅ Ví dụ `fetcher/config.yaml` cập nhật

```yaml
targets:
  - name: EmbeddingAgent
    folder: storage/agentB_output
    allow_overwrite: false

  - name: VectorSearchAgent
    folder: storage/agentC_output
    allow_overwrite: true

output_dir: storage/fetcher_output
processed_file: agents/fetcher/processed.json
```

---

## ✅ Cập nhật `fetcher/agent.py` với `allow_overwrite`

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
            allow_overwrite = target.get("allow_overwrite", False)

            if name not in self.processed:
                self.processed[name] = []

            for file in os.listdir(folder):
                if not file.endswith(".json"):
                    continue

                full_path = os.path.join(folder, file)

                # Nếu không cho phép overwrite, bỏ qua file đã xử lý
                if not allow_overwrite and file in self.processed[name]:
                    continue

                with open(full_path) as f:
                    content = json.load(f)

                output_file = os.path.join(
                    self.output_dir,
                    f"{name}_{file.replace('.json','')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
                )
                with open(output_file, "w") as f:
                    json.dump(content, f, indent=2)

                print(f"✅ Collected {file} from {name} → {output_file}")
                if not allow_overwrite:
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

## ✅ Lợi ích và tùy chọn kiểm soát

| Tên thuộc tính           | Ý nghĩa                                         |
| ------------------------ | ----------------------------------------------- |
| `allow_overwrite: true`  | Luôn lấy lại file (ngay cả khi đã lấy trước đó) |
| `allow_overwrite: false` | Chỉ lấy file mới chưa từng thu thập             |

---

Bạn có thể:

* Dùng `allow_overwrite: true` cho các file có tên cố định như `latest.json`, `result.json`
* Dùng `false` cho file theo timestamp như `output_20250714.json`

---

Nếu bạn muốn mình:

* Đóng gói toàn bộ hệ thống fetcher mới thành thư mục mẫu
* Viết luôn `main_fetcher.py` để chạy độc lập
* Tích hợp vào project tổng Multi-Agent

Hãy nói mình biết phần nào cần tiếp theo nhé!
