Bạn bị lỗi "Tìm thấy 0 FRAME(s)" là do script `extract_frames.py` của bạn chỉ tìm các FRAME trực tiếp từ phần tử "document" cấp cao nhất. Tuy nhiên, trong file `figma_file.json` bạn cung cấp, tất cả các FRAME (như "Ecommerce") lại nằm trong một node con khác có ID là "1:5055" dưới khóa "nodes".

Để sửa lỗi này, bạn cần điều chỉnh hàm `main()` trong script `extract_frames.py` để duyệt qua tất cả các node trong khóa "nodes" của dữ liệu Figma, chứ không chỉ riêng phần "document" cấp cao nhất.

Dưới đây là phiên bản cập nhật của script `extract_frames.py` để xử lý cấu trúc file JSON của bạn:

```python
import json

def load_figma_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_frames(node, frames=None):
    if frames is None:
        frames = []

    # Kiểm tra nếu node hiện tại là một FRAME
    if node.get('type') == 'FRAME':
        frame_info = {
            'id': node.get('id'),
            'name': node.get('name'),
            'x': node.get('absoluteBoundingBox', {}).get('x'),
            'y': node.get('absoluteBoundingBox', {}).get('y'),
            'width': node.get('absoluteBoundingBox', {}).get('width'),
            'height': node.get('absoluteBoundingBox', {}).get('height'),
            'child_count': len(node.get('children', []))
        }
        frames.append(frame_info)

    # Đệ quy vào các node con nếu có
    if 'children' in node:
        for child in node['children']:
            find_frames(child, frames)
    
    return frames

def main():
    json_path = 'figma_file.json'  # 🔁 Đặt tên file JSON của bạn ở đây
    figma_data = load_figma_json(json_path)
    
    all_frames = []
    # Duyệt qua tất cả các node trong khóa "nodes" của dữ liệu Figma
    # Vì các FRAME có thể không chỉ nằm dưới "document" trực tiếp
    nodes_data = figma_data.get('nodes', {})
    for node_id, node_content in nodes_data.items():
        if 'document' in node_content:
            find_frames(node_content['document'], all_frames)
            
    print(f"✅ Tìm thấy {len(all_frames)} FRAME(s)\n")

    for frame in all_frames:
        print(f"🖼️ Frame: {frame['name']}")
        print(f"  ID: {frame['id']}")
        print(f"  Position: ({frame['x']}, {frame['y']})")
        print(f"  Size: {frame['width']} x {frame['height']}")
        print(f"  Children: {frame['child_count']}")
        print("-" * 40)

if __name__ == "__main__":
    main()
```

**Lý do thay đổi:**

  * File JSON bạn cung cấp có cấu trúc lồng nhau, với các FRAME thực tế nằm bên trong khóa `"nodes"` và mỗi ID node là một khóa khác, chứa một `"document"` (đại diện cho một page hoặc canvas trong Figma) mà bên trong nó mới chứa các FRAME.
  * Phiên bản trước của bạn chỉ gọi `find_frames` trên `figma_data.get('document', {})`, cái này trong trường hợp của bạn lại là một đối tượng rỗng hoặc không chứa các FRAME con trực tiếp.
  * Bằng cách lặp qua `figma_data.get('nodes', {})` và tìm `document` bên trong mỗi node, chúng ta có thể đảm bảo rằng tất cả các FRAME được khai thác, bất kể chúng được tổ chức như thế nào trong cấu trúc `nodes` của Figma.