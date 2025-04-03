import numpy as np
import math
from collections import Counter

"""
Transforms a 1xN input grid (NumPy array) based on contiguous sequences of non-zero colors (objects) within the single row.

- Objects are defined as contiguous sequences of identical non-zero pixels within the row. In the training examples, observed object lengths are 1 or 3.
- The background color is 0 (white), forming gaps between objects.
- The transformation rules are applied sequentially from left to right:
    1. If an object has a length of 3, it remains unchanged in the output, and the gap of zeros immediately preceding it also remains unchanged.
    2. If an object has a length of 1 (a single pixel), it is expanded in the output to a length of 3 (by repeating its color).
    3. The gap of zeros immediately preceding a single-pixel object is reduced in length in the output. The amount of reduction is equal to the cumulative count of single-pixel objects encountered *so far* (including the current one). The gap length cannot become negative (minimum length is 0).
    4. Trailing zeros after the last object are preserved.
"""

def _find_next_object_length(grid, start_col):
    """Helper function to find the length of the next non-zero object."""
    rows, cols = grid.shape
    
    # Find the start of the next non-zero sequence
    obj_col = start_col
    while obj_col < cols and grid[0, obj_col] == 0:
        obj_col += 1

    # If we reached the end looking for the start, there's no object
    if obj_col >= cols:
        return 0 

    # Found the start, now find the end
    object_color = grid[0, obj_col]
    object_start = obj_col
    while obj_col < cols and grid[0, obj_col] == object_color:
        obj_col += 1
        
    return obj_col - object_start


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (np.ndarray): A 2D NumPy array of shape (1, N) representing the input row.

    Returns:
        np.ndarray: A 2D NumPy array of shape (1, M) representing the transformed row,
                    where M might differ from N due to object expansion and gap reduction.
    """
    
    # Ensure input is a 2D numpy array
    if not isinstance(input_grid, np.ndarray) or input_grid.ndim != 2 or input_grid.shape[0] != 1:
         raise ValueError("Input must be a 2D NumPy array with exactly one row.")

    output_row_pixels = []
    single_pixel_count = 0
    j = 0 # Current column index in the input grid
    rows, N = input_grid.shape # N is the number of columns

    while j < N:
        # Record the start of the current segment
        start_j = j
        current_pixel = input_grid[0, j]

        # --- Process a Gap (sequence of zeros) ---
        if current_pixel == 0:
            # Find the end of the gap
            while j < N and input_grid[0, j] == 0:
                j += 1
            gap_length = j - start_j

            # Look ahead to determine the length of the next object (if any)
            # This determines if the gap needs reduction
            next_object_length = 0
            if j < N: # Check if we are not at the end of the grid
                 next_object_length = _find_next_object_length(input_grid, j)

            # Apply gap reduction rule if the next object is a single pixel
            if next_object_length == 1:
                reduction = single_pixel_count + 1 # Reduction depends on count *before* processing the object
                new_gap_length = max(0, gap_length - reduction)
                output_row_pixels.extend([0] * new_gap_length)
            else:
                # Keep original gap length if next object is length 3, >3, or if it's a trailing gap
                output_row_pixels.extend([0] * gap_length)

        # --- Process an Object (sequence of non-zeros) ---
        else:
            object_color = current_pixel
            # Find the end of the object
            while j < N and input_grid[0, j] == object_color:
                j += 1
            object_length = j - start_j

            # Apply object transformation rule
            if object_length == 1:
                single_pixel_count += 1 # Increment count *after* identifying the single pixel
                output_row_pixels.extend([object_color] * 3) # Expand to length 3
            elif object_length == 3:
                output_row_pixels.extend([object_color] * 3) # Keep as length 3
            else:
                # Handle unexpected object lengths (e.g., length 2 or >3) - append as is
                # Based on examples, only 1 and 3 are expected, but this is safer.
                 output_row_pixels.extend(input_grid[0, start_j:j].tolist())

    # Convert the list of output pixels into the final NumPy array format
    if not output_row_pixels: # Handle empty input case
        output_grid = np.empty((1, 0), dtype=int)
    else:
        output_grid = np.array([output_row_pixels], dtype=int)
        
    return output_grid