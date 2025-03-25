```python
"""
1.  **Identify and Extract Objects:** Locate all connected regions (objects) of color 2 (red) and color 3 (green) within the input grid.
2.  **Compute Bounding Box** Find the bounding box that contains all identified red and green objects in the original input grid.
3.  **Stack Objects:** Stack the extracted objects vertically, maintaining their original horizontal positions relative to each other.  The objects are stacked from top to bottom based on their order in the original image.
4.  **Create Azure Bar:** Create a horizontal bar of color 8 (azure) below the stacked objects. The width of the bar spans the entire width from the minimum column to the maximum column of the bounding box identified in step 2, and height 1.
5. **Determine and Create Output Grid:** Create output grid. Keep the original background, and add the stacked objects and azure bar in the location specified by rules 3 & 4.
"""

import numpy as np

def find_objects(grid, colors):
    """
    Finds connected regions of specified colors in the grid.
    Returns a list of (object, color) tuples.
    """
    visited = set()
    objects = []

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(row + dr, col + dc, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] in colors and (row, col) not in visited:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                objects.append((current_object, grid[row, col]))
    return objects

def get_bounding_box(objects):
    """
    Compute the bounding box for a list of objects.
    """
    if not objects:
        return None

    min_row = float('inf')
    min_col = float('inf')
    max_row = float('-inf')
    max_col = float('-inf')

    for obj, _ in objects:
        for row, col in obj:
            min_row = min(min_row, row)
            max_row = max(max_row, row)
            min_col = min(min_col, col)
            max_col = max(max_col, col)

    return (min_row, min_col, max_row, max_col)

def get_object_height(obj):
    """Calculates the height of an object."""
    rows = [r for r, _ in obj]
    return max(rows) - min(rows) + 1

def transform(input_grid):
    input_grid = np.array(input_grid)

    # 1. Identify and Extract Objects
    objects = find_objects(input_grid, [2, 3])

    # 2. Compute Bounding Box (in original grid)
    bounding_box = get_bounding_box(objects)
    if bounding_box is None:
        return input_grid.tolist()  # No objects to transform
    min_row_all, min_col_all, max_row_all, max_col_all = bounding_box

    # 3. Stack Objects and 4. Create Azure Bar
    output_grid = np.array(input_grid).tolist() # start with a copy
    
    # remove objects from original grid
    for obj, _ in objects:
      for r,c in obj:
        output_grid[r][c] = 0

    current_row = min_row_all  # Start stacking at the top-most object's row
    for obj, color in objects:
        obj_height = get_object_height(obj)
        min_row_obj = min([r for r,_ in obj])
        for r, c in obj:
           
            new_c = c - min_col_all + min_col_all # maintain col
            output_grid[current_row + (r - min_row_obj)][new_c] = color
        current_row += obj_height

    # Create Azure Bar
    azure_row = current_row
    for col in range(min_col_all, max_col_all+1):
      output_grid[azure_row][col] = 8


    return output_grid
```