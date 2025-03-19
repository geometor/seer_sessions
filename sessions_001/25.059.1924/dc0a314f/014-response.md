# dc0a314f • 014 • refine_coder

---
```python
"""
1. **Identify Target Object:** Find the contiguous region (object) in the input grid that contains pixels of color orange (7) and/or red (2). This is the "target object."  Pixels of other colors, and the background (0), are ignored when identifying this object.

2.  **Determine Target Object Bounding Box:** Calculate the bounding box of the target object. This is the smallest rectangle that encloses all pixels of the target object.  The bounding box is defined by:
    *   `min_row`: The smallest row index of any pixel in the target object.
    *   `min_col`: The smallest column index of any pixel in the target object.
    *   `max_row`: The largest row index of any pixel in the target object.
    *   `max_col`: The largest column index of any pixel in the target object.

3.  **Extract Subgrid (Output):** Extract the rectangular subgrid defined by the target object's bounding box. The extracted subgrid has:

    *   Height: `max_row - min_row + 1`
    *   Width: `max_col - min_col + 1`
    *   Top-left corner coordinates: (`min_row`, `min_col`)
    * get data from `input_grid` using these coordinates

4.  **Output:** The extracted subgrid is the output.
"""

import numpy as np

def find_target_object(grid):
    # Find the contiguous region containing colors 7 and 2
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    target_object = []

    def is_target_color(color):
        return color == 7 or color == 2

    def dfs(row, col):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or not is_target_color(grid[row, col])
        ):
            return []

        visited[row, col] = True
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))
        return region

    for r in range(rows):
        for c in range(cols):
            if is_target_color(grid[r, c]) and not visited[r, c]:
                target_object = dfs(r, c)
                # Return after finding the first target object.  We assume there is only one
                return target_object
    return target_object

def get_bounding_box(target_object):
    # input is list of (row, col) tuples
    if not target_object:
        return (0, 0, -1, -1) # Handle empty target object case

    rows, cols = zip(*target_object) # separate row and col
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the target object (contiguous region of colors 7 and 2)
    target_object = find_target_object(input_grid)

    # if nothing found, return empty grid
    if not target_object: return [[]]

    # Get the bounding box
    min_row, min_col, max_row, max_col = get_bounding_box(target_object)

    # Extract subgrid
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1].tolist()
    
    return output_grid
```
