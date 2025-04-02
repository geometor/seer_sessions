import numpy as np
from typing import List, Tuple

"""
The transformation identifies the single non-background color (C) and the locations of all pixels with this color in the input grid. 
It then determines a fill rule based on the coordinates of the "first" pixel (minimum row, then minimum column).

Rule Determination:
1. Find the non-background color C and all its pixel coordinates (r, c).
2. Identify the first pixel (r_first, c_first) - the one with the minimum row, and among those, the minimum column.
3. If c_first <= r_first, apply Fill Rule A.
4. If c_first > r_first, apply Fill Rule B.

Fill Rule A:
- For each pixel of color C at (r, c) in the input, fill the corresponding row 'r' in the output grid from column 0 up to column 'c' (inclusive) with color C.

Fill Rule B:
- Find the maximum row index (max_r) containing a pixel of color C.
- For each pixel of color C at (r, c) in the input, fill the corresponding row 'r' in the output grid from column 'c' up to the last column (inclusive) with color C.
- Fill all rows in the output grid from row 'max_r + 1' to the bottom completely with color C.

If no non-background color is found, the input grid is returned unchanged.
The background color is assumed to be 0 (white).
"""

def find_color_pixels(grid: np.ndarray) -> Tuple[int, List[Tuple[int, int]]]:
    """Finds the non-background color and coordinates of all its pixels."""
    color = -1
    coords = []
    non_background_pixels = np.where(grid != 0)
    
    if len(non_background_pixels[0]) == 0:
        return -1, [] # No non-background color found

    # Get the color from the first non-background pixel found
    first_r, first_c = non_background_pixels[0][0], non_background_pixels[1][0]
    color = grid[first_r, first_c]
    
    # Find all coordinates of this specific color
    color_pixels = np.where(grid == color)
    coords = list(zip(color_pixels[0], color_pixels[1]))
    
    return int(color), coords

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule based on the position of the first non-background pixel.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # Find the non-background color and its pixel coordinates
    color, coords = find_color_pixels(input_np)

    # If no non-background color or no pixels of that color found, return original
    if color == -1 or not coords:
        return input_grid

    # Sort coordinates to easily find the first pixel (min row, then min col)
    coords.sort()
    r_first, c_first = coords[0]

    # Determine which fill rule to apply
    if c_first <= r_first:
        # Apply Fill Rule A: Fill left in the row
        for r, c in coords:
            output_grid[r, 0:c+1] = color
    else:
        # Apply Fill Rule B: Fill right in the row and fill rows below
        max_r = -1
        for r, c in coords:
            output_grid[r, c:width] = color
            if r > max_r:
                max_r = r
        
        # Fill rows below the max row containing the color
        if max_r < height - 1:
            output_grid[max_r+1:height, :] = color

    # Convert back to list of lists before returning
    return output_grid.tolist()