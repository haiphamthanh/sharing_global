Để **đọc các thông số thiết kế từ Figma và chuyển thành JSON** thông qua **Figma REST API**, bạn chỉ cần bật **một số quyền truy cập tối thiểu cần thiết**. Dưới đây là gợi ý cụ thể cho phần **"Generate new token"** mà bạn đang thấy trong ảnh:

---

## ✅ Quyền cần bật (Access Scopes)

| Scope name               | Mô tả quyền                                       | Gợi ý chọn                                     |
| ------------------------ | ------------------------------------------------- | ---------------------------------------------- |
| ✅ `File content`         | Đọc nội dung và render hình ảnh từ file           | **Read access** ✅                              |
| ✅ `File metadata`        | Đọc metadata của file (tên, nodes, v.v.)          | **Read access** ✅                              |
| ✅ `Library assets`       | Đọc chi tiết về các components và styles          | **Read access** ✅ *(nếu dùng thư viện design)* |
| ⛔ `Dev resources`        | Đọc/ghi tài nguyên dev (ít dùng)                  | No access                                      |
| ⛔ `Comments`             | Đọc/ghi comment (không cần)                       | No access                                      |
| ⛔ `File versions`        | Lịch sử version (không cần để extract)            | No access                                      |
| ⛔ `Projects`             | Cấu trúc project (ít khi cần)                     | No access                                      |
| ⛔ `Team library content` | Chỉ cần nếu dùng thư viện chung                   | Có thể bật nếu dùng Team libraries             |
| ⛔ `Webhooks`             | Quản lý webhook (chỉ cần với automation nâng cao) | No access                                      |

---

## 🎯 Tối thiểu để hoạt động:

Bạn chỉ cần bật **3 scope** sau là đủ để dùng API như:

```http
GET https://api.figma.com/v1/files/<FILE_KEY>
```

| Scope            | Chọn:               |
| ---------------- | ------------------- |
| `File content`   | ✅ Read              |
| `File metadata`  | ✅ Read              |
| `Library assets` | ✅ Read *(tuỳ chọn)* |

---

## 💡 Gợi ý: Nếu bạn dùng team và muốn lấy cả các style từ team library:

* Bật thêm `Team library content` → ✅ Read

---

Sau khi chọn đúng scope, bạn bấm **Generate token**, Figma sẽ tạo 1 đoạn mã như sau:

```
figd_xxx_xxx_xxx
```

Bạn dùng mã này để gọi API từ code như sau:

```bash
curl -H "X-Figma-Token: figd_xxx_xxx_xxx" \
     "https://api.figma.com/v1/files/<FILE_KEY>"
```

---

Bạn muốn mình tạo luôn file Python/Python Notebook để test gọi API và extract thành JSON mẫu không?
