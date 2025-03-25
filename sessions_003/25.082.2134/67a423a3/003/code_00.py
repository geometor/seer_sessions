"""
1.  **Find Vertical Line:** Identify a vertical line, defined as a column where all cells have the same non-zero color. Note the color and column index. If no such line exists, return the original grid.

2.  **Find Horizontal Line:** Identify a horizontal line. A horizontal line exists on a row that intersects the vertical line, is not the same color as the vertical line, and has at least one other pixel that is not color 0.

3.  **Locate Intersection:** The intersection is the point where the vertical and horizontal lines meet (share the same row and column indices).

4.  **Create Frame (Conditional):** If a horizontal line exists, create a yellow (color 4) frame around the intersection *only* on the cells adjacent to the vertical line. This frame extends:
    *   One row above the intersection.
    *   On the intersection row itself.
    *   One row below the intersection.

5.  **Preserve Unchanged Pixels:** Pixels not part of the vertical line or the frame (if it exists) should remain unchanged. Specifically, the vertical line's color should be preserved.
"""

import numpy as np

def find_vertical_line(grid):
    """Finds the vertical line in the grid."""
    rows, cols = grid.shape
    for j in range(cols):
        first_color = grid[0, j]
        if first_color == 0:
            continue
        is_vertical_line = True
        for i in range(1, rows):
            if grid[i, j] != first_color:
                is_vertical_line = False
                break
        if is_vertical_line:
            return j, first_color
    return None, None

def find_horizontal_line(grid, vertical_line_col, vertical_line_color):
    """Finds the horizontal line intersecting the vertical line."""
    rows, cols = grid.shape
    for i in range(rows):
        if grid[i, vertical_line_col] == vertical_line_color:
            for j in range(cols):
                if j != vertical_line_col and grid[i,j] != 0 and grid[i,j] != vertical_line_color:
                    # Check for a horizontal line (at least one non-zero, non-vertical-line color)
                    is_horizontal = False
                    for k in range(cols):
                        if k != vertical_line_col and grid[i,k] != 0 and grid[i,k] != vertical_line_color:
                            is_horizontal = True
                            break
                    if is_horizontal:

                        return i, grid[i,j] #return any color other than 0 and vertical line
    return None, None

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    rows, cols = grid.shape
    output_grid = grid.copy()

    # Find the vertical line
    vertical_line_col, vertical_line_color = find_vertical_line(grid)

    if vertical_line_col is None:
        return output_grid.tolist()  # No vertical line, return original

    # Find horizontal line
    horizontal_line_row, _ = find_horizontal_line(grid, vertical_line_col, vertical_line_color)

    if horizontal_line_row is None:
        return output_grid.tolist() #No horizontal line found, return original

    # Locate intersection (already have row and col from above steps)
    intersection_row = horizontal_line_row
    intersection_col = vertical_line_col

    # Create frame (only if a horizontal line was found)

    # Row above
    row_above = max(0, intersection_row - 1)
    if row_above != intersection_row:
        if intersection_col > 0:
            output_grid[row_above, intersection_col - 1] = 4  # Left
        if intersection_col < cols - 1:
            output_grid[row_above, intersection_col + 1] = 4  # Right

    # Intersection row
    if intersection_col > 0:
        output_grid[intersection_row, intersection_col - 1] = 4  # Left
    if intersection_col < cols - 1:
        output_grid[intersection_row, intersection_col + 1] = 4  # Right

    # Row below
    row_below = min(rows - 1, intersection_row + 1)
    if row_below != intersection_row:
        if intersection_col > 0:
            output_grid[row_below, intersection_col - 1] = 4  # Left
        if intersection_col < cols - 1:
            output_grid[row_below, intersection_col + 1] = 4  # Right

    return output_grid.tolist()