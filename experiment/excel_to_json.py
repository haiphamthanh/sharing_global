import json
from openpyxl import load_workbook

wb = load_workbook("reconstructed.xlsx")
ws = wb.active

data = []
for i, row in enumerate(ws.iter_rows(values_only=False), start=1):
    row_data = []
    for cell in row:
        cell_info = {
            "text": cell.value,  # text hiển thị
            "link": cell.hyperlink.target if cell.hyperlink else None,
            "raw": repr(cell.value),  # hiện rõ \n nếu có
        }
        row_data.append(cell_info)
    data.append(row_data)

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
