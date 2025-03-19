"""
1.  **Identify the Center:** Find the center pixel of the input grid.
2.  **Propagate Center Color (Conditionally):**
    *   **Row Propagation:** Starting from the center pixel and moving outwards in both directions along the row:
        *   If the current pixel's color is the *same* as the center pixel's color, change the current pixel's color to the center pixel's color.
        *   If the current pixel's color is *different* from the center pixel's color, *stop* propagation in that direction.
    *   **Column Propagation:** Starting from the center pixel and moving outwards in both directions along the column:
        *   If the current pixel's color is the *same* as the center pixel's color, change the current pixel's color to the center pixel's color.
        *   If the current pixel's color is *different* from the center pixel's color, *stop* propagation in that direction.
3.  **Unchanged Pixels:** Pixels not affected by the propagation remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # find the center coordinates
    center_row = rows // 2
    center_col = cols // 2

    # get center pixel color
    center_color = input_grid[center_row, center_col]

    # Row propagation (left)
    for j in range(center_col - 1, -1, -1):
        if input_grid[center_row, j] == center_color:
            output_grid[center_row, j] = center_color
        else:
            break

    # Row propagation (right)
    for j in range(center_col + 1, cols):
        if input_grid[center_row, j] == center_color:
            output_grid[center_row, j] = center_color
        else:
            break

    # Column propagation (up)
    for i in range(center_row - 1, -1, -1):
        if input_grid[i, center_col] == center_color:
            output_grid[i, center_col] = center_color
        else:
            break

    # Column propagation (down)
    for i in range(center_row + 1, rows):
        if input_grid[i, center_col] == center_color:
            output_grid[i, center_col] = center_color
        else:
            break

    return output_grid