# a3325580 • 036 • refine_coder

---
```python
"""
1. **Identify Objects:** Find all distinct connected regions (objects) of non-white pixels in the input grid. Record the color, shape (as a set of pixel coordinates), and bounding box (min/max row and column) of each object.

2. **Transformation Rules:**
    *   **Rule 1 (Vertical Extension):** If the input contains multiple objects and they can be arranged from left to right based on increasing column value, transform each object into a vertical line of the same color. The height of each output line is the maximum height of all identified objects, the width is 1 and arranged from left to right.
    *   **Rule 2 (Bounding Box Fill):** If the input contains a single object, create an output grid with dimensions equal to the bounding box of the input object, and fill it with the object's color.
    *   **Rule 3 (Identity):** If the input is a filled rectangle (the number of pixels equals height * width of bounding box), the output is identical to the input.
    *   **Rule 4 (Unidentified):** If none of the above rules apply, no transformation can yet be determined,
"""

import numpy as np

def find_objects(grid):
    """Find connected regions of non-zero pixels."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj_pixels):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj_pixels.append((r, c))
        dfs(r + 1, c, color, obj_pixels)
        dfs(r - 1, c, color, obj_pixels)
        dfs(r, c + 1, color, obj_pixels)
        dfs(r, c - 1, color, obj_pixels)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                obj_pixels = []
                dfs(r, c, grid[r, c], obj_pixels)
                if obj_pixels:
                    objects.append((grid[r,c], obj_pixels))
    return objects

def get_bounding_box(pixels):
    """Calculates the bounding box of a set of pixels."""
    rows = [p[0] for p in pixels]
    cols = [p[1] for p in pixels]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, max_row, min_col, max_col

def is_filled_rectangle(pixels, bounding_box):
    """Checks if a set of pixels forms a filled rectangle."""
    min_row, max_row, min_col, max_col = bounding_box
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return len(pixels) == height * width

def transform(input_grid):
    input_grid = np.array(input_grid)
    objects = find_objects(input_grid)

    # Rule 1: Vertical Extension
    if len(objects) > 1:
        # Sort objects by their leftmost column
        sorted_objects = sorted(objects, key=lambda obj: min(p[1] for p in obj[1]))

        # Get max height
        max_height = 0
        for _, pixels in objects:  # Use original objects for height calculation
            _, max_row, _, _ = get_bounding_box(pixels)
            max_height = max(max_height, max_row)

        # Check if objects can be arranged left-to-right (non-overlapping columns)
        valid_arrangement = True
        for i in range(len(sorted_objects) - 1):
            _, _, _, max_col1 = get_bounding_box(sorted_objects[i][1])
            _, _, min_col2, _ = get_bounding_box(sorted_objects[i+1][1])
            if max_col1 >= min_col2:
                valid_arrangement = False
                break

        if valid_arrangement:
             output_height = max_height + 1 # correct for zero index
             output_width = len(sorted_objects)
             output_grid = np.zeros((output_height, output_width), dtype=int)

             for i, (color, _) in enumerate(sorted_objects):
                for j in range(output_height):
                    output_grid[j,i] = color
             return output_grid

    # Rule 2: Bounding Box Fill
    if len(objects) == 1:
        color, pixels = objects[0]
        min_row, max_row, min_col, max_col = get_bounding_box(pixels)
        height = max_row - min_row + 1
        width = max_col - min_col + 1

        # Rule 3: Identity (check if already a filled rectangle)
        if is_filled_rectangle(pixels, (min_row, max_row, min_col, max_col)):
            return input_grid.copy()

        output_grid = np.full((height, width), color, dtype=int)
        return output_grid

    # Rule 4: Unidentified - return a default 2x2 orange grid for now.
    return np.array([[7, 7], [7, 7]])
```
