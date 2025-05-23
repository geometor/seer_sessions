"""
1.  **Identify Broken Gray Line:** Locate the broken vertical column of gray pixels. It's not necessarily a continuous line, but a series of gray pixels in the same column.
2.  **Color Gray Line Blue:** Change the color of all gray pixels in that identified column to blue. The "broken" nature is preserved.
3. **Identify Last Column White Pixels**: Find the white pixels in the last three rows of the last column.
4.  **Color White Pixels Red:** Change the color of these specific white pixels (last three rows, last column) to red.
5. **Preserve all other pixels**
"""

import numpy as np

def find_broken_vertical_line(grid, color):
    """Finds the column index and row indices of a broken vertical line of a given color."""
    rows, cols = grid.shape
    for j in range(cols):
        gray_pixels = []
        for i in range(rows):
            if grid[i, j] == color:
                gray_pixels.append(i)
        if len(gray_pixels) > 1:  # Consider it a line if there are at least two gray pixels
            return j, gray_pixels
    return None, []

def transform(input_grid):
    # Initialize output grid with a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the broken vertical gray line
    col_index, row_indices = find_broken_vertical_line(input_grid, 5)
    if col_index is not None:
        # Change the color of the gray pixels to blue
        for i in row_indices:
            output_grid[i, col_index] = 1

    # Change white cells in the last three rows of the last column to red
    for i in range(max(0, rows - 3), rows):  # Ensure we don't go out of bounds
        if cols > 0 and output_grid[i, cols - 1] == 0: # make sure there is a last col
            output_grid[i, cols - 1] = 2

    return output_grid