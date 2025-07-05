Dưới đây là chức năng mới `init-feature` để giúp bạn **tạo nhanh một module chức năng mới**, gồm:

* Tạo thư mục `modules/<feature_name>/`
* Tạo file `config.json` với `project`, `preprocess_version`, `db_index` mặc định
* Tạo file `logic.py` với hàm `run(config)`

---

## ✅ Cập nhật `main.py` với lệnh `init-feature`

```python
# main.py
import typer
from pathlib import Path
import json

app = typer.Typer()

MODULE_DIR = Path("modules")
PROJECT_DIR = Path("projects")

@app.command()
def list_projects():
    projects = [p.name for p in PROJECT_DIR.iterdir() if p.is_dir()]
    for prj in projects:
        typer.echo(f"- {prj}")

@app.command()
def list_features():
    for mod in MODULE_DIR.iterdir():
        if mod.is_dir():
            typer.echo(f"- {mod.name}")

@app.command()
def run_feature(feature: str):
    mod_path = MODULE_DIR / feature
    config_path = mod_path / "config.json"
    if not config_path.exists():
        typer.echo(f"[❌] Không tìm thấy config cho {feature}")
        raise typer.Exit()

    config = json.loads(config_path.read_text())
    project = config["project"]
    db_index = config["db_index"]

    typer.echo(f"[🚀] Đang chạy {feature}")
    typer.echo(f"→ Dữ liệu từ project: {project}")
    typer.echo(f"→ Sử dụng index: {db_index}")

    try:
        logic_module = __import__(f"modules.{feature}.logic", fromlist=["run"])
        logic_module.run(config)
    except Exception as e:
        typer.echo(f"[❌] Lỗi khi chạy chức năng: {e}")
        raise typer.Exit()

@app.command()
def init_feature(
    feature_name: str = typer.Argument(..., help="Tên thư mục chức năng mới"),
    project: str = typer.Option(..., help="Tên project nguồn dữ liệu"),
    version: str = typer.Option("v1", help="Version pipeline xử lý"),
    db_index: str = typer.Option("process_v1.index", help="Tên file index tương ứng")
):
    """Khởi tạo một feature module mới"""
    mod_path = MODULE_DIR / feature_name
    if mod_path.exists():
        typer.echo(f"[⚠️] Module {feature_name} đã tồn tại.")
        raise typer.Exit()

    # Tạo thư mục
    mod_path.mkdir(parents=True)
    # Ghi file config.json
    config = {
        "project": project,
        "preprocess_version": version,
        "db_index": db_index
    }
    (mod_path / "config.json").write_text(json.dumps(config, indent=4))

    # Tạo logic.py mẫu
    logic_code = f'''def run(config):
    project = config["project"]
    index = config["db_index"]
    print(f"Đang xử lý với index {{index}} từ project {{project}}")
    # Thêm logic xử lý ở đây
'''
    (mod_path / "logic.py").write_text(logic_code)

    typer.echo(f"[✅] Đã tạo module mới: {feature_name} với config cho project {project}")
```

---

## ✅ Cách sử dụng:

```bash
python main.py init-feature feature3_bao_cao \
  --project finance_jira \
  --version v3 \
  --db-index process_v3.index
```

Output:

```
[✅] Đã tạo module mới: feature3_bao_cao với config cho project finance_jira
```

---

Bạn có muốn mình thêm cả lệnh `list-config` để hiển thị nội dung `config.json` của từng module không?
