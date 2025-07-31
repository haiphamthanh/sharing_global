import json


def load_figma_json(path):
    """Loads a JSON file from the given path."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_nodes_with_bounds(node, nodes_with_bounds=None):
    """Recursively finds all nodes with 'absoluteBoundingBox'."""
    if nodes_with_bounds is None:
        nodes_with_bounds = []

    if 'absoluteBoundingBox' in node:
        nodes_with_bounds.append(node)

    if 'children' in node:
        for child in node['children']:
            get_nodes_with_bounds(child, nodes_with_bounds)
    return nodes_with_bounds


def calculate_distance(node1, node2):
    """Calculates horizontal and vertical distances between two nodes."""
    bounds1 = node1.get('absoluteBoundingBox')
    bounds2 = node2.get('absoluteBoundingBox')

    if not bounds1 or not bounds2:
        return None, None

    x1, y1 = bounds1['x'], bounds1['y']
    w1, h1 = bounds1['width'], bounds1['height']
    x2, y2 = bounds2['x'], bounds2['y']
    w2, h2 = bounds2['width'], bounds2['height']

    # Calculate horizontal distance
    # The minimum distance between two rectangles. If they overlap, distance is negative.
    horz_dist = 0
    if x1 + w1 < x2:  # node1 is to the left of node2
        horz_dist = x2 - (x1 + w1)
    elif x2 + w2 < x1:  # node2 is to the left of node1
        horz_dist = x1 - (x2 + w2)
    else:  # They overlap horizontally
        horz_dist = max(x1, x2) - min(x1 + w1, x2 + w2)
        if horz_dist < 0:
            horz_dist = 0  # Consider overlap as 0 distance if asking for positive distance, or leave as negative for overlap

    # Calculate vertical distance
    vert_dist = 0
    if y1 + h1 < y2:  # node1 is above node2
        vert_dist = y2 - (y1 + h1)
    elif y2 + h2 < y1:  # node2 is above node1
        vert_dist = y1 - (y2 + h2)
    else:  # They overlap vertically
        vert_dist = max(y1, y2) - min(y1 + h1, y2 + h2)
        if vert_dist < 0:
            vert_dist = 0  # Consider overlap as 0 distance if asking for positive distance, or leave as negative for overlap

    return horz_dist, vert_dist


def main():
    json_path = 'figma_file.json'
    figma_data = load_figma_json(json_path)

    # Collect all parent nodes that have children (e.g., FRAME, GROUP)
    parent_nodes = []

    # Start recursion from the document node within 'nodes'
    if 'nodes' in figma_data and '1:5055' in figma_data['nodes']:
        document_node = figma_data['nodes']['1:5055']['document']
        all_nodes_in_document = get_nodes_with_bounds(document_node)

        # Filter for nodes that are parents (have children)
        for node in all_nodes_in_document:
            if 'children' in node and node['children']:
                parent_nodes.append(node)

    if not parent_nodes:
        print("Không tìm thấy các node có chứa children để tính khoảng cách.")
        return

    print("✅ Tính toán khoảng cách giữa các đối tượng anh em ruột (siblings):\n")

    for parent in parent_nodes:
        if not parent.get('children'):
            continue

        print(f"Parent Node: {parent['name']} (ID: {parent['id']})")
        children = parent['children']

        # We only calculate distances between objects within the same parent
        for i in range(len(children)):
            for j in range(i + 1, len(children)):
                node1 = children[i]
                node2 = children[j]

                # Ensure both nodes have absoluteBoundingBox
                if 'absoluteBoundingBox' not in node1 or 'absoluteBoundingBox' not in node2:
                    continue

                h_dist, v_dist = calculate_distance(node1, node2)
                if h_dist is not None and v_dist is not None:
                    print(
                        f"  Khoảng cách giữa '{node1.get('name', 'Unknown')}' (ID: {node1['id']}) và '{node2.get('name', 'Unknown')}' (ID: {node2['id']}):")
                    print(f"    Ngang: {h_dist:.2f}")
                    print(f"    Dọc: {v_dist:.2f}")
        print("-" * 60)


if __name__ == "__main__":
    main()
