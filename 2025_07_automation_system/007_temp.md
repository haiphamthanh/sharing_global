Hoàn toàn được — để **hỗ trợ `config riêng cho mỗi loại agent`**, bạn nên tổ chức như sau:

---

## ✅ Cách 1: Để config riêng trong mỗi agent (ưu tiên gọn)

### 📁 Cấu trúc

```
agents/
├── embedding/
│   ├── agent.py
│   └── config.yaml      ← config riêng
├── pdf_reader/
│   ├── agent.py
│   └── config.yaml
```

### 🧠 Agent tự load config riêng (nếu có)

📄 `agents/embedding/agent.py`:

```python
import os
import yaml
from agents.base_agent import BaseAgent

class EmbeddingAgent(BaseAgent):
    def __init__(self):
        # Load config.yaml trong thư mục hiện tại
        path = os.path.join(os.path.dirname(__file__), "config.yaml")
        self.config = yaml.safe_load(open(path, "r"))

    def name(self):
        return "EmbeddingAgent"

    def run(self, input_data):
        text = input_data["text"]
        dim = self.config.get("dim", 5)
        return {"embedding": [hash(text) % 1000 / 1000.0 for _ in range(dim)]}
```

📄 `agents/embedding/config.yaml`:

```yaml
dim: 8
```

**✅ Ưu điểm:** tách biệt, sạch, dễ scale
**⛔ Nhược:** không thể chỉnh config từng instance từ pipeline YAML (dưới đây là cách mở rộng thêm)

---

## ✅ Cách 2: Cho phép **pipeline YAML override cấu hình** từng agent (mạnh hơn)

### 📄 Cập nhật `pipeline.yaml`

```yaml
pipeline:
  - name: reader
    type: PdfReaderAgent
    inputs:
      file_path: "sample.pdf"
    outputs:
      text: doc_text

  - name: embedder
    type: EmbeddingAgent
    config:
      dim: 10
    inputs:
      text: $doc_text
    outputs:
      embedding: doc_embedding
```

### 📄 Cập nhật `PipelineRunner` để inject `config`

📄 `core/pipeline_runner.py` (trích đoạn cập nhật):

```python
            config_override = step.get("config", {})
            if hasattr(agent, "setup") and callable(getattr(agent, "setup")):
                agent.setup(config_override)
```

### 📄 Agent hỗ trợ `setup(config)`

📄 `agents/embedding/agent.py`:

```python
class EmbeddingAgent(BaseAgent):
    def __init__(self):
        self.config = {"dim": 5}  # default

    def setup(self, config):
        self.config.update(config)

    def name(self):
        return "EmbeddingAgent"

    def run(self, input_data):
        text = input_data["text"]
        dim = self.config.get("dim", 5)
        return {"embedding": [hash(text) % 1000 / 1000.0 for _ in range(dim)]}
```

---

## ✅ Bonus: Hỗ trợ cả hai cơ chế (file config + override YAML)

Bạn có thể:

* Trong `__init__()` load `config.yaml` nếu có
* Trong `setup()`, nhận config mới và `update()` vào config hiện tại

Kết quả:
🔁 File `config.yaml` là default
🔁 YAML trong pipeline là override cho từng pipeline cụ thể

---

## ✅ Tổng kết các cách thêm config

| Cách                       | Dễ dùng | Linh hoạt | Scale |
| -------------------------- | ------- | --------- | ----- |
| File riêng trong mỗi agent | ✅       | ❌         | ✅     |
| Cấu hình YAML override     | ✅       | ✅         | ✅     |
| Kết hợp cả hai             | ✅✅      | ✅✅        | ✅✅    |

---

Bạn muốn mình **update lại toàn bộ project mẫu hiện tại để hỗ trợ cả hai kiểu config (file + override)** luôn không? Nếu có, mình sẽ đưa luôn mã nguồn hoàn chỉnh.
