Tuyệt vời! Để làm demo thử solution **đọc thông số Figma và chuẩn hoá thành JSON**, bạn cần tạo một **Figma Plugin hoặc Figma App**. Dưới đây là hướng dẫn từng bước để bạn tạo **Figma Plugin (tốt hơn cho mục đích này)** vì nó cho phép truy cập trực tiếp vào cây giao diện và export JSON tùy ý.

---

## ✅ Mục tiêu:

Tạo **Figma Plugin** để:

* Truy cập các node trong thiết kế (frame, text, button...)
* Lấy thông số như width, height, font, màu, padding...
* Chuẩn hoá và xuất ra JSON file

---

## ⚙️ Bước 1: Tạo plugin trên Figma

1. Mở [Figma](https://figma.com)
2. Chọn menu **Plugins → Development → New Plugin…**
3. Bấm **"Create your own plugin"**
4. Nhập tên: `Extract Design Tokens`
5. Chọn **"With UI & Browser APIs"** → bấm **Save**

Figma sẽ tạo cấu trúc cơ bản gồm:

```
manifest.json
code.ts
ui.html
```

---

## 🧠 Bước 2: Viết logic extract dữ liệu trong `code.ts`

Đây là nơi xử lý thông số từ canvas.

### ✅ Ví dụ `code.ts`:

```ts
// code.ts
figma.showUI(__html__, { width: 300, height: 200 })

figma.ui.onmessage = async (msg) => {
  if (msg.type === 'extract') {
    const nodes = figma.currentPage.selection

    const extracted = nodes.map(node => {
      if ('width' in node && 'height' in node) {
        return {
          name: node.name,
          type: node.type,
          width: node.width,
          height: node.height,
          fills: ('fills' in node && node.fills.length) ? node.fills[0] : null,
          fontSize: ('fontSize' in node) ? node.fontSize : null
        }
      }
      return null
    }).filter(Boolean)

    figma.ui.postMessage({ type: 'result', data: extracted })
  }
}
```

---

## 💻 Bước 3: Tạo UI đơn giản trong `ui.html`

```html
<!-- ui.html -->
<html>
  <body>
    <button id="extract">Extract</button>
    <pre id="output"></pre>

    <script>
      document.getElementById('extract').onclick = () => {
        parent.postMessage({ pluginMessage: { type: 'extract' } }, '*')
      }

      onmessage = (event) => {
        if (event.data.pluginMessage.type === 'result') {
          document.getElementById('output').textContent = 
            JSON.stringify(event.data.pluginMessage.data, null, 2)
        }
      }
    </script>
  </body>
</html>
```

---

## 📦 Bước 4: Chạy plugin demo

1. Quay lại Figma → mở thiết kế
2. Chọn một Frame hoặc Text → vào menu **Plugins → Development → "Extract Design Tokens"**
3. Nhấn **Extract**
4. Xem JSON kết quả ngay trên giao diện UI plugin

---

## 🧪 Kết quả mẫu:

```json
[
  {
    "name": "Primary Button",
    "type": "FRAME",
    "width": 120,
    "height": 44,
    "fills": {
      "type": "SOLID",
      "color": { "r": 0.2, "g": 0.6, "b": 1 }
    },
    "fontSize": null
  },
  {
    "name": "Label",
    "type": "TEXT",
    "width": 80,
    "height": 20,
    "fills": {
      "type": "SOLID",
      "color": { "r": 0, "g": 0, "b": 0 }
    },
    "fontSize": 14
  }
]
```

---

## 🎯 Gợi ý mở rộng

| Mục tiêu                       | Cách làm                                                     |
| ------------------------------ | ------------------------------------------------------------ |
| Xuất ra file JSON              | Dùng `figma.ui.postMessage` để gửi sang trình duyệt tải file |
| Hỗ trợ nhiều component         | Lọc theo tên / type / tag để group thông tin                 |
| Dùng được nhiều người          | Đăng plugin lên Community                                    |
| Chuyển sang format token chuẩn | Kết hợp `Style Dictionary` để chuẩn hóa output               |

---

## 📁 Nếu bạn cần project mẫu

Mình có thể tạo sẵn file ZIP với toàn bộ cấu trúc plugin và gửi bạn để import trực tiếp vào Figma.

---

Bạn có muốn mình:

* Tạo plugin đầy đủ, export JSON vào file?
* Mở rộng để so sánh luôn với thông số implement từ code?

Chỉ cần nói rõ mình sẽ giúp bạn triển khai luôn.
