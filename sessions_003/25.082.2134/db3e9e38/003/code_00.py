"""
The transformation rule involves locating a vertical line of '7's in the input grid and using its position to generate an alternating pattern of '7's and '8's in the output grid. The pattern expands outwards from the initial line location, creating nested 'L' shapes, while maintaining the '0' background. The L shapes are formed with the horizontal part going to the left and right and the vertical part going up.
"""

import numpy as np

def find_vertical_line(grid, color=7):
    """Finds the coordinates of a vertical line of a specified color."""
    rows, cols = grid.shape
    for j in range(cols):
        for i in range(rows):
            if grid[i, j] == color:
                # Check if it's a vertical line
                line_start = i
                line_end = i
                while line_end < rows and grid[line_end, j] == color:
                    line_end += 1
                if line_end - line_start > 1:  # Ensure it's a line
                    return [(r, j) for r in range(line_start, line_end)]
    return []

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)  # Convert to NumPy array
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Locate the Vertical Line
    line_coords = find_vertical_line(input_grid)

    if not line_coords:
        return output_grid.tolist() # Return blank grid if no line is found

    line_col = line_coords[0][1]
    line_row_start = line_coords[0][0]

    # 2 & 3. Establish the Pattern Seed and Expand
    # Initial vertical line
    for i, (row, _) in enumerate(line_coords):
      output_grid[row, line_col] = 7

    offset = 0
    while True:
        offset += 1
        row_index = line_row_start - offset  # Move one row up
        col_start = line_col - offset        # Move one col left
        col_end = line_col + offset          # Move one col right

        if row_index < 0 or col_start < 0 or col_end >= cols:
            break  # stop if out of top/left/right bounds

        # horizontal (top of L)
        for c in range(col_start, col_end + 1):
          output_grid[row_index, c] = 7 if (c - col_start) % 2 == 0 else 8

        # vertical section of L (going upwards)
        for r in range(row_index + 1, line_row_start +1):

            output_grid[r, col_start] = 7 if (r-row_index)%2!=0 else 8

    # 4. Maintain Background (already handled by initializing output_grid to 0s)

    return output_grid.tolist()