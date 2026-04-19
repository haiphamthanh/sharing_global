Dưới đây là một ví dụ **toàn bộ project sample** hệ thống Multi-Agent gồm:

* 3 agent: `PdfReaderAgent`, `EmbeddingAgent`, `VectorSearchAgent`
* Một `AgentManager` để quản lý agent
* Một `AgentContext` để lưu input/output
* Một `PipelineRunner` để chạy pipeline dựa trên file YAML

---

## 🗂️ Cấu trúc thư mục dự án

```
multi_agent_project/
│
├── agents/
│   ├── base_agent.py
│   ├── pdf_reader.py
│   ├── embedding.py
│   └── vector_search.py
│
├── core/
│   ├── agent_context.py
│   ├── agent_manager.py
│   └── pipeline_runner.py
│
├── config/
│   └── pipeline.yaml
│
├── main.py
└── requirements.txt
```

---

## 📄 `agents/base_agent.py`

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
```

---

## 📄 `agents/pdf_reader.py`

```python
from agents.base_agent import BaseAgent

class PdfReaderAgent(BaseAgent):
    def name(self):
        return "PdfReaderAgent"

    def run(self, input_data):
        file_path = input_data["file_path"]
        # Giả lập đọc file
        return {"text": f"Extracted text from {file_path}"}
```

---

## 📄 `agents/embedding.py`

```python
from agents.base_agent import BaseAgent

class EmbeddingAgent(BaseAgent):
    def name(self):
        return "EmbeddingAgent"

    def run(self, input_data):
        text = input_data["text"]
        return {"embedding": [hash(text) % 1_000 / 1_000.0 for _ in range(5)]}
```

---

## 📄 `agents/vector_search.py`

```python
from agents.base_agent import BaseAgent

class VectorSearchAgent(BaseAgent):
    def name(self):
        return "VectorSearchAgent"

    def run(self, input_data):
        vector = input_data["vector"]
        return {"results": [f"doc_{int(x*1000)}" for x in vector]}
```

---

## 📄 `core/agent_context.py`

```python
class AgentContext:
    def __init__(self):
        self.data = {}

    def set(self, key: str, value):
        self.data[key] = value

    def get(self, key: str):
        return self.data.get(key)

    def has(self, key: str):
        return key in self.data
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
        for step in self.config["pipeline"]:
            agent = self.manager.get(step["type"])
            resolved_inputs = {}
            for k, v in step.get("inputs", {}).items():
                if isinstance(v, str) and v.startswith("$"):
                    resolved_inputs[k] = self.context.get(v[1:])
                else:
                    resolved_inputs[k] = v
            result = agent.run(resolved_inputs)
            for k, alias in step.get("outputs", {}).items():
                self.context.set(alias, result[k])
```

---

## 📄 `config/pipeline.yaml`

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
    inputs:
      text: $doc_text
    outputs:
      embedding: doc_embedding

  - name: retriever
    type: VectorSearchAgent
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

from agents.pdf_reader import PdfReaderAgent
from agents.embedding import EmbeddingAgent
from agents.vector_search import VectorSearchAgent

def main():
    manager = AgentManager()
    context = AgentContext()

    # Đăng ký agents
    manager.register(PdfReaderAgent())
    manager.register(EmbeddingAgent())
    manager.register(VectorSearchAgent())

    runner = PipelineRunner(manager, context, "config/pipeline.yaml")
    runner.run()

    # Hiển thị kết quả cuối cùng
    print("=== Final Context ===")
    for k, v in context.data.items():
        print(f"{k}: {v}")

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

## 📌 Output mẫu

```
=== Final Context ===
doc_text: Extracted text from sample.pdf
doc_embedding: [0.432, 0.432, 0.432, 0.432, 0.432]
search_results: ['doc_432', 'doc_432', 'doc_432', 'doc_432', 'doc_432']
```

---

Nếu bạn muốn:

* Xuất context ra file `.json`
* Thêm logger cho từng bước
* Thêm `depends_on`, `tags`, hoặc caching…

Mình có thể mở rộng tiếp. Bạn muốn mình thêm phần nào trước?
