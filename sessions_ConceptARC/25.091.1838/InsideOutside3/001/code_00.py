import numpy as np
from typing import List, Tuple

"""
Transformation rule:
1. Find the single yellow pixel (4) and all red pixels (2).
2. Determine the coordinate parity (odd=1, even=0) of the yellow pixel (y_r % 2, y_c % 2).
3. If the yellow pixel's parity is NOT (odd, odd) (i.e., not (1, 1)), remove the yellow pixel (set to white 0), keeping all red pixels.
4. If the yellow pixel's parity IS (odd, odd) (i.e., (1, 1)):
    a. Check the parity of all red pixels.
    b. If ANY red pixel also has (odd, odd) parity, remove the yellow pixel (set to white 0), keeping all red pixels.
    c. If NO red pixel has (odd, odd) parity, keep the yellow pixel and remove ALL red pixels (set them to white 0).
"""

def find_pixels_by_color(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def get_pixel_parity(row: int, col: int) -> Tuple[int, int]:
    """Calculates the parity (0 for even, 1 for odd) of row and column."""
    return (row % 2, col % 2)

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule based on yellow and red pixel coordinate parities.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    output_grid = grid_np.copy()

    # Find the yellow pixel (color 4)
    yellow_pixels = find_pixels_by_color(grid_np, 4)
    if not yellow_pixels:
        # Should not happen based on task description, but handle defensively
        return output_grid.tolist() 
    
    y_r, y_c = yellow_pixels[0] # Assuming exactly one yellow pixel

    # Find all red pixels (color 2)
    red_pixels = find_pixels_by_color(grid_np, 2)

    # Calculate the parity of the yellow pixel
    y_parity = get_pixel_parity(y_r, y_c)

    # Apply the core logic based on yellow pixel parity
    if y_parity != (1, 1):
        # Case 1: Yellow pixel is NOT at (odd, odd) coordinate. Remove yellow.
        output_grid[y_r, y_c] = 0
    else:
        # Case 2: Yellow pixel IS at (odd, odd) coordinate.
        found_odd_odd_red = False
        for r_r, r_c in red_pixels:
            r_parity = get_pixel_parity(r_r, r_c)
            if r_parity == (1, 1):
                # Subcase 2a: Found a red pixel also at (odd, odd).
                found_odd_odd_red = True
                break # No need to check further red pixels

        if found_odd_odd_red:
            # Subcase 2a action: Remove yellow pixel.
            output_grid[y_r, y_c] = 0
        else:
            # Subcase 2b: No red pixel found at (odd, odd). Remove all red pixels.
            for r_r, r_c in red_pixels:
                output_grid[r_r, r_c] = 0
            # Yellow pixel remains in this subcase

    # Convert the result back to a list of lists
    return output_grid.tolist()
