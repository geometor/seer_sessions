"""
1.  **Find Horizontal Line:** Scan the input grid to identify a horizontal line (a row) where all pixels have the same non-zero color. If no such line is found, the output grid is identical to the input grid.
2.  **Find Vertical Lines:** Identify any vertical lines - columns that have at least three consecutive pixels of the *same* non-zero color. Note which columns these are.
3.  **Modify Horizontal Line:** For each pixel in the identified horizontal line:
    *   If the pixel's column is part of a vertical line, keep its original color.
    *   If the pixel's column is *not* part of a vertical line:
        * If the horizontal line is the very top row of the grid, change pixel to the color directly *below* it
        * Otherwise, change the pixel to the color directly *above* it.
4. Return modified grid.
"""

import numpy as np

def find_horizontal_line(grid):
    """Finds a row with all pixels having the same non-zero color."""
    for i, row in enumerate(grid):
        first_color = row[0]
        if first_color != 0 and np.all(row == first_color):
            return i, first_color
    return None, None

def find_vertical_lines(grid):
    """Finds columns with at least three consecutive pixels of the same non-zero color."""
    vertical_lines = []
    grid_array = np.array(grid)
    rows, cols = grid_array.shape
    for j in range(cols):
        for i in range(rows - 2):
            if grid_array[i, j] != 0 and grid_array[i, j] == grid_array[i+1, j] and grid_array[i, j] == grid_array[i+2, j]:
                vertical_lines.append(j)
                break  # Move to the next column
    return vertical_lines

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    grid = np.array(input_grid)
    rows, cols = grid.shape
    output_grid = grid.copy()

    # 1. Find Horizontal Line
    horizontal_line_row, horizontal_line_color = find_horizontal_line(grid)

    if horizontal_line_row is None:
        return output_grid.tolist()  # Return unchanged if no horizontal line

    # 2. Find Vertical Lines
    vertical_lines = find_vertical_lines(grid)

    # 3. Modify Horizontal Line
    for j in range(cols):
        if j in vertical_lines:
            # Keep original color
            continue
        else:
            # Change color based on row position
            if horizontal_line_row == 0:
                output_grid[horizontal_line_row, j] = grid[horizontal_line_row + 1, j]
            else:
                output_grid[horizontal_line_row, j] = grid[horizontal_line_row - 1, j]

    return output_grid.tolist()