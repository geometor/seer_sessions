# 4290ef0e • 006 • refine_coder

---
```python
"""
1.  **Identify the Background:** Determine the most frequent color in the input grid. This is the background color.
2.  **Find Objects:** Identify all contiguous regions of non-background colors. These are the objects.
3.  **Determine Output Size:** Find the smallest rectangular area that can enclose all identified objects. Add 1 to all sides, this will be the space for the border.
4.  **Create Output Grid:** Create a new grid of the determined size.
5.  **Apply Border:** Fill the outermost rows and columns of the output grid with magenta (color 6).
6.  **Copy Objects:** Copy each object from the input grid to the output grid, preserving its shape, color and relative position.
7.  **Fill Background:** Fill the any area within the border, not already occupied by another object with the input background color.
"""

import numpy as np
from collections import Counter

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    color_counts = Counter(grid.flatten())
    return color_counts.most_common(1)[0][0]

def find_objects(grid, background_color):
    """Finds objects in the grid, excluding the background color."""
    objects = {}
    for color in np.unique(grid):
        if color != background_color:
            objects[color] = np.argwhere(grid == color)
    return objects

def determine_output_size(objects):
    """Determines the size of the output grid based on object extents, including border."""
    min_row, min_col = float('inf'), float('inf')
    max_row, max_col = float('-inf'), float('-inf')

    for color_objects in objects.values():
        for row, col in color_objects:
            min_row = min(min_row, row)
            min_col = min(min_col, col)
            max_row = max(max_row, row)
            max_col = max(max_col, col)

    return max_row - min_row + 3, max_col - min_col + 3, min_row, min_col # +3 for border on all sides

def create_bordered_grid(height, width, background_color, border_color=6):
    """Creates a grid with a border and background color."""
    grid = np.full((height, width), background_color)
    grid[0, :] = border_color
    grid[-1, :] = border_color
    grid[:, 0] = border_color
    grid[:, -1] = border_color
    return grid

def transform(input_grid):
    """Transforms the input grid to the output grid based on the defined rules."""

    # 1. Identify the Background
    background_color = find_background_color(input_grid)

    # 2. Find Objects
    objects = find_objects(input_grid, background_color)

    # 3. Determine Output Size
    output_height, output_width, row_offset, col_offset = determine_output_size(objects)

    # 4. Create Output Grid
    output_grid = create_bordered_grid(output_height, output_width, background_color)

    # 5. (Border is already applied in create_bordered_grid)

    # 6. Copy Objects
    for color, positions in objects.items():
        for row, col in positions:
            new_row = row - row_offset + 1  # +1 for the border offset
            new_col = col - col_offset + 1
            output_grid[new_row, new_col] = color

    # 7. (Background is already filled by create_bordered_grid)

    return output_grid
```
