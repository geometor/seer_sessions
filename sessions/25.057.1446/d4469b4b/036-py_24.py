"""
The transformation extracts a centered subgrid from the input and applies a color transformation based on the non-white color present in the subgrid.

1.  **Input:** Begin with an input grid of size *N*x*M*.
2.  **Output Size:** Determine the output grid size as (*N*-2)x(*M*-2).
3.  **Subgrid Extraction:** Extract the subgrid from the input that corresponds to the output grid size, centered within the input.
4.  **Identify Non-White Color:** Find the single non-white color present in the extracted subgrid.
5.  **Color Transformation:** Apply color transformation to every cell in the extracted subgrid:
    *   If the cell is red (2), change it to gray (5).
    *   If the cell is blue (1), change it to red (2).
    *   If the cell is green (3), change it to yellow (4).
    *   If the cell is gray (5), change it to magenta (6).
    *   If the cell is white (0), it remains white (0).
6.  **Output:** The output grid contains the transformed subgrid.
"""

import numpy as np

def get_center_subgrid(grid, subgrid_size):
    """
    Extracts a subgrid centered within the input grid.
    """
    grid_height, grid_width = grid.shape
    subgrid_height, subgrid_width = subgrid_size

    start_row = (grid_height - subgrid_height) // 2
    end_row = start_row + subgrid_height
    start_col = (grid_width - subgrid_width) // 2
    end_col = start_col + subgrid_width

    return grid[start_row:end_row, start_col:end_col]

def find_non_white_color(grid):
    """
    Finds the single non-white color in the grid. Returns None if only white is present.
    """
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0:
            return color
    return None

def transform(input_grid):
    # Determine output size
    input_size = np.array(input_grid).shape
    output_size = (input_size[0] - 2, input_size[1] - 2)

    # Extract subgrid
    subgrid = get_center_subgrid(np.array(input_grid), output_size)

    # Find non-white color (This is used for the condition, but the transformation is applied to all cells)
    non_white_color = find_non_white_color(subgrid)


    # initialize output grid
    output_grid = np.zeros(output_size, dtype=int)

    # Apply color transformation to every cell in subgrid
    for i in range(output_size[0]):
        for j in range(output_size[1]):
            if subgrid[i, j] == 0:
                output_grid[i, j] = 0
            elif subgrid[i,j] == 2:
                output_grid[i,j] = 5
            elif subgrid[i,j] == 1:
                output_grid[i,j] = 2
            elif subgrid[i,j] == 3:
                output_grid[i,j] = 4
            elif subgrid[i,j] == 5:
                output_grid[i,j] = 6
            # else we should not need this branch, based on instructions

    return output_grid