Để tạo **Web Interface** tương tác với menu và chạy module, bạn có thể dùng **FastAPI** – framework hiện đại, nhẹ, hỗ trợ cả API lẫn giao diện bằng `Jinja2` hoặc `React`.

---

## ✅ Tổng quan luồng hệ thống Web:

1. Trang web hiển thị danh sách **feature (tên, mô tả, project liên quan)**
2. Người dùng chọn **1 tính năng và nhấn "Run"**
3. Backend gọi đúng `run_feature(<feature>)`
4. Kết quả được hiển thị ra màn hình hoặc log

---

## ✅ 1. Cài đặt FastAPI và uvicorn:

```bash
pip install fastapi uvicorn jinja2
```

---

## ✅ 2. Cấu trúc thư mục gợi ý:

```
auto_process_manager/
├── web/
│   ├── main_web.py           # Web entry
│   ├── templates/            # HTML template
│   │   └── index.html
│   └── static/               # (optional) CSS/JS
├── modules/
│   └── ...
├── menu/enum.py              # Đã có
└── ...
```

---

## ✅ 3. Giao diện web đơn giản (`templates/index.html`)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Automation Features</title>
</head>
<body>
    <h1>Danh sách chức năng tự động</h1>
    <form action="/run" method="post">
        <select name="feature">
            {% for f in features %}
                <option value="{{ f.name }}">{{ f.title }} ({{ f.name }})</option>
            {% endfor %}
        </select>
        <button type="submit">Chạy tính năng</button>
    </form>

    {% if result %}
    <h2>Kết quả</h2>
    <pre>{{ result }}</pre>
    {% endif %}
</body>
</html>
```

---

## ✅ 4. Web backend (`web/main_web.py`)

```python
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from menu.enum import load_feature_meta
from main import run_feature  # Hàm CLI đã có

import os
import sys
import io
from contextlib import redirect_stdout

app = FastAPI()
templates = Jinja2Templates(directory="web/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    features = load_feature_meta()
    return templates.TemplateResponse("index.html", {"request": request, "features": features})

@app.post("/run", response_class=HTMLResponse)
async def run_selected_feature(request: Request, feature: str = Form(...)):
    # Capture stdout để lấy kết quả in ra
    buf = io.StringIO()
    with redirect_stdout(buf):
        try:
            run_feature(feature)
        except Exception as e:
            print(f"[❌] Lỗi khi chạy: {e}")
    result = buf.getvalue()

    features = load_feature_meta()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "features": features,
        "result": result
    })
```

---

## ✅ 5. Chạy web server

```bash
uvicorn web.main_web:app --reload
```

Mở trình duyệt tại:
📍 [http://localhost:8000](http://localhost:8000)

---

## ✅ Bạn có thể mở rộng:

* Hiển thị chi tiết `project`, `preprocess_version`, `db_index` khi hover hoặc click
* Cho phép chọn `version`/`project` từ dropdown nếu muốn ghi đè config
* Thêm login nếu dùng nhiều user

---

Nếu bạn muốn mình gộp toàn bộ vào 1 template GitHub (CLI + Web + Chat-AI), mình có thể tạo giúp bạn bản starter project hoàn chỉnh. Bạn muốn không?
