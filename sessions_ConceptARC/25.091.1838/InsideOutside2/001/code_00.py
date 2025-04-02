import numpy as np
from typing import List, Tuple

"""
Transformation Rule:

1. Identify the locations of red (2) and yellow (4) pixels in the input grid.
2. Determine which color is the majority color (red, with 2 instances) and which is the minority color (yellow, with 1 instance).
3. Check if the pixels of the majority color (red) are aligned either horizontally (all in the same row) or vertically (all in the same column).
4. If the majority color pixels (red) are aligned: Keep the majority color pixels (red) and change the minority color pixel (yellow) to white (0).
5. If the majority color pixels (red) are not aligned: Keep the minority color pixel (yellow) and change the majority color pixels (red) to white (0).
6. Return the modified grid.
"""

def find_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds the coordinates of all pixels of a given color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def check_alignment(coords: List[Tuple[int, int]]) -> bool:
    """Checks if all coordinates share the same row or the same column."""
    if not coords or len(coords) <= 1:
        return True  # Single pixel or no pixels are considered aligned

    rows = [r for r, c in coords]
    cols = [c for r, c in coords]

    # Check if all rows are the same
    if len(set(rows)) == 1:
        return True
    # Check if all columns are the same
    if len(set(cols)) == 1:
        return True

    return False

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    Keeps either the red pixels or the yellow pixel based on the alignment
    of the red pixels.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Define colors
    red = 2
    yellow = 4
    white = 0

    # Find pixel coordinates for each color
    red_coords = find_pixels(input_grid, red)
    yellow_coords = find_pixels(input_grid, yellow)

    # Assuming red is always the majority (2 pixels) and yellow the minority (1 pixel)
    # based on the examples.
    majority_color = red
    minority_color = yellow
    majority_coords = red_coords
    minority_coords = yellow_coords

    # Check if the majority color pixels (red) are aligned
    is_aligned = check_alignment(majority_coords)

    # Apply the transformation based on alignment
    if is_aligned:
        # Keep majority (red), remove minority (yellow)
        for r, c in minority_coords:
            output_grid[r, c] = white
    else:
        # Keep minority (yellow), remove majority (red)
        for r, c in majority_coords:
            output_grid[r, c] = white

    return output_grid
