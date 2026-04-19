Tuyệt vời! Dưới đây là phiên bản **mới nhất, hoàn chỉnh** của dự án Multi-Agent:

🎯 Hỗ trợ:

✅ Input/output tự động
✅ YAML pipeline
✅ `depends_on`, `tags`, `description`
✅ Caching
✅ Log từng bước
✅ Xuất context ra `.json`
✅ **Config riêng per-agent bằng file `config.yaml`**
✅ **Override config per-agent từ YAML pipeline**

---

## 🗂️ Cấu trúc thư mục

```
multi_agent_project/
│
├── agents/
│   ├── base_agent.py
│   ├── pdf_reader/
│   │   ├── agent.py
│   │   └── config.yaml
│   ├── embedding/
│   │   ├── agent.py
│   │   └── config.yaml
│   └── vector_search/
│       ├── agent.py
│       └── config.yaml
│
├── core/
│   ├── agent_context.py
│   ├── agent_manager.py
│   └── pipeline_runner.py
│
├── config/
│   └── pipeline.yaml
│
├── output/
│   └── final_context.json  ← Tự sinh sau khi chạy
│
├── main.py
└── requirements.txt
```

---

## 📄 `agents/base_agent.py`

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseAgent(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def setup(self, config: Dict[str, Any]):
        """Optional: override config"""
        pass

    def depends_on(self) -> List[str]:
        return []

    def tags(self) -> List[str]:
        return []

    def description(self) -> str:
        return self.__class__.__doc__ or "No description"
```

---

## 📄 `agents/pdf_reader/agent.py`

```python
import os
import yaml
from agents.base_agent import BaseAgent

class PdfReaderAgent(BaseAgent):
    def __init__(self):
        self.config = {}
        path = os.path.join(os.path.dirname(__file__), "config.yaml")
        if os.path.exists(path):
            self.config = yaml.safe_load(open(path))

    def name(self):
        return "PdfReaderAgent"

    def setup(self, config):
        self.config.update(config)

    def run(self, input_data):
        file_path = input_data["file_path"]
        prefix = self.config.get("prefix", "[PDF]")
        return {"text": f"{prefix} Extracted from {file_path}"}
```

📄 `agents/pdf_reader/config.yaml`

```yaml
prefix: "[DefaultPDF]"
```

---

## 📄 `agents/embedding/agent.py`

```python
import os
import yaml
from agents.base_agent import BaseAgent

class EmbeddingAgent(BaseAgent):
    """Sinh embedding từ văn bản"""

    def __init__(self):
        self.config = {"dim": 5}
        path = os.path.join(os.path.dirname(__file__), "config.yaml")
        if os.path.exists(path):
            self.config.update(yaml.safe_load(open(path)))

    def name(self):
        return "EmbeddingAgent"

    def setup(self, config):
        self.config.update(config)

    def run(self, input_data):
        text = input_data["text"]
        dim = self.config["dim"]
        return {"embedding": [hash(text + str(i)) % 1000 / 1000.0 for i in range(dim)]}

    def tags(self):
        return ["embedding"]
```

📄 `agents/embedding/config.yaml`

```yaml
dim: 6
```

---

## 📄 `agents/vector_search/agent.py`

```python
import os
import yaml
from agents.base_agent import BaseAgent

class VectorSearchAgent(BaseAgent):
    def __init__(self):
        self.config = {}
        path = os.path.join(os.path.dirname(__file__), "config.yaml")
        if os.path.exists(path):
            self.config = yaml.safe_load(open(path))

    def name(self):
        return "VectorSearchAgent"

    def setup(self, config):
        self.config.update(config)

    def run(self, input_data):
        vector = input_data["vector"]
        top_k = self.config.get("top_k", 3)
        return {"results": [f"doc_{int(x*1000)}" for x in vector[:top_k]]}

    def depends_on(self):
        return ["EmbeddingAgent"]

    def tags(self):
        return ["retrieval"]
```

📄 `agents/vector_search/config.yaml`

```yaml
top_k: 2
```

---

## 📄 `core/agent_context.py`

```python
import os
import json
from datetime import datetime

class AgentContext:
    def __init__(self, cache_enabled=True, export_path="output/final_context.json"):
        self.data = {}
        self.log = []
        self.cache_enabled = cache_enabled
        self.export_path = export_path
        os.makedirs(os.path.dirname(export_path), exist_ok=True)

    def set(self, key, value):
        self.data[key] = value
        self.log.append({
            "timestamp": datetime.now().isoformat(),
            "key": key,
            "value": str(value)[:300]
        })

    def get(self, key):
        return self.data.get(key)

    def has(self, key):
        return key in self.data

    def dump_context(self):
        with open(self.export_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def get_log(self):
        return self.log
```

---

## 📄 `core/agent_manager.py`

```python
class AgentManager:
    def __init__(self):
        self.agents = {}

    def register(self, agent):
        self.agents[agent.name()] = agent

    def get(self, name):
        return self.agents.get(name)
```

---

## 📄 `core/pipeline_runner.py`

```python
import yaml

class PipelineRunner:
    def __init__(self, agent_manager, context, config_path):
        self.manager = agent_manager
        self.context = context
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def run(self):
        completed = set()
        for step in self.config["pipeline"]:
            agent = self.manager.get(step["type"])
            agent_name = agent.name()
            print(f"\n🔧 Running: {agent_name}")

            for dep in agent.depends_on():
                if dep not in completed:
                    raise Exception(f"Agent {agent_name} depends on {dep}")

            cache_key = f"CACHE_{agent_name}"
            if self.context.cache_enabled and self.context.has(cache_key):
                print(f"✅ [Cache Hit] Skipping {agent_name}")
                completed.add(agent_name)
                continue

            # Inject config nếu có
            agent.setup(step.get("config", {}))

            resolved_inputs = {}
            for k, v in step.get("inputs", {}).items():
                resolved_inputs[k] = self.context.get(v[1:]) if isinstance(v, str) and v.startswith("$") else v

            result = agent.run(resolved_inputs)

            for k, alias in step.get("outputs", {}).items():
                self.context.set(alias, result[k])

            if self.context.cache_enabled:
                self.context.set(cache_key, True)

            completed.add(agent_name)

        self.context.dump_context()
```

---

## 📄 `config/pipeline.yaml`

```yaml
pipeline:
  - name: reader
    type: PdfReaderAgent
    config:
      prefix: "[CustomPDF]"
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

  - name: retriever
    type: VectorSearchAgent
    config:
      top_k: 3
    inputs:
      vector: $doc_embedding
    outputs:
      results: search_results
```

---

## 📄 `main.py`

```python
from core.agent_manager import AgentManager
from core.agent_context import AgentContext
from core.pipeline_runner import PipelineRunner

from agents.pdf_reader.agent import PdfReaderAgent
from agents.embedding.agent import EmbeddingAgent
from agents.vector_search.agent import VectorSearchAgent

def main():
    manager = AgentManager()
    context = AgentContext()

    manager.register(PdfReaderAgent())
    manager.register(EmbeddingAgent())
    manager.register(VectorSearchAgent())

    runner = PipelineRunner(manager, context, "config/pipeline.yaml")
    runner.run()

    print("\n📦 Final Context:")
    for k, v in context.data.items():
        print(f"{k}: {v}")

    print("\n📝 Log:")
    for entry in context.get_log():
        print(f"[{entry['timestamp']}] {entry['key']} = {entry['value']}")

if __name__ == "__main__":
    main()
```

---

## 📄 `requirements.txt`

```text
pyyaml
```

---

## ✅ Cách chạy

```bash
pip install -r requirements.txt
python main.py
```

---

## 📌 Kết quả:

* Log chi tiết quá trình
* Context đầy đủ lưu ra `output/final_context.json`
* Config từng agent có thể tuỳ chỉnh qua YAML hoặc file riêng

---

Bạn có muốn:

* Đóng gói thành file `.zip` tải về?
* Tích hợp vẽ sơ đồ DAG pipeline?
* Thêm web UI cho cấu hình và theo dõi agent?

Mình có thể giúp bạn ở bước tiếp theo.
