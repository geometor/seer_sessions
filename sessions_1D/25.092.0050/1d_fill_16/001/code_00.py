import numpy as np
from typing import List, Tuple

"""
Transformation Rule:
Identify the two non-white pixels in the input row grid. Verify they have the 
same color. Fill the segment of the grid between and including these two pixels 
with their color. Leave the rest of the grid white (0).
"""

def find_non_white_pixels(grid: np.ndarray) -> List[Tuple[int, int, int]]:
    """
    Finds all non-white pixels (value != 0) in a 1D grid (represented as 1xN).

    Args:
        grid: A numpy array representing the input grid (assumed 1xN).

    Returns:
        A list of tuples, where each tuple contains (row_index, col_index, color).
        Since it's 1xN, row_index will always be 0.
    """
    non_white_pixels = []
    # Find indices where the value is not 0
    indices = np.where(grid != 0)
    # `indices` is a tuple of arrays (one for each dimension)
    if len(indices[0]) > 0: # Check if any non-white pixels were found
        row_indices = indices[0]
        col_indices = indices[1]
        for r, c in zip(row_indices, col_indices):
            color = grid[r, c]
            non_white_pixels.append((r, c, color))
    return non_white_pixels

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid according to the rule: fill the segment between
    two identical non-white pixels with their color.

    Args:
        input_grid: A numpy array representing the 1xN input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    
    # 1. Find non-white pixels
    non_white_info = find_non_white_pixels(input_grid)

    # 2. Validate assumptions (exactly two, same color)
    if len(non_white_info) != 2:
        # Handle error or unexpected input - returning input for now
        # Or raise ValueError("Expected exactly two non-white pixels.")
        print(f"Warning: Expected 2 non-white pixels, found {len(non_white_info)}. Returning input.")
        return input_grid.copy() 

    (r1, c1, color1) = non_white_info[0]
    (r2, c2, color2) = non_white_info[1]

    if color1 != color2:
        # Handle error or unexpected input - returning input for now
        # Or raise ValueError("Expected the two non-white pixels to have the same color.")
        print(f"Warning: Non-white pixels have different colors ({color1}, {color2}). Returning input.")
        return input_grid.copy()

    # 3. Determine the segment boundaries
    fill_color = color1
    start_col = min(c1, c2)
    end_col = max(c1, c2)
    row_idx = r1 # Since it's 1xN, row index is the same (0)

    # 4. Initialize output grid (same shape, filled with background color 0)
    output_grid = np.zeros_like(input_grid)

    # 5. Fill the segment in the output grid
    # Use slicing to set the values from start_col to end_col (inclusive)
    output_grid[row_idx, start_col:end_col + 1] = fill_color

    # 6. Return the modified output grid
    return output_grid
