```python
"""
Processes a grid based on color-specific rules related to neighbor interactions and a global boundary defined by maroon pixels.

1.  Determines the rightmost column index (`max_col_maroon`) occupied by any maroon (9) pixel in the input grid. If no maroon pixels exist, this boundary is the right edge of the grid.
2.  For each red (2) pixel in the input grid, if its immediate left neighbor is orange (7), the corresponding left neighbor in the output grid is changed to red (2).
3.  For each row in the output grid, gray (5) pixels are iteratively extended to the right into adjacent orange (7) pixels, but only up to the `max_col_maroon` column index.
4.  Any green (3) pixel in the output grid located in a column strictly to the right of `max_col_maroon` is changed to orange (7).
5.  Other colors (blue-1, azure-8, maroon-9, orange-7 unless modified) remain unchanged.
"""

import numpy as np

def find_max_maroon_col(grid):
    """Finds the maximum column index containing a maroon (9) pixel."""
    height, width = grid.shape
    max_col = -1
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 9:
                max_col = max(max_col, c)
    # If no maroon found, the boundary is the right edge
    if max_col == -1:
        max_col = width - 1
    return max_col

def transform(input_grid):
    """
    Applies color-specific transformation rules to the input grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    # 1. Determine the maximum column index for maroon pixels
    max_col_maroon = find_max_maroon_col(input_np)

    # 2. Process Red Pixels based on input grid state
    # Iterate through each cell (r, c) of the *input* grid.
    for r in range(height):
        for c in range(width):
            # Check if the input cell is red (2)
            if input_np[r, c] == 2:
                # Check if its left neighbor exists (c > 0)
                # and is orange (7) in the *input* grid
                if c > 0 and input_np[r, c - 1] == 7:
                    # Set the corresponding left neighbor in the *output* grid to red (2)
                    output_grid[r, c - 1] = 2

    # 3. Process Gray Pixels - iterative extension within rows on the output grid
    # Iterate through each row r of the output grid.
    for r in range(height):
        # Use a flag to track if any changes were made in a pass
        changed_in_pass = True
        # Repeat scanning the row as long as changes are being made
        while changed_in_pass:
            changed_in_pass = False
            # Scan from left to right (c from 0 to width - 2)
            for c in range(width - 1):
                # Check if the current cell is gray (5)
                # AND the cell to its right is orange (7)
                # AND the right cell's column index is within the maroon boundary
                if (output_grid[r, c] == 5 and
                        output_grid[r, c + 1] == 7 and
                        c + 1 <= max_col_maroon):
                    # Change the right orange cell to gray (5)
                    output_grid[r, c + 1] = 5
                    # Mark that a change was made in this pass
                    changed_in_pass = True

    # 4. Process Green Pixels based on the output grid state
    # Iterate through each cell (r, c) of the output grid.
    for r in range(height):
        for c in range(width):
            # Check if the cell is green (3)
            # AND its column index c is greater than max_col_maroon
            if output_grid[r, c] == 3 and c > max_col_maroon:
                # Change the cell to orange (7)
                output_grid[r, c] = 7

    # Convert numpy array back to list of lists for the final output format
    return output_grid.tolist()
```