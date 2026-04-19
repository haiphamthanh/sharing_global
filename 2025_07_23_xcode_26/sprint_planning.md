Dưới đây là kế hoạch chi tiết theo **chu kỳ 2 tuần (1 sprint)** để phát triển một AI Agent có khả năng **phát hiện và cập nhật tự động sự thay đổi của dự án liên quan đến Xcode 26**, hỗ trợ bạn chuẩn bị cho **Sprint Planning**.

---

## 🎯 **Mục tiêu chính**:

Tạo một AI Agent có thể:

* Phân tích sự thay đổi của Xcode 26 (Release Notes, Migration Guide…)
* So sánh với mã nguồn dự án hiện tại
* Gợi ý hoặc thực hiện cập nhật cần thiết (ví dụ: API deprecated, thay đổi Swift, config build)
* Gửi báo cáo định kỳ trước Sprint Planning

---

## 🗓️ Sprint 1 – **Thiết lập nền tảng (2 tuần)**

### 🔹 Tuần 1 – **Crawler & Phân tích sự thay đổi Xcode**

1. [ ] **Nghiên cứu Xcode 26**

   * Thu thập Release Notes, Migration Guide chính thức từ Apple
   * Tổng hợp dạng JSON: `{ version, change_type, component, description }`

2. [ ] **Xây dựng Xcode Update Crawler**

   * Crawl và parse dữ liệu từ:

     * [https://developer.apple.com/documentation/xcode-release-notes](https://developer.apple.com/documentation/xcode-release-notes)
     * [https://developer.apple.com/xcode/resources/](https://developer.apple.com/xcode/resources/)

3. [ ] **Chuẩn hóa dữ liệu cập nhật (Change Database)**

   * Lưu dưới dạng cấu trúc dễ truy vấn
   * Tạo từ khóa để phân loại: `SwiftSyntax`, `BuildSettings`, `DeprecatedAPI`, `NewFeatures`, v.v.

---

### 🔹 Tuần 2 – **Scan dự án và phân tích tương quan**

4. [ ] **Scan mã nguồn dự án hiện tại**

   * Tạo script (Python hoặc SwiftSyntax) để duyệt các file `.swift`, `pbxproj`, `plist`,…
   * Trích xuất:

     * Danh sách API đang sử dụng
     * Build setting, Swift version, cấu hình…

5. [ ] **So sánh với thay đổi của Xcode**

   * Mapping các thay đổi từ database vào dự án
   * Đánh dấu: `cảnh báo`, `cần sửa`, `bị deprecated`, `không ảnh hưởng`

6. [ ] **Sinh báo cáo Sprint Planning**

   * Gợi ý thay đổi theo định dạng markdown/PDF
   * Ví dụ:

     ```markdown
     ### 🛠 Deprecated APIs
     - [ ] `NSURLConnection` bị loại bỏ – thay thế bằng `URLSession`

     ### ⚙️ Build Settings
     - [ ] `ENABLE_BITCODE` không còn hỗ trợ – cần xoá trong `project.pbxproj`

     ### ✅ Không ảnh hưởng
     - [x] Swift Concurrency cải tiến – không cần thay đổi
     ```

---