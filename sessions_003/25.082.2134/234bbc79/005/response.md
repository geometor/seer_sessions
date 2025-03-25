```python
"""
1.  **Initialization:** Create a copy of the input grid as the output grid.

2.  **Gray Pixel Processing:** Iterate through each cell of the *input* grid. Only process cells that are gray (value 5) in the *input* grid.

3.  **Color Source Determination (for gray pixels):**
    *   **Left Scan:** Examine the cells in the same row, to the *left* of the current gray pixel. Stop at the first cell that is *not* gray (5) and *not* zero (0).  If such a cell is found, remember its color.
    *   **Right Scan (if no color found on the left):** If no suitable color was found to the left, examine the cells to the *right* of the current gray pixel, using the same criteria (non-gray, non-zero). Remember the color if found.
    * **Zero Assignment (if no color found)**: If, after scanning left and right, no source color is determined, set output to zero (0)

4.  **Color Propagation:**
    * If a source color was found (either left or right):
        * Change the current (originally gray) pixel in the output grid to the source color.
        * **Contiguous Gray Propagation:** Continue propagating this source color *in the same direction the color was found* along the current row in the output grid. Only overwrite pixels that were originally gray (5) in the *input* grid. Stop propagation when a non-gray pixel or the edge of the grid is reached.

5.  **Non-Gray Pixel Preservation:** If a cell in the input grid is *not* gray (5), its value is directly copied to the output grid without change.

6.  **Row Removal:** After processing all pixels, iterate through the rows of the *output* grid.  If *any* row contains only zeros (0), remove that entire row from the output grid. The final output grid's dimensions may be smaller than the input grid's dimensions.
"""

import numpy as np

def get_source_color(input_grid, row, col):
    """Finds the source color for a gray pixel."""
    rows, cols = input_grid.shape
    left_color = 0
    # Left Scan
    for i in range(col - 1, -1, -1):
        if input_grid[row, i] != 5 and input_grid[row, i] != 0:
            left_color = input_grid[row, i]
            break
    if left_color != 0:
        return left_color, -1  # -1 indicates left direction

    # Right Scan
    right_color = 0
    for i in range(col + 1, cols):
        if input_grid[row, i] != 5 and input_grid[row, i] != 0:
            right_color = input_grid[row, i]
            break
    if right_color != 0:
        return right_color, 1  # 1 indicates right direction

    return 0, 0 # no color found

def propagate(input_grid, output_grid, row, col, color, direction):
    """Propagates the color in the specified direction."""
    rows, cols = input_grid.shape
    current_col = col

    while 0 <= current_col < cols:
        if input_grid[row, current_col] == 5:
            output_grid[row, current_col] = color
            current_col += direction
        else:
            break  # Stop propagation


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # Gray Pixel Processing
            if input_grid[r, c] == 5:
                # Color Source Determination
                source_color, direction = get_source_color(input_grid, r, c)

                # Color Propagation / Zero Assignment
                if source_color != 0:
                    propagate(input_grid, output_grid, r, c, source_color, direction)
                else:
                    output_grid[r,c] = 0

            # Non-Gray Pixel Preservation (already handled by copying input_grid initially)

    # Row Removal
    rows_to_keep = []
    for r in range(output_grid.shape[0]):
        if np.any(output_grid[r] != 0):  # Check if the row has any non-zero elements
            rows_to_keep.append(r)

    output_grid = output_grid[rows_to_keep]

    return output_grid
```