Dưới đây là **bộ tiêu chuẩn mở rộng** cho từng agent trong hệ thống Multi-Agent được route bởi một `AgentManager`. Các tiêu chuẩn này giúp quản lý tốt hơn về dữ liệu, trạng thái, phụ thuộc, log, cấu hình và tích hợp mô-đun hóa.

---

## ✅ **1. Tiêu chuẩn tổng quát đầy đủ cho Agent (Python)**

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseAgent(ABC):
    @abstractmethod
    def name(self) -> str:
        """Tên duy nhất của agent (dùng để định tuyến)."""
        pass

    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Hàm chính xử lý dữ liệu đầu vào và trả về kết quả."""
        pass

    @abstractmethod
    def input_schema(self) -> Dict[str, str]:
        """Định nghĩa schema cho input (dùng để kiểm tra hợp lệ)."""
        pass

    @abstractmethod
    def output_schema(self) -> Dict[str, str]:
        """Định nghĩa schema cho output."""
        pass

    def depends_on(self) -> List[str]:
        """Danh sách tên agent phải chạy trước (nếu có)."""
        return []

    def setup(self, config: Dict[str, Any]) -> None:
        """Nhận config để khởi tạo agent nếu cần (load model, path, API key, v.v.)."""
        self.config = config

    def input_file_mode(self) -> bool:
        """Trả về True nếu agent dùng file thay vì dict input (như đọc PDF, ảnh)."""
        return False

    def output_file_mode(self) -> bool:
        """Trả về True nếu output là file (để agent manager ghi ra disk)."""
        return False

    def description(self) -> str:
        """Mô tả ngắn về chức năng của agent, hỗ trợ sinh sơ đồ hoặc bảng."""
        return "No description provided."

    def tags(self) -> List[str]:
        """Danh sách các tag phân loại (ví dụ: 'preprocess', 'rag', 'llm')."""
        return []

    def reset(self) -> None:
        """Đặt lại trạng thái agent (nếu agent có trạng thái)."""
        pass
```

---

## ✅ **2. Ý nghĩa và lợi ích của các tiêu chuẩn bổ sung**

| Tiêu chuẩn bổ sung   | Mục đích chính                                                                 |
| -------------------- | ------------------------------------------------------------------------------ |
| `depends_on()`       | Hỗ trợ tự động xác định thứ tự chạy pipeline.                                  |
| `setup(config)`      | Cho phép inject cấu hình bên ngoài (như API key, đường dẫn, mô hình AI, v.v.). |
| `input_file_mode()`  | Agent xử lý theo file (ví dụ: file ảnh, âm thanh).                             |
| `output_file_mode()` | Agent sẽ sinh file đầu ra (ví dụ: PDF, JSON output).                           |
| `description()`      | Hữu ích khi hiển thị agent trong dashboard, docs hoặc auto-gen sơ đồ.          |
| `tags()`             | Dễ lọc agent theo loại chức năng khi hiển thị UI hoặc routing tự động.         |
| `reset()`            | Hữu ích trong long-running app (clear state, session).                         |

---

## ✅ **3. Ví dụ Agent có đầy đủ tiêu chuẩn**

```python
class EmbeddingAgent(BaseAgent):
    def name(self):
        return "embedding"

    def run(self, input_data: Dict[str, Any]):
        text = input_data["text"]
        # Giả lập tạo vector embedding
        return {"embedding": [0.1, 0.2, 0.3]}

    def input_schema(self):
        return {"text": "string"}

    def output_schema(self):
        return {"embedding": "List[float]"}

    def description(self):
        return "Tạo embedding từ đoạn văn bản."

    def tags(self):
        return ["embedding", "preprocess"]
```

---

## ✅ **4. Kết hợp với AgentManager**

Trong `AgentManager`, bạn có thể dùng các hàm `depends_on()`, `input_schema()`... để:

* Kiểm tra hợp lệ input
* Tự động xác định pipeline chạy theo thứ tự phụ thuộc
* Sinh docs tự động cho toàn bộ hệ thống
* Hỗ trợ load cấu hình hoặc reset toàn bộ agents

---

## ✅ **5. Bonus: Chuẩn hóa thư mục mỗi Agent**

```
agents/
│
├── embedding_agent/
│   ├── __init__.py
│   ├── agent.py          # class EmbeddingAgent(BaseAgent)
│   ├── config.yaml       # config riêng cho agent
│   ├── output/           # chứa kết quả output nếu dùng output_file_mode
│   └── resources/        # mô hình, tokenizer nếu có
```

---

Nếu bạn muốn, mình có thể giúp bạn:

* Tạo bộ khởi động (starter kit) gồm nhiều agent + manager
* Viết template YAML cho việc cấu hình pipeline
* Sinh sơ đồ routing tự động từ agent dependency

Bạn muốn mình hỗ trợ phần nào tiếp theo?
