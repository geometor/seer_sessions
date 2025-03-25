"""
Identify a horizontal line of a constant color. Modify this line, replacing the color of pixels *not* part of
vertical lines of the same color. The replacement color comes from the row directly above, unless the horizontal line
is the topmost row, in which case it comes from the row below.
"""

import numpy as np

def find_horizontal_line(grid):
    """Finds a row with all pixels having the same non-zero color."""
    for i, row in enumerate(grid):
        first_color = row[0]
        if first_color != 0 and np.all(row == first_color):
            return i, first_color
    return None, None

def find_vertical_lines(grid, color):
    """Finds columns with repeating colors of the specified color spanning at least three rows."""
    vertical_lines = []
    rows, cols = grid.shape
    for j in range(cols):
        for i in range(rows - 2):
            if grid[i, j] == color and grid[i+1, j] == color and grid[i+2, j] == color:
                vertical_lines.append(j)
                break  # Move to the next column after finding a matching vertical line
    return vertical_lines

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    rows, cols = grid.shape
    output_grid = grid.copy()

    # Find the special horizontal line
    horizontal_line_row, horizontal_line_color = find_horizontal_line(grid)

    if horizontal_line_row is None:
        return output_grid.tolist()  # Return unchanged if no horizontal line is found

    # Find the persistent vertical lines OF THE SAME COLOR
    vertical_lines = find_vertical_lines(grid, horizontal_line_color)

    # Modify the special row
    for j in range(cols):
        # Check if the current column is part of a vertical line of the SAME color
        is_vertical_line = j in vertical_lines

        # Replace the color if not part of a matching vertical line
        if not is_vertical_line:
            if horizontal_line_row == 0:
                output_grid[horizontal_line_row, j] = grid[horizontal_line_row + 1, j]
            else:
                output_grid[horizontal_line_row, j] = grid[horizontal_line_row - 1, j]

    return output_grid.tolist()