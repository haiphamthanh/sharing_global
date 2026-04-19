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
