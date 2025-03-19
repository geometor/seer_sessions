"""
1. Identify Black Rectangle: Find a rectangle within the input grid where all the pixels on the border of the rectangle are black (0). It does not need to be the *largest* such rectangle, nor does the inside need to be solid black.
2. Crop: Crop the input grid to the bounding box of this black-bordered rectangle.
3. Reflect: Reflect the cropped grid along the horizontal axis (across the x-axis, i.e., flip vertically). The output grid is the reflected, cropped region.
"""

import numpy as np

def find_black_bordered_rectangle(grid: np.ndarray) -> tuple[int, int, int, int] | None:
    """
    Finds a rectangle within the grid where all border pixels are black (0).
    Returns (min_row, min_col, max_row, max_col) or None if no such rectangle is found.
    """
    rows, cols = grid.shape
    for r1 in range(rows):
        for c1 in range(cols):
            for r2 in range(r1, rows):
                for c2 in range(c1, cols):
                    # Check if all border pixels are black
                    is_bordered = True
                    # Top border
                    for c in range(c1, c2 + 1):
                        if grid[r1, c] != 0:
                            is_bordered = False
                            break
                    if not is_bordered:
                        continue
                    # Bottom border
                    for c in range(c1, c2 + 1):
                        if grid[r2, c] != 0:
                            is_bordered = False
                            break
                    if not is_bordered:
                        continue
                    # Left border (excluding corners already checked)
                    for r in range(r1 + 1, r2):
                        if grid[r, c1] != 0:
                            is_bordered = False
                            break
                    if not is_bordered:
                        continue
                    # Right border (excluding corners already checked)
                    for r in range(r1 + 1, r2):
                        if grid[r, c2] != 0:
                            is_bordered = False
                            break
                    if is_bordered:
                        return (r1, c1, r2, c2)
    return None

def transform(input_grid):
    # Find the black-bordered rectangle
    rectangle = find_black_bordered_rectangle(input_grid)

    if rectangle is None:
        return np.zeros((0, 0), dtype=int)  # Return an empty array if no such rectangle is found

    min_row, min_col, max_row, max_col = rectangle

    # Crop the input grid to the bounding box of the rectangle
    cropped_grid = input_grid[min_row:max_row+1, min_col:max_col+1]

    # Reflect the cropped grid vertically (across the x-axis)
    output_grid = np.flipud(cropped_grid)

    return output_grid