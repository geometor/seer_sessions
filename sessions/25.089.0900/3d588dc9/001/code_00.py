import numpy as np
from collections import deque

"""
Identify the single contiguous object composed of gray (5) pixels and all 
contiguous objects composed of white (0) pixels. Determine their bounding boxes.
Filter the white objects to find only those that share at least one row with the 
gray object. From this filtered set, select the white object that has the 
minimum horizontal distance (gap size) to the gray object. Determine if the 
selected white object is to the left or right of the gray object. If it's to 
the left, identify its rightmost column index. If it's to the right, identify 
its leftmost column index. Create the output grid by copying the input grid. 
Modify the output grid by changing the color of all pixels within the selected 
white object that fall into the identified column to magenta (6).
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'coords' (a set of (r, c) tuples) and 'bbox'
              (a dictionary with 'row_min', 'row_max', 'col_min', 'col_max').
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if obj_coords:
                    bbox = {'row_min': min_r, 'row_max': max_r, 'col_min': min_c, 'col_max': max_c}
                    objects.append({'coords': obj_coords, 'bbox': bbox})
    return objects

def check_row_overlap(box1, box2):
    """Checks if two bounding boxes overlap vertically."""
    return not (box1['row_max'] < box2['row_min'] or box1['row_min'] > box2['row_max'])

def horizontal_distance(box1, box2):
    """Calculates the minimum horizontal gap between two bounding boxes."""
    if box1['col_max'] < box2['col_min']:
        # box1 is to the left of box2
        return box2['col_min'] - box1['col_max'] - 1
    elif box2['col_max'] < box1['col_min']:
        # box2 is to the left of box1
        return box1['col_min'] - box2['col_max'] - 1
    else:
        # Boxes overlap horizontally or touch
        return 0 # Or could return a negative value for overlap, but 0 is fine for finding minimum gap

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)
    gray_color = 5
    white_color = 0
    magenta_color = 6

    # 1. Identify the gray object
    gray_objects = find_objects(input_grid, gray_color)
    if not gray_objects:
        return output_grid # No gray object, no change
    # Assuming only one gray object based on examples
    gray_obj = gray_objects[0]
    gray_bbox = gray_obj['bbox']

    # 2. Identify all white objects
    white_objects = find_objects(input_grid, white_color)
    if not white_objects:
        return output_grid # No white objects, no change

    # 3. Filter white objects that share rows with the gray object
    candidate_white_objects = []
    for w_obj in white_objects:
        if check_row_overlap(gray_bbox, w_obj['bbox']):
            candidate_white_objects.append(w_obj)

    if not candidate_white_objects:
        return output_grid # No white objects share rows with gray object

    # 4. Calculate horizontal distance and find the closest white object
    min_dist = float('inf')
    selected_white_obj = None
    for w_obj in candidate_white_objects:
        dist = horizontal_distance(gray_bbox, w_obj['bbox'])
        # Ensure distance is non-negative (i.e., they don't overlap horizontally)
        # Although the description implies closest, the examples show modification only happens when separated
        if dist >= 0 and dist < min_dist:
            min_dist = dist
            selected_white_obj = w_obj
        # Tie-breaking: if distances are equal, current logic picks the first one found.
        # Could add other criteria if needed (e.g., largest object, highest object). Based on examples, simple min distance seems sufficient.

    if selected_white_obj is None:
        return output_grid # No suitable white object found

    # 5. Determine which column to modify
    selected_bbox = selected_white_obj['bbox']
    col_to_modify = -1
    if selected_bbox['col_max'] < gray_bbox['col_min']:
        # White object is to the left of gray object
        col_to_modify = selected_bbox['col_max']
    elif selected_bbox['col_min'] > gray_bbox['col_max']:
        # White object is to the right of gray object
        col_to_modify = selected_bbox['col_min']
    else:
         # This case (horizontal overlap) should ideally not happen based on selection criteria,
         # but if it did, no modification would occur according to the rule's interpretation.
         return output_grid

    # 6. Apply the modification
    if col_to_modify != -1:
        for r, c in selected_white_obj['coords']:
            if c == col_to_modify:
                output_grid[r, c] = magenta_color

    return output_grid