Tuyệt vời! Ta sẽ mở rộng thêm phần fuzzy gợi ý để **hiển thị cả `title` và `description`** từ `meta.json` giúp người dùng **chọn chính xác** hơn.

---

## ✅ 1. Cập nhật lại `suggest_closest_feature` trong `menu/enum.py`

```python
from thefuzz import process

def suggest_closest_feature(feature_name: str, feature_meta: list[dict], limit: int = 3):
    """
    Gợi ý các feature gần giống với tên được AI trả về.
    Trả về danh sách dict gồm: name, score, title, description
    """
    feature_names = [f["name"] for f in feature_meta]
    matches = process.extract(feature_name, feature_names, limit=limit)

    suggestions = []
    for name, score in matches:
        match_meta = next((f for f in feature_meta if f["name"] == name), None)
        if match_meta:
            suggestions.append({
                "name": name,
                "score": score,
                "title": match_meta.get("title", name),
                "description": match_meta.get("description", "")
            })
    return suggestions
```

---

## ✅ 2. Cập nhật lệnh `chat-run` trong `main.py`

Thay đoạn cũ fuzzy như sau:

```python
    if suggested_feature not in all_feature_names:
        typer.echo(f"⚠️ Không tìm thấy tính năng '{suggested_feature}' trong danh sách.")
        from menu.enum import suggest_closest_feature
        suggestions = suggest_closest_feature(suggested_feature, feature_list)

        typer.echo("🧐 Có thể bạn muốn chọn:")
        for i, s in enumerate(suggestions, 1):
            typer.echo(f"{i}. {s['name']} ({s['score']}%)")
            typer.echo(f"   🏷️ {s['title']}")
            typer.echo(f"   📄 {s['description']}")
            typer.echo("")

        index = typer.prompt("👉 Nhập số tương ứng (hoặc bỏ qua)", default="0")
        if index.isdigit() and 1 <= int(index) <= len(suggestions):
            corrected_feature = suggestions[int(index)-1]["name"]
            typer.echo(f"✅ Đã chọn: {corrected_feature}")
            run_feature(corrected_feature)
        else:
            typer.echo("❌ Không chọn chức năng nào. Huỷ thao tác.")
        return
```

---

## ✅ Ví dụ kết quả:

```bash
python main.py chat-run
```

> 💬 Nhập yêu cầu của bạn:
> phân tích tốc độ xử lý task trong tháng

> ⚠️ Không tìm thấy tính năng `feature_task_speed`

> 🧐 Có thể bạn muốn chọn:

```
1. feature3_bao_cao (86%)
   🏷️ Tạo báo cáo từ dữ liệu Jira
   📄 Sinh báo cáo chi tiết hàng tháng từ dữ liệu Jira dự án Finance, phân tích theo tag, thời gian, và trạng thái ticket

2. feature1_thong_ke_jira (78%)
   🏷️ Thống kê Jira theo trạng thái
   📄 Tính toán tổng hợp số lượng ticket theo trạng thái và nhóm thời gian trong tháng

👉 Nhập số tương ứng: 1  
✅ Đã chọn: feature3_bao_cao
```

---

Bạn có muốn mình gộp toàn bộ các phần này thành một starter project template hoàn chỉnh không? Hoặc hỗ trợ deploy web API từ CLI này (sử dụng FastAPI)?
