Quản lý **input và output giữa các agent** hiệu quả là **trái tim của hệ thống Multi-Agent**. Một hệ thống tốt cần:

* **Theo dõi dữ liệu sinh ra từ mỗi agent**
* **Cung cấp input đúng cho agent tiếp theo**
* **Lưu lịch sử hoặc cache để debug**
* **Hỗ trợ chạy lại từng bước nếu cần**

---

## ✅ Cách tiếp cận tổng quát: **AgentContext** + **DataStore**

> Gợi ý thiết kế mô-đun quản lý input/output theo hướng module hóa, rõ ràng, có thể mở rộng.

---

## 1. `AgentContext`: Bộ nhớ dùng chung giữa các agent

Đây là "bộ não" giữ toàn bộ input/output/tạm thời của các agent.

```python
class AgentContext:
    def __init__(self):
        self.data = {}  # Dict[str, Any] dùng để lưu input/output từng agent
        self.cache = {}  # Cache tạm thời nếu cần
        self.metadata = {}  # Ghi log, thời gian, trạng thái, v.v.

    def set(self, key: str, value: Any):
        self.data[key] = value

    def get(self, key: str) -> Any:
        return self.data.get(key)

    def has(self, key: str) -> bool:
        return key in self.data

    def clear(self):
        self.data.clear()
```

---

## 2. `AgentManager` sử dụng `AgentContext`

```python
class AgentManager:
    def __init__(self):
        self.agents = {}
        self.context = AgentContext()

    def register(self, agent):
        self.agents[agent.name()] = agent

    def run_agent(self, agent_name: str, input_keys: List[str], output_key: str):
        agent = self.agents[agent_name]
        
        input_data = {k: self.context.get(k) for k in input_keys if self.context.has(k)}
        output = agent.run(input_data)
        
        self.context.set(output_key, output)
        return output
```

---

## 3. Cấu hình pipeline YAML (hoặc JSON) để tự động hóa

```yaml
pipeline:
  - name: "pdf_reader"
    input_keys: ["file_path"]
    output_key: "doc_text"

  - name: "embedding"
    input_keys: ["doc_text"]
    output_key: "embedding_vector"

  - name: "search"
    input_keys: ["embedding_vector"]
    output_key: "top_documents"
```

Quy trình:

* AgentManager đọc pipeline này
* Mapping input từ `context`
* Chạy agent → lưu `output_key` vào context → tiếp tục

---

## 4. Visual hóa context giúp debug

Bạn có thể in trạng thái `context` sau mỗi bước:

```python
def print_context(ctx: AgentContext):
    for k, v in ctx.data.items():
        print(f"[{k}] = {str(v)[:200]}")
```

---

## 5. Tích hợp output vào file (nếu cần)

Mở rộng `AgentContext` để lưu kết quả vào `./outputs/`:

```python
import json
import os

class FileBackedAgentContext(AgentContext):
    def __init__(self, output_dir="outputs"):
        super().__init__()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def set(self, key: str, value: Any):
        super().set(key, value)
        with open(f"{self.output_dir}/{key}.json", "w") as f:
            json.dump(value, f, indent=2)
```

---

## ✅ Tóm lại: Quản lý hiệu quả gồm

| Thành phần               | Vai trò                                  |
| ------------------------ | ---------------------------------------- |
| `AgentContext`           | Nơi lưu toàn bộ input/output trung gian  |
| `input_keys/output_key`  | Xác định rõ agent nhận gì và tạo gì      |
| `AgentManager`           | Điều phối toàn bộ agent chạy theo thứ tự |
| `Pipeline config`        | YAML hoặc JSON cấu hình luồng chạy       |
| `File output` (tùy chọn) | Ghi log, trace, debug hoặc reuse kết quả |

---

Nếu bạn đang có một số agent cụ thể và muốn quản lý I/O giữa chúng, mình có thể giúp viết sẵn pipeline mẫu hoặc system scaffold cho bạn. Bạn muốn ví dụ với các agent nào?
