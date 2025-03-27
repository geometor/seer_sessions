"""
Identify all non-white pixels in the input grid. Determine the coordinates 
(row and column indices) of the top-leftmost position occupied by any of 
these non-white pixels (minimum row index `min_row` and minimum column index 
`min_col`). Extract a 3x3 subgrid from the input grid starting at the 
determined top-left coordinate (`min_row`, `min_col`). This extracted 3x3 
subgrid is the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts a 3x3 subgrid from the input grid based on the top-leftmost 
    non-white pixel.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The 3x3 extracted subgrid.
    """
    # Convert input to a numpy array for efficient operations
    grid = np.array(input_grid, dtype=int)

    # Find the coordinates (row, column) of all non-white pixels (value != 0)
    non_white_pixels = np.where(grid != 0)

    # Check if any non-white pixels were found
    if non_white_pixels[0].size == 0:
        # Handle the case where the grid is all white (return an empty 3x3 grid or based on specific rules if needed)
        # For this task, based on examples, we assume non-white pixels exist.
        # If not, returning a 3x3 white grid might be a safe default, but let's stick to the observed pattern.
        # If this case occurs in test, we might need refinement.
        # Let's raise an error for now to highlight unexpected input.
         raise ValueError("Input grid contains no non-white pixels.")


    # Determine the minimum row index (topmost) among non-white pixels
    min_row = np.min(non_white_pixels[0])

    # Determine the minimum column index (leftmost) among non-white pixels
    min_col = np.min(non_white_pixels[1])

    # Extract the 3x3 subgrid starting from (min_row, min_col)
    # Slicing automatically handles boundaries if the extraction goes out of bounds,
    # but ARC constraints (max 30x30) and the logic usually prevent this.
    # However, let's ensure the slice dimensions are correct.
    output_grid = grid[min_row:min_row + 3, min_col:min_col + 3]

    # Ensure the output is exactly 3x3, padding with 0 if extraction is near edges
    # (Though based on examples, this might not be needed as the patterns seem sufficiently away from edges)
    # Let's keep the direct slice for now as it matches the examples perfectly.

    return output_grid.tolist() # Return as list of lists to match expected format