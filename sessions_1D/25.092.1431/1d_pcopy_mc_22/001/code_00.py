"""
Identifies single non-white pixels in the input grid and expands them horizontally into a 1x3 line of the same color in the output grid. The original single pixel becomes the center of the new line. Existing shapes (like 1x3 lines) are preserved.

1. Initialize the output grid as a copy of the input grid.
2. Iterate through each cell (pixel) of the input grid.
3. If a cell contains a non-white pixel, check if it represents a single-pixel object by examining its 8 neighbors. If all neighbors are either outside the grid boundary or are white (0), then the cell is a single-pixel object.
4. If a cell is identified as a single-pixel object with color C at position (row, col):
    - Change the color of the cell at (row, col-1) to C in the output grid (if col-1 is within grid bounds).
    - Change the color of the cell at (row, col) to C in the output grid.
    - Change the color of the cell at (row, col+1) to C in the output grid (if col+1 is within grid bounds).
5. If a non-white cell is part of a larger object, do nothing during this iteration (it's already copied).
6. Return the modified output grid.
"""

import numpy as np

def _is_single_pixel(grid, r, c):
    """
    Checks if the pixel at (r, c) is non-white and has no non-white neighbors.
    """
    rows, cols = grid.shape
    # The pixel itself must be non-white
    if grid[r, c] == 0:
        return False

    # Check all 8 neighbors
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center cell itself
            if dr == 0 and dc == 0:
                continue

            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # If a neighbor is within bounds AND is non-white,
                # then the pixel at (r, c) is not isolated.
                if grid[nr, nc] != 0:
                    return False
    # If the loop completes without finding any non-white neighbors, it's a single pixel
    return True

def transform(input_grid):
    """
    Transforms the input grid according to the rule: expand single non-white pixels
    horizontally into 1x3 lines.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape

    # Iterate through each cell of the original input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell in the *original* input represents a single-pixel object
            if _is_single_pixel(input_np, r, c):
                # Get the color of the single pixel
                color = input_np[r, c]

                # Modify the output grid to create the 1x3 line
                # Center pixel (already set by copy, but can be explicit)
                output_grid[r, c] = color

                # Left pixel (check bounds)
                if c - 1 >= 0:
                    output_grid[r, c - 1] = color

                # Right pixel (check bounds)
                if c + 1 < cols:
                    output_grid[r, c + 1] = color

    # Convert the result back to a list of lists before returning
    return output_grid.tolist()