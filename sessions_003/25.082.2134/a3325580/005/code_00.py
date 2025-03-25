"""
1.  **Identify Common Colors:** Determine the set of colors that are present in *both* the input and output grids. Ignore color 0 (background).

2.  **Identify Relevant Rows:** Find the rows in the input grid that contain *any* of the common colors.

3. **Identify Bounding Box:** Find the smallest and largest row and column containing any of the common colors. The output dimensions is based on the smallest rectangle encompassing all the common colors.

4.  **Construct Output:**
    *   Create a new output grid. The dimensions are determined by the bounding box (number of rows by the number of common colors).
    * The height is the difference between max_row and min_row of common colors + 1.
    * The width is the number of common colors.
    * Each row in the output will be filled with the common colors, in sorted, ascending order.
"""

import numpy as np

def get_common_colors(input_grid, output_grid):
    """Finds common non-zero colors between input and output grids."""
    input_colors = set(input_grid.flatten())
    output_colors = set(output_grid.flatten())
    common_colors = sorted(list(input_colors.intersection(output_colors)))
    return [c for c in common_colors if c != 0]

def get_bounding_box(input_grid, common_colors):
    """Finds the bounding box of common colors in the input grid."""
    rows, cols = [], []
    for color in common_colors:
        color_positions = np.where(input_grid == color)
        if len(color_positions[0]) > 0:  # Check if the color exists
            rows.extend(color_positions[0])
            cols.extend(color_positions[1])
    
    if not rows: # Handle the case where no common colors are found
        return 0, 0, 0, 0

    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid, output_grid):  # Added output_grid as a parameter
    # Identify common colors
    common_colors = get_common_colors(input_grid, output_grid)

    # Handle the edge case where there are no common colors
    if not common_colors:
        return np.array([[]], dtype=int)

    # Identify bounding box
    min_row, max_row, min_col, max_col = get_bounding_box(input_grid, common_colors)

    # Construct output grid
    output_height = max_row - min_row + 1
    output_width = len(common_colors)
    output_grid_result = np.zeros((output_height, output_width), dtype=int)

    for i in range(output_height):
        output_grid_result[i, :] = sorted(common_colors)

    return output_grid_result