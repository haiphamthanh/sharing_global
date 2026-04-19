Tuyệt vời! Dưới đây là lệnh mới `list-config` giúp bạn:

### ✅ Chức năng:

* Hiển thị nội dung `config.json` của một module bất kỳ
* Kiểm tra nhanh **module đang dùng project nào**, phiên bản xử lý nào, và file index nào

---

## 📌 Cập nhật `main.py` – thêm lệnh `list-config`

Thêm vào sau các lệnh khác:

```python
@app.command()
def list_config(feature: str):
    """Hiển thị nội dung config của một feature"""
    mod_path = MODULE_DIR / feature
    config_path = mod_path / "config.json"

    if not config_path.exists():
        typer.echo(f"[❌] Không tìm thấy config trong {feature}")
        raise typer.Exit()

    config = json.loads(config_path.read_text())
    typer.echo(f"📄 Cấu hình của {feature}:")
    for k, v in config.items():
        typer.echo(f"  {k}: {v}")
```

---

## ✅ Cách sử dụng CLI:

```bash
python main.py list-config feature1_chuc_nang_1
```

Kết quả mẫu:

```
📄 Cấu hình của feature1_chuc_nang_1:
  project: finance_jira
  preprocess_version: v2
  db_index: process_v2.index
```

---

Nếu bạn muốn, mình có thể tiếp tục mở rộng:

* Lệnh `update-config` để thay đổi giá trị nào đó trong `config.json`
* Hiển thị danh sách tất cả modules kèm project & index tương ứng (dạng bảng)

Bạn muốn thêm phần nào tiếp theo?
