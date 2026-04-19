```python?code_reference&code_event_index=2
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
            horz_dist = 0 # Consider overlap as 0 distance if asking for positive distance, or leave as negative for overlap

    # Calculate vertical distance
    vert_dist = 0
    if y1 + h1 < y2:  # node1 is above node2
        vert_dist = y2 - (y1 + h1)
    elif y2 + h2 < y1:  # node2 is above node1
        vert_dist = y1 - (y2 + h2)
    else:  # They overlap vertically
        vert_dist = max(y1, y2) - min(y1 + h1, y2 + h2)
        if vert_dist < 0:
            vert_dist = 0 # Consider overlap as 0 distance if asking for positive distance, or leave as negative for overlap

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
                    print(f"  Khoảng cách giữa '{node1.get('name', 'Unknown')}' (ID: {node1['id']}) và '{node2.get('name', 'Unknown')}' (ID: {node2['id']}):")
                    print(f"    Ngang: {h_dist:.2f}")
                    print(f"    Dọc: {v_dist:.2f}")
        print("-" * 60)

if __name__ == "__main__":
    main()
```

```text?code_stdout&code_event_index=2
✅ Tính toán khoảng cách giữa các đối tượng anh em ruột (siblings):

Parent Node: Ecommerce (ID: 1:5055)
  Khoảng cách giữa 'Row' (ID: 1:5056) và 'Row' (ID: 1:5075):
    Ngang: 0.00
    Dọc: 16.00
  Khoảng cách giữa 'Row' (ID: 1:5056) và 'Row' (ID: 1:5100):
    Ngang: 0.00
    Dọc: 309.00
  Khoảng cách giữa 'Row' (ID: 1:5056) và 'Banner' (ID: 1:5111):
    Ngang: 0.00
    Dọc: 16.00
  Khoảng cách giữa 'Row' (ID: 1:5056) và 'Pills' (ID: 1:5119):
    Ngang: 0.00
    Dọc: 168.00
  Khoảng cách giữa 'Row' (ID: 1:5056) và 'Search' (ID: 1:5136):
    Ngang: 0.00
    Dọc: 208.00
  Khoảng cách giữa 'Row' (ID: 1:5056) và 'Tab Bar' (ID: 1:5141):
    Ngang: 0.00
    Dọc: 276.00
  Khoảng cách giữa 'Row' (ID: 1:5056) và 'Status Bar' (ID: 1:5157):
    Ngang: 0.00
    Dọc: 256.00
  Khoảng cách giữa 'Row' (ID: 1:5075) và 'Row' (ID: 1:5100):
    Ngang: 0.00
    Dọc: 16.00
  Khoảng cách giữa 'Row' (ID: 1:5075) và 'Banner' (ID: 1:5111):
    Ngang: 0.00
    Dọc: 190.00
  Khoảng cách giữa 'Row' (ID: 1:5075) và 'Pills' (ID: 1:5119):
    Ngang: 0.00
    Dọc: 342.00
  Khoảng cách giữa 'Row' (ID: 1:5075) và 'Search' (ID: 1:5136):
    Ngang: 0.00
    Dọc: 382.00
  Khoảng cách giữa 'Row' (ID: 1:5075) và 'Tab Bar' (ID: 1:5141):
    Ngang: 0.00
    Dọc: 0.00
  Khoảng cách giữa 'Row' (ID: 1:5075) và 'Status Bar' (ID: 1:5157):
    Ngang: 0.00
    Dọc: 430.00
  Khoảng cách giữa 'Row' (ID: 1:5100) và 'Banner' (ID: 1:5111):
    Ngang: 0.00
    Dọc: 483.00
  Khoảng cách giữa 'Row' (ID: 1:5100) và 'Pills' (ID: 1:5119):
    Ngang: 0.00
    Dọc: 635.00
  Khoảng cách giữa 'Row' (ID: 1:5100) và 'Search' (ID: 1:5136):
    Ngang: 0.00
    Dọc: 675.00
  Khoảng cách giữa 'Row' (ID: 1:5100) và 'Tab Bar' (ID: 1:5141):
    Ngang: 0.00
    Dọc: 0.00
  Khoảng cách giữa 'Row' (ID: 1:5100) và 'Status Bar' (ID: 1:5157):
    Ngang: 0.00
    Dọc: 723.00
  Khoảng cách giữa 'Banner' (ID: 1:5111) và 'Pills' (ID: 1:5119):
    Ngang: 0.00
    Dọc: 16.00
  Khoảng cách giữa 'Banner' (ID: 1:5111) và 'Search' (ID: 1:5136):
    Ngang: 0.00
    Dọc: 56.00
  Khoảng cách giữa 'Banner' (ID: 1:5111) và 'Tab Bar' (ID: 1:5141):
    Ngang: 0.00
    Dọc: 450.00
  Khoảng cách giữa 'Banner' (ID: 1:5111) và 'Status Bar' (ID: 1:5157):
    Ngang: 0.00
    Dọc: 104.00
  Khoảng cách giữa 'Pills' (ID: 1:5119) và 'Search' (ID: 1:5136):
    Ngang: 0.00
    Dọc: 8.00
  Khoảng cách giữa 'Pills' (ID: 1:5119) và 'Tab Bar' (ID: 1:5141):
    Ngang: 0.00
    Dọc: 602.00
  Khoảng cách giữa 'Pills' (ID: 1:5119) và 'Status Bar' (ID: 1:5157):
    Ngang: 0.00
    Dọc: 56.00
  Khoảng cách giữa 'Search' (ID: 1:5136) và 'Tab Bar' (ID: 1:5141):
    Ngang: 0.00
    Dọc: 642.00
  Khoảng cách giữa 'Search' (ID: 1:5136) và 'Status Bar' (ID: 1:5157):
    Ngang: 0.00
    Dọc: 8.00
  Khoảng cách giữa 'Tab Bar' (ID: 1:5141) và 'Status Bar' (ID: 1:5157):
    Ngang: 0.00
    Dọc: 690.00
------------------------------------------------------------
Parent Node: Row (ID: 1:5056)
  Khoảng cách giữa 'Title' (ID: 1:5057) và 'Carousel' (ID: 1:5062):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Title (ID: 1:5057)
  Khoảng cách giữa 'Title' (ID: 1:5058) và 'Chevron' (ID: 1:5059):
    Ngang: 10.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Chevron (ID: 1:5059)
  Khoảng cách giữa 'Container' (ID: 1:5060) và 'Icon/Chevron' (ID: 1:5061):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Icon/Chevron (ID: 1:5061)
  Khoảng cách giữa 'chevron_right_slim' (ID: I1:5061;106:519) và 'chevron_right_slim' (ID: I1:5061;106:520):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Carousel (ID: 1:5062)
  Khoảng cách giữa 'Item' (ID: 1:5063) và 'Item' (ID: 1:5066):
    Ngang: 24.00
    Dọc: 0.00
  Khoảng cách giữa 'Item' (ID: 1:5063) và 'Item' (ID: 1:5069):
    Ngang: 124.00
    Dọc: 0.00
  Khoảng cách giữa 'Item' (ID: 1:5063) và 'Item' (ID: 1:5072):
    Ngang: 224.00
    Dọc: 0.00
  Khoảng cách giữa 'Item' (ID: 1:5066) và 'Item' (ID: 1:5069):
    Ngang: 24.00
    Dọc: 0.00
  Khoảng cách giữa 'Item' (ID: 1:5066) và 'Item' (ID: 1:5072):
    Ngang: 124.00
    Dọc: 0.00
  Khoảng cách giữa 'Item' (ID: 1:5069) và 'Item' (ID: 1:5072):
    Ngang: 24.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Item (ID: 1:5063)
  Khoảng cách giữa 'Image' (ID: 1:5064) và 'Title' (ID: 1:5065):
    Ngang: 0.00
    Dọc: 8.00
------------------------------------------------------------
Parent Node: Item (ID: 1:5066)
  Khoảng cách giữa 'Image' (ID: 1:5067) và 'Title' (ID: 1:5068):
    Ngang: 0.00
    Dọc: 8.00
------------------------------------------------------------
Parent Node: Item (ID: 1:5069)
  Khoảng cách giữa 'Image' (ID: 1:5070) và 'Title' (ID: 1:5071):
    Ngang: 0.00
    Dọc: 8.00
------------------------------------------------------------
Parent Node: Item (ID: 1:5072)
  Khoảng cách giữa 'Image' (ID: 1:5073) và 'Title' (ID: 1:5074):
    Ngang: 0.00
    Dọc: 8.00
------------------------------------------------------------
Parent Node: Row (ID: 1:5075)
  Khoảng cách giữa 'Header' (ID: 1:5076) và 'Carousel' (ID: 1:5081):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Header (ID: 1:5076)
  Khoảng cách giữa 'Title' (ID: 1:5077) và 'Group 123201' (ID: 1:5078):
    Ngang: 10.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Group 123201 (ID: 1:5078)
  Khoảng cách giữa 'Ellipse 160' (ID: 1:5079) và 'Icon/Chevron_Right_Slim_LTR' (ID: 1:5080):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Icon/Chevron_Right_Slim_LTR (ID: 1:5080)
  Khoảng cách giữa 'chevron_right_slim' (ID: I1:5080;106:519) và 'chevron_right_slim' (ID: I1:5080;106:520):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Carousel (ID: 1:5081)
  Khoảng cách giữa 'Card' (ID: 1:5082) và 'Card' (ID: 1:5088):
    Ngang: 12.00
    Dọc: 0.00
  Khoảng cách giữa 'Card' (ID: 1:5082) và 'Card' (ID: 1:5094):
    Ngang: 172.00
    Dọc: 0.00
  Khoảng cách giữa 'Card' (ID: 1:5088) và 'Card' (ID: 1:5094):
    Ngang: 12.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Card (ID: 1:5082)
  Khoảng cách giữa 'Image' (ID: 1:5083) và 'Info' (ID: 1:5084):
    Ngang: 0.00
    Dọc: 12.00
------------------------------------------------------------
Parent Node: Info (ID: 1:5084)
  Khoảng cách giữa 'Brand' (ID: 1:5085) và 'Product name' (ID: 1:5086):
    Ngang: 0.00
    Dọc: 2.00
  Khoảng cách giữa 'Brand' (ID: 1:5085) và '$10.99' (ID: 1:5087):
    Ngang: 0.00
    Dọc: 24.00
  Khoảng cách giữa 'Product name' (ID: 1:5086) và '$10.99' (ID: 1:5087):
    Ngang: 0.00
    Dọc: 2.00
------------------------------------------------------------
Parent Node: Card (ID: 1:5088)
  Khoảng cách giữa 'Image' (ID: 1:5089) và 'Info' (ID: 1:5090):
    Ngang: 0.00
    Dọc: 12.00
------------------------------------------------------------
Parent Node: Info (ID: 1:5090)
  Khoảng cách giữa 'Brand' (ID: 1:5091) và 'Product name' (ID: 1:5092):
    Ngang: 0.00
    Dọc: 2.00
  Khoảng cách giữa 'Brand' (ID: 1:5091) và '$10.99' (ID: 1:5093):
    Ngang: 0.00
    Dọc: 24.00
  Khoảng cách giữa 'Product name' (ID: 1:5092) và '$10.99' (ID: 1:5093):
    Ngang: 0.00
    Dọc: 2.00
------------------------------------------------------------
Parent Node: Card (ID: 1:5094)
  Khoảng cách giữa 'Image' (ID: 1:5095) và 'Info' (ID: 1:5096):
    Ngang: 0.00
    Dọc: 12.00
------------------------------------------------------------
Parent Node: Info (ID: 1:5096)
  Khoảng cách giữa 'Brand' (ID: 1:5097) và 'Product name' (ID: 1:5098):
    Ngang: 0.00
    Dọc: 2.00
  Khoảng cách giữa 'Brand' (ID: 1:5097) và '$10.99' (ID: 1:5099):
    Ngang: 0.00
    Dọc: 24.00
  Khoảng cách giữa 'Product name' (ID: 1:5098) và '$10.99' (ID: 1:5099):
    Ngang: 0.00
    Dọc: 2.00
------------------------------------------------------------
Parent Node: Row (ID: 1:5100)
  Khoảng cách giữa 'Title' (ID: 1:5101) và 'Carousel' (ID: 1:5106):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Title (ID: 1:5101)
  Khoảng cách giữa 'Title' (ID: 1:5102) và 'Chevron' (ID: 1:5103):
    Ngang: 10.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Chevron (ID: 1:5103)
  Khoảng cách giữa 'BG' (ID: 1:5104) và 'Icon/Chevron' (ID: 1:5105):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Icon/Chevron (ID: 1:5105)
  Khoảng cách giữa 'chevron_right_slim' (ID: I1:5105;106:519) và 'chevron_right_slim' (ID: I1:5105;106:520):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Carousel (ID: 1:5106)
  Khoảng cách giữa 'Image' (ID: 1:5107) và 'Image' (ID: 1:5108):
    Ngang: 12.00
    Dọc: 0.00
  Khoảng cách giữa 'Image' (ID: 1:5107) và 'Image' (ID: 1:5109):
    Ngang: 120.00
    Dọc: 0.00
  Khoảng cách giữa 'Image' (ID: 1:5107) và 'Image' (ID: 1:5110):
    Ngang: 228.00
    Dọc: 0.00
  Khoảng cách giữa 'Image' (ID: 1:5108) và 'Image' (ID: 1:5109):
    Ngang: 12.00
    Dọc: 0.00
  Khoảng cách giữa 'Image' (ID: 1:5108) và 'Image' (ID: 1:5110):
    Ngang: 120.00
    Dọc: 0.00
  Khoảng cách giữa 'Image' (ID: 1:5109) và 'Image' (ID: 1:5110):
    Ngang: 12.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Banner (ID: 1:5111)
  Khoảng cách giữa 'Banner title' (ID: 1:5112) và 'Pagination' (ID: 1:5113):
    Ngang: 0.00
    Dọc: 41.00
------------------------------------------------------------
Parent Node: Pagination (ID: 1:5113)
  Khoảng cách giữa 'Selected' (ID: 1:5114) và 'Default' (ID: 1:5115):
    Ngang: 5.00
    Dọc: 0.00
  Khoảng cách giữa 'Selected' (ID: 1:5114) và 'Default' (ID: 1:5116):
    Ngang: 15.00
    Dọc: 0.00
  Khoảng cách giữa 'Selected' (ID: 1:5114) và 'Default' (ID: 1:5117):
    Ngang: 25.00
    Dọc: 0.00
  Khoảng cách giữa 'Selected' (ID: 1:5114) và 'Default' (ID: 1:5118):
    Ngang: 35.00
    Dọc: 0.00
  Khoảng cách giữa 'Default' (ID: 1:5115) và 'Default' (ID: 1:5116):
    Ngang: 5.00
    Dọc: 0.00
  Khoảng cách giữa 'Default' (ID: 1:5115) và 'Default' (ID: 1:5117):
    Ngang: 15.00
    Dọc: 0.00
  Khoảng cách giữa 'Default' (ID: 1:5115) và 'Default' (ID: 1:5118):
    Ngang: 25.00
    Dọc: 0.00
  Khoảng cách giữa 'Default' (ID: 1:5116) và 'Default' (ID: 1:5117):
    Ngang: 5.00
    Dọc: 0.00
  Khoảng cách giữa 'Default' (ID: 1:5116) và 'Default' (ID: 1:5118):
    Ngang: 15.00
    Dọc: 0.00
  Khoảng cách giữa 'Default' (ID: 1:5117) và 'Default' (ID: 1:5118):
    Ngang: 5.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Pills (ID: 1:5119)
  Khoảng cách giữa 'Pill' (ID: 1:5120) và 'Pill' (ID: 1:5124):
    Ngang: 8.00
    Dọc: 0.00
  Khoảng cách giữa 'Pill' (ID: 1:5120) và 'Pill' (ID: 1:5128):
    Ngang: 107.00
    Dọc: 0.00
  Khoảng cách giữa 'Pill' (ID: 1:5120) và 'Pill' (ID: 1:5132):
    Ngang: 221.00
    Dọc: 0.00
  Khoảng cách giữa 'Pill' (ID: 1:5124) và 'Pill' (ID: 1:5128):
    Ngang: 8.00
    Dọc: 0.00
  Khoảng cách giữa 'Pill' (ID: 1:5124) và 'Pill' (ID: 1:5132):
    Ngang: 122.00
    Dọc: 0.00
  Khoảng cách giữa 'Pill' (ID: 1:5128) và 'Pill' (ID: 1:5132):
    Ngang: 8.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Pill (ID: 1:5120)
------------------------------------------------------------
Parent Node: Icon + Label (ID: 1:5121)
  Khoảng cách giữa 'Icon/Favorite' (ID: 1:5122) và 'Label' (ID: 1:5123):
    Ngang: 4.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Icon/Favorite (ID: 1:5122)
------------------------------------------------------------
Parent Node: Pill (ID: 1:5124)
------------------------------------------------------------
Parent Node: Icon + Label (ID: 1:5125)
  Khoảng cách giữa 'Icon/History' (ID: 1:5126) và 'Label' (ID: 1:5127):
    Ngang: 4.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Icon/History (ID: 1:5126)
  Khoảng cách giữa '_source' (ID: I1:5126;106:476) và 'watch_history' (ID: I1:5126;106:481):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: _source (ID: I1:5126;106:476)
------------------------------------------------------------
Parent Node: Union (ID: I1:5126;106:477)
  Khoảng cách giữa 'Ellipse 131' (ID: I1:5126;106:478) và 'Polygon 2' (ID: I1:5126;106:479):
    Ngang: 0.00
    Dọc: 0.00
  Khoảng cách giữa 'Ellipse 131' (ID: I1:5126;106:478) và 'Polygon 3' (ID: I1:5126;106:480):
    Ngang: 0.00
    Dọc: 0.00
  Khoảng cách giữa 'Polygon 2' (ID: I1:5126;106:479) và 'Polygon 3' (ID: I1:5126;106:480):
    Ngang: 1.13
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Pill (ID: 1:5128)
------------------------------------------------------------
Parent Node: Icon + Label (ID: 1:5129)
  Khoảng cách giữa 'Icon/Following' (ID: 1:5130) và 'Label' (ID: 1:5131):
    Ngang: 4.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Icon/Following (ID: 1:5130)
  Khoảng cách giữa '_source' (ID: I1:5130;106:512) và 'person_tick' (ID: I1:5130;106:513):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Pill (ID: 1:5132)
------------------------------------------------------------
Parent Node: Icon + Label (ID: 1:5133)
  Khoảng cách giữa 'Icon/Order' (ID: 1:5134) và 'Label' (ID: 1:5135):
    Ngang: 4.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Icon/Order (ID: 1:5134)
------------------------------------------------------------
Parent Node: Search (ID: 1:5136)
  Khoảng cách giữa 'search' (ID: 1:5137) và 'Label' (ID: 1:5140):
    Ngang: 12.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: search (ID: 1:5137)
  Khoảng cách giữa 'Vector' (ID: 1:5138) và 'Vector' (ID: 1:5139):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Tab Bar (ID: 1:5141)
  Khoảng cách giữa 'Tabs' (ID: 1:5142) và 'Home Indicator' (ID: 1:5155):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Tabs (ID: 1:5142)
  Khoảng cách giữa 'Tab Bar Item' (ID: 1:5143) và 'Tab Bar Item' (ID: 1:5146):
    Ngang: 0.00
    Dọc: 0.00
  Khoảng cách giữa 'Tab Bar Item' (ID: 1:5143) và 'Tab Bar Item' (ID: 1:5148):
    Ngang: 74.00
    Dọc: 0.00
  Khoảng cách giữa 'Tab Bar Item' (ID: 1:5143) và 'Tab Bar Item' (ID: 1:5151):
    Ngang: 149.00
    Dọc: 0.00
  Khoảng cách giữa 'Tab Bar Item' (ID: 1:5143) và 'Tab Bar Item' (ID: 1:5153):
    Ngang: 224.00
    Dọc: 0.00
  Khoảng cách giữa 'Tab Bar Item' (ID: 1:5146) và 'Tab Bar Item' (ID: 1:5148):
    Ngang: 0.00
    Dọc: 0.00
  Khoảng cách giữa 'Tab Bar Item' (ID: 1:5146) và 'Tab Bar Item' (ID: 1:5151):
    Ngang: 74.00
    Dọc: 0.00
  Khoảng cách giữa 'Tab Bar Item' (ID: 1:5146) và 'Tab Bar Item' (ID: 1:5153):
    Ngang: 149.00
    Dọc: 0.00
  Khoảng cách giữa 'Tab Bar Item' (ID: 1:5148) và 'Tab Bar Item' (ID: 1:5151):
    Ngang: 0.00
    Dọc: 0.00
  Khoảng cách giữa 'Tab Bar Item' (ID: 1:5148) và 'Tab Bar Item' (ID: 1:5153):
    Ngang: 74.00
    Dọc: 0.00
  Khoảng cách giữa 'Tab Bar Item' (ID: 1:5151) và 'Tab Bar Item' (ID: 1:5153):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Tab Bar Item (ID: 1:5143)
------------------------------------------------------------
Parent Node: Icon_Tab/Home_Fill (ID: 1:5144)
------------------------------------------------------------
Parent Node: Tab Bar Item (ID: 1:5146)
------------------------------------------------------------
Parent Node: Icon_Tab/Discover (ID: 1:5147)
  Khoảng cách giữa '_source' (ID: I1:5147;106:461) và 'discover' (ID: I1:5147;106:464):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: _source (ID: I1:5147;106:461)
  Khoảng cách giữa 'Oval 5 (Stroke)' (ID: I1:5147;106:462) và 'Vector 1 (Stroke)' (ID: I1:5147;106:463):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Tab Bar Item (ID: 1:5148)
------------------------------------------------------------
Parent Node: iconmonstr-shopping-cart-2 1 (ID: 1:5149)
------------------------------------------------------------
Parent Node: Tab Bar Item (ID: 1:5151)
------------------------------------------------------------
Parent Node: Icon_3pt/Bell (ID: 1:5152)
  Khoảng cách giữa '_source' (ID: I1:5152;106:449) và 'bell' (ID: I1:5152;106:453):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: _source (ID: I1:5152;106:449)
  Khoảng cách giữa 'Rectangle 535' (ID: I1:5152;106:450) và 'Vector 119' (ID: I1:5152;106:451):
    Ngang: 0.00
    Dọc: 0.00
  Khoảng cách giữa 'Rectangle 535' (ID: I1:5152;106:450) và 'Ellipse 159' (ID: I1:5152;106:452):
    Ngang: 0.00
    Dọc: 0.75
  Khoảng cách giữa 'Vector 119' (ID: I1:5152;106:451) và 'Ellipse 159' (ID: I1:5152;106:452):
    Ngang: 0.00
    Dọc: 13.00
------------------------------------------------------------
Parent Node: Tab Bar Item (ID: 1:5153)
------------------------------------------------------------
Parent Node: Icon/Person (ID: 1:5154)
  Khoảng cách giữa '_source' (ID: I1:5154;110:13783) và 'person' (ID: I1:5154;110:13784):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Home Indicator (ID: 1:5155)
------------------------------------------------------------
Parent Node: Status Bar (ID: 1:5157)
  Khoảng cách giữa 'Notch' (ID: 1:5158) và 'Right Side' (ID: 1:5163):
    Ngang: 0.00
    Dọc: 0.00
  Khoảng cách giữa 'Notch' (ID: 1:5158) và 'Left Side' (ID: 1:5179):
    Ngang: 3.00
    Dọc: 0.00
  Khoảng cách giữa 'Right Side' (ID: 1:5163) và 'Left Side' (ID: 1:5179):
    Ngang: 218.67
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Notch (ID: 1:5158)
  Khoảng cách giữa 'BG' (ID: 1:5159) và 'Exclude' (ID: 1:5160):
    Ngang: 0.00
    Dọc: 0.00
  Khoảng cách giữa 'BG' (ID: 1:5159) và 'Notch' (ID: 1:5162):
    Ngang: 0.00
    Dọc: 0.00
  Khoảng cách giữa 'Exclude' (ID: 1:5160) và 'Notch' (ID: 1:5162):
    Ngang: 0.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Exclude (ID: 1:5160)
------------------------------------------------------------
Parent Node: Right Side (ID: 1:5163)
  Khoảng cách giữa 'Battery' (ID: 1:5164) và 'Wifi' (ID: 1:5168):
    Ngang: 5.03
    Dọc: 0.00
  Khoảng cách giữa 'Battery' (ID: 1:5164) và 'Mobile Signal' (ID: 1:5172):
    Ngang: 25.33
    Dọc: 0.00
  Khoảng cách giữa 'Battery' (ID: 1:5164) và 'Recording Indicator' (ID: 1:5177):
    Ngang: 32.00
    Dọc: 3.33
  Khoảng cách giữa 'Wifi' (ID: 1:5168) và 'Mobile Signal' (ID: 1:5172):
    Ngang: 5.03
    Dọc: 0.00
  Khoảng cách giữa 'Wifi' (ID: 1:5168) và 'Recording Indicator' (ID: 1:5177):
    Ngang: 11.69
    Dọc: 3.33
  Khoảng cách giữa 'Mobile Signal' (ID: 1:5172) và 'Recording Indicator' (ID: 1:5177):
    Ngang: 0.00
    Dọc: 3.67
------------------------------------------------------------
Parent Node: Battery (ID: 1:5164)
  Khoảng cách giữa 'Rectangle' (ID: 1:5165) và 'Combined Shape' (ID: 1:5166):
    Ngang: 1.00
    Dọc: 0.00
  Khoảng cách giữa 'Rectangle' (ID: 1:5165) và 'Rectangle' (ID: 1:5167):
    Ngang: 0.00
    Dọc: 0.00
  Khoảng cách giữa 'Combined Shape' (ID: 1:5166) và 'Rectangle' (ID: 1:5167):
    Ngang: 3.00
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Wifi (ID: 1:5168)
  Khoảng cách giữa 'Wifi-path' (ID: 1:5169) và 'Wifi-path' (ID: 1:5170):
    Ngang: 0.00
    Dọc: 0.00
  Khoảng cách giữa 'Wifi-path' (ID: 1:5169) và 'Wifi-path' (ID: 1:5171):
    Ngang: 0.00
    Dọc: 2.85
  Khoảng cách giữa 'Wifi-path' (ID: 1:5170) và 'Wifi-path' (ID: 1:5171):
    Ngang: 0.00
    Dọc: 0.16
------------------------------------------------------------
Parent Node: Mobile Signal (ID: 1:5172)
  Khoảng cách giữa 'Cellular_Connection-path' (ID: 1:5173) và 'Cellular_Connection-path' (ID: 1:5174):
    Ngang: 1.67
    Dọc: 0.00
  Khoảng cách giữa 'Cellular_Connection-path' (ID: 1:5173) và 'Cellular_Connection-path' (ID: 1:5175):
    Ngang: 6.33
    Dọc: 0.00
  Khoảng cách giữa 'Cellular_Connection-path' (ID: 1:5173) và 'Cellular_Connection-path' (ID: 1:5176):
    Ngang: 11.00
    Dọc: 0.00
  Khoảng cách giữa 'Cellular_Connection-path' (ID: 1:5174) và 'Cellular_Connection-path' (ID: 1:5175):
    Ngang: 1.67
    Dọc: 0.00
  Khoảng cách giữa 'Cellular_Connection-path' (ID: 1:5174) và 'Cellular_Connection-path' (ID: 1:5176):
    Ngang: 6.33
    Dọc: 0.00
  Khoảng cách giữa 'Cellular_Connection-path' (ID: 1:5175) và 'Cellular_Connection-path' (ID: 1:5176):
    Ngang: 1.67
    Dọc: 0.00
------------------------------------------------------------
Parent Node: Recording Indicator (ID: 1:5177)
------------------------------------------------------------
Parent Node: Left Side (ID: 1:5179)
------------------------------------------------------------
Parent Node: Time (ID: 1:5180)
------------------------------------------------------------

```

Tất nhiên\! Tôi đã tạo một file Python mới tên là `calculate_distances.py` để trích xuất và tính toán khoảng cách giữa các đối tượng trong bảng thiết kế Figma của bạn.

Script này sẽ đi qua cấu trúc file JSON của Figma, tìm tất cả các node có thông tin về kích thước và vị trí (`absoluteBoundingBox`), sau đó tính toán khoảng cách ngang và dọc giữa các đối tượng "anh em ruột" (sibling) trong cùng một nhóm hoặc frame cha.

**Giải thích về cách tính khoảng cách:**

  * **Khoảng cách Ngang (Horizontal Distance):** Đây là khoảng cách ngắn nhất giữa cạnh phải của đối tượng bên trái và cạnh trái của đối tượng bên phải. Nếu các đối tượng chồng lên nhau theo chiều ngang, khoảng cách sẽ được coi là 0 (hoặc giá trị âm để thể hiện sự chồng lấn, trong trường hợp này tôi đã chỉnh về 0 cho dễ hiểu).
  * **Khoảng cách Dọc (Vertical Distance):** Tương tự, đây là khoảng cách ngắn nhất giữa cạnh dưới của đối tượng phía trên và cạnh trên của đối tượng phía dưới. Nếu chúng chồng lên nhau theo chiều dọc, khoảng cách sẽ là 0.

Dưới đây là nội dung của file `calculate_distances.py` và kết quả thực thi với file `figma_file.json` bạn đã cung cấp:

```python
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
            horz_dist = 0 # Consider overlap as 0 distance if asking for positive distance, or leave as negative for overlap

    # Calculate vertical distance
    vert_dist = 0
    if y1 + h1 < y2:  # node1 is above node2
        vert_dist = y2 - (y1 + h1)
    elif y2 + h2 < y1:  # node2 is above node1
        vert_dist = y1 - (y2 + h2)
    else:  # They overlap vertically
        vert_dist = max(y1, y2) - min(y1 + h1, y2 + h2)
        if vert_dist < 0:
            vert_dist = 0 # Consider overlap as 0 distance if asking for positive distance, or leave as negative for overlap

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
                    print(f"  Khoảng cách giữa '{node1.get('name', 'Unknown')}' (ID: {node1['id']}) và '{node2.get('name', 'Unknown')}' (ID: {node2['id']}):")
                    print(f"    Ngang: {h_dist:.2f}")
                    print(f"    Dọc: {v_dist:.2f}")
        print("-" * 60)

if __name__ == "__main__":
    main()
```

**Hướng dẫn sử dụng:**

1.  Lưu đoạn code trên vào một file tên `calculate_distances.py`.
2.  Đảm bảo file JSON từ Figma của bạn có tên là `figma_file.json` và nằm cùng thư mục với script này.
3.  Chạy lệnh sau trong terminal:
    ```bash
    python calculate_distances.py
    ```

**Kết quả từ file của bạn:**

Chương trình đã thực hiện tính toán và in ra khoảng cách giữa các đối tượng con trực tiếp trong cùng một phần tử cha. Ví dụ, trong "Ecommerce" (ID: 1:5055) có nhiều "Row" và "Banner" với các khoảng cách ngang và dọc được liệt kê.

Bạn có thể thấy kết quả chi tiết trong phần đầu ra của code, hiển thị khoảng cách ngang và dọc (đã làm tròn đến 2 chữ số thập phân) giữa các cặp đối tượng trong từng node cha.