"""
1.  **Identify the Background:** The background color is consistently '0' (white) in all examples.
2.  **Find Objects:** Identify all contiguous regions of non-background colors. These are the objects.
3.  **Determine Output Size:** The output size is determined by adding 2 to both dimensions (height and width) of the bounding box that encompasses *all* objects in the input.  This creates a one-pixel wide space on all sides for the border.
4.  **Create Output Grid:** Create a new grid of the determined size, filled with the background color (0/white).
5.  **Apply Border:** Fill the outermost rows and columns of the output grid with magenta (color 6).
6.  **Copy Objects:** Copy each object from the input grid to the output grid, preserving its shape, color, and relative position within the bounding box. The objects are placed such that the top-left corner of their bounding box in the input is offset by (1, 1) in the output grid (due to the border).
7.  **Fill Background:** Ensure the background within the border is the same as the identified background color (0).
"""

import numpy as np
from collections import Counter

def find_background_color(grid):
    """
    Finds the most frequent color in the grid.  In this specific task, it's
    always 0.  However, we keep the function for generality.
    """
    color_counts = Counter(grid.flatten())
    return color_counts.most_common(1)[0][0]

def find_objects(grid, background_color):
    """Finds objects in the grid, excluding the background color."""
    objects = {}
    for color in np.unique(grid):
        if color != background_color:
            objects[color] = np.argwhere(grid == color)
    return objects

def determine_output_size(objects, input_grid):
    """Determines the size of the output grid based on object extents, including border."""
    min_row, min_col = float('inf'), float('inf')
    max_row, max_col = float('-inf'), float('-inf')

    for color_objects in objects.values():
        for row, col in color_objects:
            min_row = min(min_row, row)
            min_col = min(min_col, col)
            max_row = max(max_row, row)
            max_col = max(max_col, col)
            
    input_height, input_width = input_grid.shape

    # Calculate output size based on bounding box and border
    output_height = max_row - min_row + 3
    output_width = max_col - min_col + 3
    
    return output_height, output_width, min_row, min_col

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
    background_color = find_background_color(input_grid)  # Usually 0

    # 2. Find Objects
    objects = find_objects(input_grid, background_color)

    # 3. Determine Output Size
    output_height, output_width, row_offset, col_offset = determine_output_size(objects, input_grid)

    # 4. Create Output Grid
    output_grid = create_bordered_grid(output_height, output_width, background_color, border_color=6)

    # 5. (Border is already applied in create_bordered_grid)

    # 6. Copy Objects
    for color, positions in objects.items():
        for row, col in positions:
            new_row = row - row_offset + 1  # +1 for the border offset
            new_col = col - col_offset + 1  # +1 for the border offset
            output_grid[new_row, new_col] = color

    # 7. (Background is already filled by create_bordered_grid)

    return output_grid