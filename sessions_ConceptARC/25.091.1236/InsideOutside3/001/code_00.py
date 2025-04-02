import numpy as np
from typing import List, Tuple

"""
Preserve either the single yellow pixel or all red pixels based on their 
spatial relationship. 

If the yellow pixel does not share a row or column with any red pixel, 
keep only the yellow pixel.

If the yellow pixel shares a row or column with red pixels, check the 
relative positions of these sharing red pixels. If ALL sharing red pixels 
are strictly to the East (same row, greater column index) of the yellow pixel, 
keep only the yellow pixel.

Otherwise (if any sharing red pixel is North, South, West, or if there are 
sharing pixels in multiple directions relative to the yellow one), keep all 
original red pixels and remove the yellow pixel.
"""

def find_pixels_by_color(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all pixels of a specific color in the grid."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on the relationship between the yellow 
    and red pixels.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid)
    height, width = grid.shape
    
    # Initialize output_grid with background color (white, 0)
    output_grid = np.zeros_like(grid)

    # Find the yellow pixel location
    yellow_pixels = find_pixels_by_color(grid, 4)
    if not yellow_pixels:
        # Should not happen based on problem description, but handle defensively
        return output_grid 
    y_row, y_col = yellow_pixels[0] # Expecting exactly one

    # Find all red pixel locations
    red_pixel_locations = find_pixels_by_color(grid, 2)

    # Find red pixels sharing the same row or column as the yellow pixel
    sharing_red_pixels = []
    for r_row, r_col in red_pixel_locations:
        if r_row == y_row or r_col == y_col:
            sharing_red_pixels.append((r_row, r_col))

    # Decision logic
    keep_yellow = False
    if not sharing_red_pixels:
        # Case 1: Yellow pixel is isolated (no red in same row/col)
        keep_yellow = True
    else:
        # Case 2: Yellow shares row/col with red(s). Check directionality.
        all_east = True
        for sr_row, sr_col in sharing_red_pixels:
            # Check if the sharing pixel is NOT strictly East
            if not (sr_row == y_row and sr_col > y_col):
                all_east = False
                break 
        
        if all_east:
            # Case 2a: All sharing red pixels are strictly East
            keep_yellow = True
        # else: Case 2b: At least one sharing red is N, S, W, or not strictly East -> keep reds (default if keep_yellow remains False)

    # Populate the output grid based on the decision
    if keep_yellow:
        # Keep only the yellow pixel
        output_grid[y_row, y_col] = 4
    else:
        # Keep all original red pixels
        for r_row, r_col in red_pixel_locations:
            output_grid[r_row, r_col] = 2

    return output_grid.tolist() # Return as list of lists as per ARC standard