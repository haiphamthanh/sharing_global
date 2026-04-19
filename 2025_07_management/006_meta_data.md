Tuyệt vời! Mình sẽ giúp bạn:

---

## ✅ 1. Chuẩn hoá `meta.json` cho mỗi feature

Tạo thêm file `meta.json` trong mỗi thư mục `modules/<feature_name>/` với cấu trúc như sau:

```json
{
  "name": "feature3_bao_cao",
  "title": "Tạo báo cáo từ dữ liệu Jira",
  "description": "Sinh báo cáo chi tiết hàng tháng từ dữ liệu Jira dự án Finance, phân tích theo tag, thời gian, và trạng thái ticket.",
  "tags": ["báo cáo", "jira", "ticket", "finance"]
}
```

---

## ✅ 2. Viết hàm load danh sách features kèm meta

Tạo file `menu/enum.py`:

```python
# menu/enum.py
import json
from pathlib import Path

MODULE_DIR = Path("modules")

def load_feature_meta():
    """Trả về danh sách dict chứa thông tin meta cho từng feature"""
    feature_meta = []
    for mod in MODULE_DIR.iterdir():
        if mod.is_dir():
            meta_path = mod / "meta.json"
            if meta_path.exists():
                data = json.loads(meta_path.read_text())
                feature_meta.append(data)
            else:
                feature_meta.append({
                    "name": mod.name,
                    "title": mod.name,
                    "description": "Không có mô tả",
                    "tags": []
                })
    return feature_meta
```

---

## ✅ 3. Cập nhật `chat_interface.py` để dùng mô tả

```python
# ai_agent/chat_interface.py
import openai

openai.api_key = "sk-..."  # Hoặc dùng biến môi trường

def ask_ai_to_map_feature(user_input: str, feature_list: list[dict]) -> str:
    """Mapping câu lệnh người dùng sang tên feature từ danh sách meta"""
    feature_desc = "\n".join(
        f"- {f['name']}: {f['title']}\n  {f['description']}"
        for f in feature_list
    )

    prompt = f"""
Bạn là trợ lý hệ thống xử lý tự động. Đây là danh sách các chức năng hiện có:

{feature_desc}

Người dùng vừa nhập câu lệnh: "{user_input}"

Hãy chọn và trả về **tên tính năng phù hợp nhất** (chính xác theo tên `name` trong danh sách). 
Chỉ trả lại tên duy nhất, không cần giải thích.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content'].strip()
```

---

## ✅ 4. Cập nhật lệnh `chat-run` trong `main.py`

```python
from menu.enum import load_feature_meta
from ai_agent.chat_interface import ask_ai_to_map_feature

@app.command()
def chat_run():
    """Gợi ý và chạy tính năng phù hợp từ câu lệnh AI"""
    user_input = typer.prompt("💬 Nhập yêu cầu của bạn")

    feature_list = load_feature_meta()
    suggested_feature = ask_ai_to_map_feature(user_input, feature_list)

    typer.echo(f"🤖 Chat-AI đề xuất chạy chức năng: {suggested_feature}")
    confirm = typer.confirm("Bạn có muốn chạy không?", default=True)

    if confirm:
        run_feature(suggested_feature)
    else:
        typer.echo("❌ Đã huỷ chạy tính năng.")
```

---

## ✅ Cách sử dụng:

```bash
python main.py chat-run
```

> 💬 Nhập yêu cầu của bạn:
> tạo báo cáo thời gian xử lý ticket trong tháng 6

> 🤖 Chat-AI đề xuất chạy chức năng: `feature3_bao_cao`
> Bạn có muốn chạy không? `[Y/n]`: `Y`

---

## ⏭️ Gợi ý mở rộng tiếp theo (nếu bạn muốn):

* Thêm `meta.json` cho từng `projects/` để gợi ý đúng `project`
* Hiển thị danh sách chức năng gần đúng nếu AI mập mờ (dùng fuzzy matching)
* Hiển thị mô tả của feature được chọn trước khi chạy

Bạn muốn mình hỗ trợ tạo lệnh `init-feature` để sinh luôn cả `meta.json` không?
