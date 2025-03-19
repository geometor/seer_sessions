# fafffa47 • 004 • refine_coder

---
```python
"""
1.  **Identify** the maroon (9) object within the input grid.
2.  **Determine Output Dimensions**: The output grid dimensions match the height and width of the bounding box of the maroon object.
3.  **Extract** the entire maroon object from the input grid.
4.  **Change** the color of the extracted object from maroon (9) to red (2).
5.  **Create** an output grid of the determined dimensions, filling it entirely with the modified (red) object. Any remaining area is implicitly filled by the object, as it fills the entire output grid.
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of all cells with the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None  # Return None if color not found
    min_row = coords[:, 0].min()
    max_row = coords[:, 0].max()
    min_col = coords[:, 1].min()
    max_col = coords[:, 1].max()
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find the maroon object (color 9).
    min_row, max_row, min_col, max_col = find_object(input_grid, 9)
    
    if min_row is None:  # Handle cases where no maroon object is found
      return np.zeros((0, 0), dtype=int)

    # Determine output dimensions based on the maroon object's bounding box.
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1

    # Initialize output_grid with the correct dimensions.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Extract the entire maroon object and change color to red (2).
    for i in range(min_row, max_row + 1):
        for j in range(min_col, max_col + 1):
            output_grid[i - min_row, j - min_col] = 2

    return output_grid
```

