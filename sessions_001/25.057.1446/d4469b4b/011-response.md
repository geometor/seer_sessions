# d4469b4b • 011 • refine_coder

---
```python
"""
1.  **Identify the Blue Rectangle:** Find the smallest rectangular region within the input grid that contains all the blue (color 1) pixels. This is the "bounding box."

2.  **Create Output Grid:** Create a new grid. The dimensions of this grid should be equal to the height and width of the bounding box found in step 1.

3.  **Map Pixels:**
    - Iterate over each cell of the newly created output grid.
    - If the corresponding pixel location inside the input's bounding box area is blue, set the ouput's cell to grey.
    - If the corresponding pixel location inside the input's bounding box area is not blue, set the output's cell to black.
    - The rest of the input grid outside the bounding box is ignored

4.  **Return Output:** The resulting output grid is the transformed output.
"""

import numpy as np

def get_bounding_box(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # Find bounding box of blue pixels (color 1)
    bounding_box = get_bounding_box(input_grid, 1)
    if bounding_box is None:
        return np.zeros((1, 1), dtype=int)  # Handle cases where the color doesn't exist

    min_row, max_row, min_col, max_col = bounding_box

    # Create output grid based on bounding box dimensions
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Map input pixels within the bounding box to the output grid
    for i in range(output_height):
        for j in range(output_width):
            input_row = min_row + i
            input_col = min_col + j
            if input_grid[input_row, input_col] == 1:
                output_grid[i, j] = 5
            else:
                output_grid[i, j] = 0

    return output_grid
```
