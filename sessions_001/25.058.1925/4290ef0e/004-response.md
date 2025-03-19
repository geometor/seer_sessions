# 4290ef0e • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Key Regions:** In the input grid, identify the distinct colored regions: the blue (1) squares, the green (3) cluster, the magenta (6) shapes, and the yellow background (4).

2.  **Create a Smaller Grid:** the output grid size can be pre-determined by the maximum extend of the non yellow regions.

3. **Magenta (6) Border:** create a border around the new, smaller grid using magenta color (6).

4.  **Inner Content:** Fill the area within the magenta border, from outermost to the middle:

    *   Copy to the new grid the blue squares, maintaining the count and general shape.
    *   Copy any green cluster preserving color and relative spatial relationships.
    *   The background is yellow (4).

In summary: Create an output grid of size pre-determined and where the non-yellow regions fit, frame it with a magenta border, copy the blue square shape, copy the green cluster, and the remaining areas are yellow.
"""

import numpy as np

def find_objects(grid, background_color=4):
    """
    Finds objects in the grid, excluding the background color.
    Returns a dictionary of objects keyed by color.
    """
    objects = {}
    for color in np.unique(grid):
        if color != background_color:
            objects[color] = np.argwhere(grid == color)
    return objects

def determine_output_size(objects):
    """
    Determines the size of the output grid based on the maximum extents of non-background objects.
    """
    min_row, min_col = float('inf'), float('inf')
    max_row, max_col = float('-inf'), float('-inf')

    for color_objects in objects.values():
        for row, col in color_objects:
            min_row = min(min_row, row)
            min_col = min(min_col, col)
            max_row = max(max_row, row)
            max_col = max(max_col, col)

    return max_row - min_row + 1, max_col - min_col + 1, min_row, min_col

def create_bordered_grid(height, width, border_color=6):
    """
    Creates a grid with a border of the specified color.
    """
    grid = np.full((height, width), 4)  # Initialize with yellow (background)
    grid[0, :] = border_color  # Top border
    grid[-1, :] = border_color  # Bottom border
    grid[:, 0] = border_color  # Left border
    grid[:, -1] = border_color  # Right border
    return grid

def transform(input_grid):
    """
    Transforms the input grid into the output grid according to the defined rules.
    """
    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Determine output grid size and offset
    output_height, output_width, row_offset, col_offset = determine_output_size(objects)

     # Adjust output size to accommodate the magenta border
    output_height += 2
    output_width += 2

    # Create output grid with magenta border
    output_grid = create_bordered_grid(output_height, output_width)

    # Copy objects to the output grid, adjusting for the offset and the border
    for color, positions in objects.items():
        for row, col in positions:
            new_row = row - row_offset + 1
            new_col = col - col_offset + 1
            # Only copy if the new position is within the inner part of the output_grid
            if 0 < new_row < output_height-1 and 0 < new_col < output_width -1:
              output_grid[new_row, new_col] = color

    return output_grid
```
