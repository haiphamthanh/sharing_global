Rất hay! Dưới đây là cách bạn có thể tích hợp **chat-AI** (sử dụng OpenAI hoặc Gemini hoặc bất kỳ LLM nào) để **mapping câu lệnh tự nhiên → enum chức năng**, rồi **tự động gọi `run-feature`**.

---

## 🧠 Ý tưởng tổng thể:

1. **User nhập câu lệnh tự nhiên**, ví dụ:

   > “Tạo báo cáo chi tiết từ dữ liệu jira tháng 6”
2. Gửi vào LLM (OpenAI/Gemini) cùng danh sách enum feature
3. LLM trả về tên feature phù hợp nhất, ví dụ:

   > `feature3_bao_cao`
4. Gọi luôn `run_feature(feature_name)`

---

## ✅ Cài đặt OpenAI API (hoặc có thể tùy chọn Gemini)

```bash
pip install openai
```

---

## 📁 Tạo file `ai_agent/chat_interface.py`

```python
# ai_agent/chat_interface.py
import openai

openai.api_key = "sk-..."  # hoặc đặt biến môi trường OPENAI_API_KEY

def ask_ai_to_map_feature(user_input: str, feature_enum: list[str]) -> str:
    """Gửi câu lệnh người dùng + danh sách feature cho AI mapping"""
    prompt = f"""
Bạn là trợ lý hệ thống xử lý tự động. Dưới đây là danh sách các chức năng có sẵn:

{chr(10).join(f"- {f}" for f in feature_enum)}

Người dùng nhập câu lệnh: "{user_input}"

Hãy trả về tên duy nhất của một chức năng phù hợp nhất (chính xác theo tên trong danh sách). Chỉ trả lại tên, không kèm giải thích.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response['choices'][0]['message']['content'].strip()
    return answer
```

---

## 🧩 Thêm vào `main.py` lệnh `chat-run`

```python
from ai_agent.chat_interface import ask_ai_to_map_feature

@app.command()
def chat_run():
    """Chạy tính năng thông qua Chat AI"""
    user_input = typer.prompt("💬 Nhập yêu cầu của bạn")

    # Liệt kê tất cả enum hiện có
    feature_enum = [mod.name for mod in MODULE_DIR.iterdir() if mod.is_dir()]
    feature = ask_ai_to_map_feature(user_input, feature_enum)

    typer.echo(f"🤖 Chat-AI gợi ý dùng chức năng: {feature}")
    confirm = typer.confirm("Bạn có muốn chạy không?", default=True)

    if confirm:
        run_feature(feature)
    else:
        typer.echo("❌ Đã huỷ chạy tính năng.")
```

---

## ✅ Ví dụ sử dụng:

```bash
python main.py chat-run
```

> 💬 Nhập yêu cầu của bạn:
> tạo báo cáo chi tiết từ dữ liệu jira tháng 6

> 🤖 Chat-AI gợi ý dùng chức năng: `feature3_bao_cao`

> Bạn có muốn chạy không? `[Y/n]`: `Y`

→ Gọi `run_feature("feature3_bao_cao")`

---

## ⏭️ Gợi ý mở rộng:

* Hiển thị kèm mô tả ngắn của từng feature để AI mapping tốt hơn
* Thêm file `meta.json` trong mỗi `modules/featureX/` để mô tả ngắn chức năng

Bạn có muốn mình giúp bạn tạo format cho `meta.json` và cải thiện prompt AI không?
