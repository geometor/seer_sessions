# 5c0a986e • 008 • refine_coder

---
```python
"""
The transformation rule identifies contiguous regions (objects) of the same non-zero color in the input grid. For each such region, it constructs a '+' shape in the output grid. The center of the '+' is positioned at the center of the bounding box of the region, and the color of the '+' matches the color of the region. The size of '+' arms is not fixed, but related to bounding box.

The previous code was fixated on 2x2 squares, this extends it to work on bounding boxes of all sizes.
"""

import numpy as np

def get_bounding_box(grid, color):
    """Finds the bounding box of a contiguous region of the given color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # No pixels of the given color
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.zeros_like(input_grid)  # Initialize with zeros
    unique_colors = np.unique(input_grid)
    
    for color in unique_colors:
        if color != 0:  # Skip background color
            bbox = get_bounding_box(input_grid, color)
            if bbox:
                min_row, max_row, min_col, max_col = bbox
                center_row = (min_row + max_row) // 2
                center_col = (min_col + max_col) // 2

                # Determine arm length based on bounding box size.
                # This is a heuristic; we might need to adjust the formula.
                row_length = max_row - min_row + 1
                col_length = max_col - min_col + 1

                arm_length_row = row_length // 2 
                arm_length_col = col_length // 2

                # Create '+' shape
                for i in range(max(0, center_row - arm_length_row), min(output_grid.shape[0], center_row + arm_length_row + 1)):
                    output_grid[i, center_col] = color
                for j in range(max(0, center_col - arm_length_col), min(output_grid.shape[1], center_col + arm_length_col + 1)):
                    output_grid[center_row, j] = color

    return output_grid
```
