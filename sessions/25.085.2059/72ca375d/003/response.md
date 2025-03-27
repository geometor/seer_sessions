```python
"""
Identifies all distinct contiguous objects (connected groups of same non-white pixels using 4-connectivity) in the input grid.
Sorts these objects based on their color index (the integer value 1-9).
Selects the second object from this sorted list.
Creates the output grid by taking the minimal bounding box around the selected object and filling it with the object's pixels, leaving other cells within the bounding box as background (white, 0).
"""

import numpy as np
from collections import deque

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-white color in the grid.
    Uses 4-connectivity.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color' (int), 'coords' (set of (row, col) tuples),
              'size' (int), and 'bbox' (tuple: min_row, min_col, max_row, max_col).
              The list is sorted by object color index.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):
            # Check if the cell is part of the grid, not background, and not visited
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                # Use a separate set to track visited cells *within the current object search*
                # to avoid issues if find_objects is called multiple times or grid changes
                current_obj_visited_in_loop = {(r, c)} 

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, correct color, and not visited globally or in this specific object search
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and \
                           (nr, nc) not in visited and \
                           (nr, nc) not in current_obj_visited_in_loop:
                            visited.add((nr, nc))
                            current_obj_visited_in_loop.add((nr, nc))
                            q.append((nr, nc))

                if obj_coords:
                    # Calculate bounding box
                    min_r = min(coord[0] for coord in obj_coords)
                    max_r = max(coord[0] for coord in obj_coords)
                    min_c = min(coord[1] for coord in obj_coords)
                    max_c = max(coord[1] for coord in obj_coords)
                    bbox = (min_r, min_c, max_r, max_c)
                    
                    objects.append({
                        'color': color,
                        'coords': obj_coords,
                        'size': len(obj_coords),
                        'bbox': bbox
                    })

    # Sort objects primarily by color index
    objects.sort(key=lambda obj: obj['color'])
    return objects

def get_bounding_box(coords):
    """
    Calculates the minimal bounding box for a set of coordinates.

    Args:
        coords (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if coords is empty.
    """
    if not coords:
        return None
    min_row = min(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_row = max(r for r, c in coords)
    max_col = max(c for r, c in coords)
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # 1. Find all objects and sort them by color index
    objects = find_objects(input_grid)

    # 2. Check if there are enough objects to select the second one
    if len(objects) < 2:
        # Handle edge case: Not enough objects found.
        # Based on examples, this shouldn't happen, but return empty grid as fallback.
        return np.array([[0]]) # Or potentially raise an error

    # 3. Select the second object (index 1) in the sorted list
    selected_object = objects[1]

    # 4. Get the bounding box of the selected object
    # The bounding box is already calculated in find_objects
    bbox = selected_object['bbox']
    min_row, min_col, max_row, max_col = bbox

    # 5. Create the output grid based on the bounding box size
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    # Initialize with background color (0)
    output_grid = np.zeros((output_height, output_width), dtype=int) 

    # 6. Populate the output grid with the pixels of the selected object
    object_color = selected_object['color']
    for r, c in selected_object['coords']:
        # Calculate relative coordinates within the output grid
        relative_r = r - min_row
        relative_c = c - min_col
        # Place the object's color in the corresponding cell
        output_grid[relative_r, relative_c] = object_color

    return output_grid
```