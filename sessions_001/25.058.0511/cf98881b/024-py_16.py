"""
1.  **Identify Unique Colors:** Determine the set of unique colors present in the input grid.
2.  **Determine Output Grid Width:** The output grid's width equals the number of unique colors in the input grid.
3. **Determine Output Grid Height:** The output grid's height equals the input's height.
4.  **Column Selection:** For each row, select the pixel values of the columns corresponding to the first appearance of a unique color. If there are multiple appearances, select the leftmost instance. The order is given by the column order of first occurrence.
5.  **Construct Output Grid:** Create a new grid, preserving row order and placing selected column contents, and stack these together, left-to-right based on unique color order.
"""

import numpy as np

def get_unique_colors(grid):
    # Flatten the grid and get unique colors
    return np.unique(grid)

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Identify Unique Colors
    unique_colors = get_unique_colors(input_grid)

    # Determine output grid dimensions
    output_width = len(unique_colors)
    output_height = rows
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Column Selection and Output Construction
    color_column_map = {}  # Map color to its first occurring column
    for color in unique_colors:
        color_column_map[color] = -1

    for j in range(cols):
      color_at_j = input_grid[0,j]
      if color_column_map[color_at_j] == -1:
        color_column_map[color_at_j] = j

    sorted_colors = sorted(color_column_map.keys(), key=lambda color: color_column_map[color])

    
    for i, color in enumerate(sorted_colors):
        col_index = color_column_map[color]
        if (col_index != -1): #check the color was present
          output_grid[:, i] = input_grid[:, col_index]
        # else the output grid section remains zeros, as initialized

    return output_grid.tolist()