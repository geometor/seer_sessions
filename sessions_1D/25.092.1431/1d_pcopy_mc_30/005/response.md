```python
import numpy as np
from typing import List, Tuple

"""
Transforms a 4x8 grid based on the following rules:

1. Initialize an output grid as a copy of the input grid.
2. Identify "source" pixels in the input grid. A pixel at (r, c) is a source if:
    a. It is not white (color value > 0).
    b. Its horizontal neighbors (left and right, with column wrap-around) have colors different from the source pixel's color.
3. For each identified source pixel at input position (r, c) with color C:
    a. Calculate the target coordinates for a 3-pixel horizontal line:
        i. Center pixel coordinates: (r, c).
        ii. Left pixel coordinates: 
            - Column: (c - 1 + 8) % 8 (column wrap-around).
            - Row: (r - 1 + 4) % 4 if the source column c is 0 (left edge), otherwise r.
        iii. Right pixel coordinates:
            - Column: (c + 1 + 8) % 8 (column wrap-around).
            - Row: (r + 1 + 4) % 4 if the source column c is 7 (right edge), otherwise r.
    b. Update the *output* grid by setting the color of the pixels at the calculated left, center, and right target coordinates to C.
4. Return the final modified output grid. Existing 3-pixel horizontal lines from the input are preserved unless overwritten by an expansion.
"""

def is_source_pixel(grid: np.ndarray, r: int, c: int) -> bool:
    """
    Checks if a pixel at (r, c) in the input grid is a source for expansion.
    A pixel is a source if it's non-white and its horizontal neighbors
    (with column wrap-around) are not the same color as the pixel.
    """
    rows, cols = grid.shape
    color = grid[r, c]

    # Must be non-white
    if color == 0:
        return False

    # Check horizontal neighbors using modulo for column wrap-around
    left_c = (c - 1 + cols) % cols
    right_c = (c + 1 + cols) % cols
    left_neighbor_color = grid[r, left_c]
    right_neighbor_color = grid[r, right_c]

    # A pixel is a source if its color differs from both its left and right horizontal neighbors
    return left_neighbor_color != color and right_neighbor_color != color

def calculate_target_coords(r: int, c: int, rows: int, cols: int) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
    """
    Calculates the target coordinates (left, center, right) for expansion,
    applying specific row and column wrap-around rules based on the source pixel's position.

    Args:
        r: Row index of the source pixel.
        c: Column index of the source pixel.
        rows: Total number of rows in the grid.
        cols: Total number of columns in the grid.

    Returns:
        A tuple containing three coordinate tuples: ((left_r, left_c), (center_r, center_c), (right_r, right_c)).
    """
    # Calculate column indices with standard horizontal wrap-around
    left_c_target = (c - 1 + cols) % cols
    center_c_target = c
    right_c_target = (c + 1 + cols) % cols

    # Calculate row indices, starting with the source row
    left_r_target = r
    center_r_target = r
    right_r_target = r

    # Apply special row wrap adjustment for edge columns
    if c == 0: # Source is in the first column (left edge)
        # The pixel wrapping to the last column uses the row above (with row wrap)
        left_r_target = (r - 1 + rows) % rows
    if c == cols - 1: # Source is in the last column (right edge)
        # The pixel wrapping to the first column uses the row below (with row wrap)
        right_r_target = (r + 1 + rows) % rows

    return ((left_r_target, left_c_target),
            (center_r_target, center_c_target),
            (right_r_target, right_c_target))

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the expansion transformation to the input grid.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Initialize output grid as a copy of the input grid
    output_np = input_np.copy()

    # Iterate through each cell of the *input* grid to find source pixels
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell in the input grid is a source for expansion
            if is_source_pixel(input_np, r, c):
                # Get the color of the source pixel
                color = input_np[r, c]

                # Calculate the target coordinates for the 3-pixel horizontal line
                (left_coord, center_coord, right_coord) = calculate_target_coords(r, c, rows, cols)

                # Update the *output* grid with the expanded line using the source color
                output_np[left_coord] = color
                # Center coordinate update overwrites the original source pixel location in the output
                output_np[center_coord] = color
                output_np[right_coord] = color

    # Convert the final numpy array back to a list of lists
    return output_np.tolist()
```