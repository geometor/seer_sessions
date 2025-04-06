"""
Transforms a 4x4 input grid into a 4x4 output grid. 
The transformation rule operates on 2x2 quadrants. 
For each 2x2 quadrant in the input grid:
- If the digit '2' is present anywhere within that quadrant, the corresponding 2x2 quadrant in the output grid is filled entirely with '2'.
- If the digit '2' is not present within that input quadrant, the corresponding 2x2 quadrant in the output grid is filled entirely with '6'.
"""

import numpy as np

def _check_quadrant_for_value(grid: np.ndarray, row_start: int, col_start: int, value: int) -> bool:
    """Checks if a specific value exists within a 2x2 quadrant of the grid."""
    quadrant = grid[row_start:row_start+2, col_start:col_start+2]
    return value in quadrant

def _fill_quadrant(grid: np.ndarray, row_start: int, col_start: int, fill_value: int):
    """Fills a 2x2 quadrant of the grid with a specific value."""
    grid[row_start:row_start+2, col_start:col_start+2] = fill_value

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the quadrant-based transformation rule to the input grid.
    Checks each 2x2 quadrant for the presence of '2' and fills the 
    corresponding output quadrant with '2' if found, otherwise with '6'.
    """
    # Convert input list of lists to a NumPy array for easier slicing
    input_array = np.array(input_grid)
    
    # Initialize the output grid (e.g., with zeros or copy input - doesn't matter as it will be overwritten)
    # Starting with 6s simplifies the logic slightly, as it's the default fill.
    output_array = np.full_like(input_array, 6) 
    
    # Define the starting coordinates for the four quadrants
    quadrants = [
        (0, 0),  # Top-left
        (0, 2),  # Top-right
        (2, 0),  # Bottom-left
        (2, 2)   # Bottom-right
    ]

    # Iterate through each quadrant
    for row_start, col_start in quadrants:
        # Check if '2' is present in the current input quadrant
        if _check_quadrant_for_value(input_array, row_start, col_start, 2):
            # If '2' is present, fill the corresponding output quadrant with '2'
            _fill_quadrant(output_array, row_start, col_start, 2)
        # else: 
            # If '2' is not present, the output quadrant is already filled with '6' (from initialization)
            # _fill_quadrant(output_array, row_start, col_start, 6) # This line is redundant if initialized with 6

    # Convert the final NumPy output array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid