Rất hay! Dưới đây là cách tích hợp thêm tính năng **gợi ý danh sách chức năng gần đúng (fuzzy matching)** khi:

* Chat-AI trả về tên không khớp 100% với tên trong enum
* Hoặc người dùng gõ nhầm/tên sai

---

## ✅ 1. Cài đặt thư viện fuzzy

```bash
pip install thefuzz[speedup]
```

---

## ✅ 2. Thêm hàm gợi ý gần đúng vào `menu/enum.py`

```python
# menu/enum.py
from thefuzz import process

def suggest_closest_feature(feature_name: str, feature_list: list[str], limit: int = 3):
    """Gợi ý các tên feature gần giống với tên nhập vào"""
    return process.extract(feature_name, feature_list, limit=limit)
```

---

## ✅ 3. Cập nhật `chat-run` trong `main.py`

Thay thế đoạn này:

```python
    typer.echo(f"🤖 Chat-AI đề xuất chạy chức năng: {suggested_feature}")
    confirm = typer.confirm("Bạn có muốn chạy không?", default=True)

    if confirm:
        run_feature(suggested_feature)
```

Bằng đoạn **kiểm tra và fuzzy fallback**:

```python
    all_feature_names = [f["name"] for f in feature_list]

    if suggested_feature not in all_feature_names:
        typer.echo(f"⚠️ Không tìm thấy tính năng '{suggested_feature}' trong danh sách.")
        from menu.enum import suggest_closest_feature
        suggestions = suggest_closest_feature(suggested_feature, all_feature_names)

        typer.echo("🧐 Có thể bạn muốn chọn:")
        for i, (name, score) in enumerate(suggestions, 1):
            typer.echo(f"{i}. {name}  (độ khớp: {score}%)")

        index = typer.prompt("👉 Nhập số tương ứng (hoặc bỏ qua)", default="0")
        if index.isdigit() and 1 <= int(index) <= len(suggestions):
            corrected_feature = suggestions[int(index)-1][0]
            typer.echo(f"✅ Đã chọn: {corrected_feature}")
            run_feature(corrected_feature)
        else:
            typer.echo("❌ Không chọn chức năng nào. Huỷ thao tác.")
        return
    else:
        typer.echo(f"🤖 Chat-AI đề xuất chạy chức năng: {suggested_feature}")
        confirm = typer.confirm("Bạn có muốn chạy không?", default=True)
        if confirm:
            run_feature(suggested_feature)
```

---

## ✅ Ví dụ hoạt động:

```bash
python main.py chat-run
```

> 💬 Nhập yêu cầu của bạn:
> thống kê thời gian xử lý phiếu Jira

> ⚠️ Không tìm thấy tính năng `feature3_thong_ke`

> 🧐 Có thể bạn muốn chọn:
>
> 1. feature3\_bao\_cao (độ khớp: 86%)
> 2. feature1\_thong\_ke\_jira (độ khớp: 78%)

> 👉 Nhập số tương ứng: `1`
> ✅ Đã chọn: `feature3_bao_cao`
> → chạy `run_feature(...)`

---

Bạn có muốn bổ sung thêm `title`/`description` khi hiển thị gợi ý không? (cho dễ hiểu người dùng chọn đúng). Nếu có mình sẽ cập nhật tiếp phần này!
