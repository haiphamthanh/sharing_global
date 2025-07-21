import json
from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter

with open("output_structured.json", "r", encoding="utf-8") as f:
    structured_data = json.load(f)

wb = Workbook()
ws = wb.active

for row_obj in structured_data:
    row_idx = row_obj["row"]
    for col_idx, cell in enumerate(row_obj["data"], start=1):
        col_letter = get_column_letter(col_idx)
        excel_cell = ws[f"{col_letter}{row_idx}"]

        text = cell.get("text", "")
        link = cell.get("link", None)

        excel_cell.value = text
        excel_cell.alignment = Alignment(wrap_text=True)

        if link:
            excel_cell.hyperlink = link
            excel_cell.style = "Hyperlink"

wb.save("reconstructed_from_structured.json.xlsx")
