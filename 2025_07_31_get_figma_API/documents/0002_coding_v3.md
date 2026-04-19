Để **lấy thông tin của một giao diện (ví dụ như một màn hình cụ thể hoặc component)** trong một file Figma, bạn sẽ cần gọi API `GET file` và **truy cập vào đúng node (frame/component)** trong cấu trúc cây (`document`).

---

## ✅ 1. Cấu trúc API: Get File Nodes

```http
GET https://api.figma.com/v1/files/{file_key}
```

### 🔑 Header:

```http
X-Figma-Token: YOUR_PERSONAL_ACCESS_TOKEN
```

---

## 📦 2. Ví dụ cụ thể bằng `curl`

```bash
curl -H "X-Figma-Token: figd_xxx_xxx" \
  https://api.figma.com/v1/files/dFgh3AbCDxYz
```

* `figd_xxx_xxx`: token bạn vừa tạo
* `dFgh3AbCDxYz`: là `file_key` (lấy từ URL Figma: `https://www.figma.com/file/dFgh3AbCDxYz/ProjectName`)

---

## 📁 3. Kết quả trả về là JSON, ví dụ:

```json
{
  "name": "My Design File",
  "document": {
    "id": "0:0",
    "name": "Document",
    "type": "DOCUMENT",
    "children": [
      {
        "id": "1:2",
        "name": "LoginScreen",
        "type": "FRAME",
        "children": [
          {
            "id": "2:10",
            "name": "Button",
            "type": "COMPONENT",
            "absoluteBoundingBox": {
              "x": 50,
              "y": 100,
              "width": 200,
              "height": 40
            },
            "fills": [
              {
                "type": "SOLID",
                "color": { "r": 0.2, "g": 0.6, "b": 1 }
              }
            ]
          }
        ]
      }
    ]
  }
}
```

Bạn có thể duyệt qua `document → children` để lấy thông tin cụ thể của:

* **Frames (screens)** như `"LoginScreen"`
* **Text**, **Components**, **Rectangles**, v.v.

---

## 🔍 4. Cách lấy *chính xác* 1 giao diện theo `node_id`

Nếu bạn biết node ID (ví dụ `"1:2"`), bạn có thể gọi API:

```http
GET https://api.figma.com/v1/files/{file_key}/nodes?ids={node_id}
```

### Ví dụ:

```bash
curl -H "X-Figma-Token: figd_xxx_xxx" \
  "https://api.figma.com/v1/files/dFgh3AbCDxYz/nodes?ids=1:2"
```

---

## 🧪 Gợi ý xử lý bằng Python

```python
import requests

headers = {
    "X-Figma-Token": "figd_xxx_xxx"
}

file_key = "dFgh3AbCDxYz"
node_id = "1:2"

url = f"https://api.figma.com/v1/files/{file_key}/nodes?ids={node_id}"
resp = requests.get(url, headers=headers)

print(resp.json())
```

---

## 📌 Mẹo: Làm sao biết node\_id?

Bạn có 2 cách:

1. Gọi API `GET /files/{file_key}` và duyệt JSON để tìm `name` và `id`
2. Dùng Figma DevTools plugin để xem trực tiếp ID của Frame/Component

---

Bạn muốn mình giúp bạn:

* Tạo đoạn script tự động trích xuất `"LoginScreen"` từ file cụ thể?
* Hay trích toàn bộ component để dùng làm reference cho so sánh với code?

Mình có thể code sẵn nếu bạn cần.
