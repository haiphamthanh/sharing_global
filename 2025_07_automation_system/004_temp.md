Để **tự động quản lý việc kết nối output của agent này thành input của agent kia**, bạn cần xây dựng một **pipeline engine có khả năng định tuyến tự động** dựa trên cấu hình. Cách làm phổ biến là:

---

## ✅ **1. Dùng cấu hình Pipeline có khai báo ràng buộc input/output**

### ▶ Cấu hình YAML dạng chuẩn:

```yaml
pipeline:
  - name: reader
    type: PdfReaderAgent
    inputs:
      file_path: "input/sample.pdf"
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
      results: search_result
```

> Trong đó:
>
> * `outputs.key = alias`
> * `inputs.key = $alias` để chỉ rõ input lấy từ output trước đó.

---

## ✅ **2. AgentManager tự động resolve input**

```python
class PipelineRunner:
    def __init__(self, agent_manager, config: dict):
        self.agent_manager = agent_manager
        self.config = config
        self.context = AgentContext()

    def run(self):
        for step in self.config["pipeline"]:
            agent = self.agent_manager.get(step["type"])
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

## ✅ **3. Cách hoạt động**

| Bước    | Input (tự động)              | Output (được đặt tên)       |
| ------- | ---------------------------- | --------------------------- |
| Agent 1 | file\_path (cứng)            | text → alias `doc_text`     |
| Agent 2 | text ← lấy từ `$doc_text`    | embedding → `doc_embedding` |
| Agent 3 | vector ← từ `$doc_embedding` | results → `search_result`   |

Mọi `output` từ bước trước được đặt tên và dùng lại bởi bước sau **không cần hardcode**.

---

## ✅ **4. Lợi ích của cấu hình này**

| Ưu điểm                        | Mô tả                               |
| ------------------------------ | ----------------------------------- |
| ✅ Tự động routing input/output | Không cần viết code truyền thủ công |
| ✅ Tái sử dụng output nhiều nơi | Một output dùng cho nhiều bước      |
| ✅ Dễ debug & trace dữ liệu     | Mỗi output có tên alias cụ thể      |
| ✅ Dễ sinh sơ đồ pipeline       | Có thể vẽ sơ đồ DAG từ config       |

---

## ✅ **5. Bonus: Visual DAG sơ đồ tự động**

Từ cấu hình trên, bạn có thể sinh sơ đồ như sau:

```
[input] → reader → doc_text → embedder → doc_embedding → retriever → search_result
```

Hoặc dùng `networkx` + `matplotlib` để auto vẽ DAG.

---

## ✅ Tổng kết: Các thành phần cần có

| Thành phần        | Mục đích                                     |
| ----------------- | -------------------------------------------- |
| `Agent` interface | Khai báo rõ input/output                     |
| `AgentContext`    | Lưu output alias của từng bước               |
| `Pipeline config` | Định nghĩa input/output mapping              |
| `PipelineRunner`  | Đọc cấu hình, resolve input, chạy từng agent |
| `AgentManager`    | Đăng ký agent theo `type`                    |

---

Nếu bạn muốn mình tạo cho bạn một **pipeline mẫu có 3 agent**, mình có thể cung cấp file `.yaml`, Python runner và ví dụ thực thi ngay.

Bạn có muốn mẫu như vậy không?
