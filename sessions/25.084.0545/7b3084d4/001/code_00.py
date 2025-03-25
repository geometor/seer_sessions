"""
1.  **Identify Colored Regions:** Scan the input grid to find contiguous regions of non-white (non-0) pixels. Consider these regions as individual "objects."
2.  **Order by y-axis:** Order the regions from top to bottom. If they have the same top y coordinate, order by x axis, from left to right.
3. **Select Regions:** Select a subset, up to 4 regions.
4.  **Extract Sub-grids:** For each of the regions create a sub-grid, keeping only the minimum rectangle to contain the shape.
5.  **Concatenate Sub-grids:**  Stack the extracted sub-grids horizontally, left to right, to form the output grid.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions of non-zero pixels."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj_coords):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def order_objects(objects):
    """Orders objects by top-left corner (y then x)."""
    def get_top_left(obj):
        return min(obj, key=lambda x: (x[0], x[1]))
    return sorted(objects, key=lambda obj: get_top_left(obj))

def extract_subgrids(grid, objects):
    """Extracts subgrids for each object."""
    subgrids = []
    for obj in objects:
        min_r = min(obj, key=lambda x: x[0])[0]
        max_r = max(obj, key=lambda x: x[0])[0]
        min_c = min(obj, key=lambda x: x[1])[1]
        max_c = max(obj, key=lambda x: x[1])[1]
        subgrids.append(grid[min_r:max_r + 1, min_c:max_c + 1])
    return subgrids

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    # Find contiguous non-zero regions (objects)
    objects = find_objects(input_grid)

    # Order objects by top-left corner (y then x)
    ordered_objects = order_objects(objects)
    
    # Select the first 4 objects
    selected_objects = ordered_objects[:4]
    
    # Extract subgrids for selected objects
    subgrids = extract_subgrids(input_grid, selected_objects)

    # Concatenate subgrids horizontally
    if subgrids:
      output_grid = np.concatenate(subgrids, axis=1)
    else:
      output_grid = np.array([])

    return output_grid