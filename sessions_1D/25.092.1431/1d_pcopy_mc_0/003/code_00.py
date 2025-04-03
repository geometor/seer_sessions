"""
Transforms a 1xN grid (represented as a 2D NumPy array) by modifying contiguous 
segments of non-zero pixels ("objects") based on their length.
Segments of length 1 are expanded to length 3 using the same color.
Segments of length greater than 1 remain unchanged.
Zero pixels (background) remain unchanged.
The output grid will have shape 1xM, where M might differ from N.
"""

import numpy as np
from typing import List

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 1xN NumPy array representing the input sequence.

    Returns:
        A 1xM NumPy array representing the transformed sequence.
    """
    
    # Ensure input is a 2D numpy array, even if visually 1D
    if input_grid.ndim == 1:
        # If somehow it's 1D, reshape to 1xN
        input_row = input_grid
    elif input_grid.shape[0] == 1:
        # Extract the first row if it's 1xN
        input_row = input_grid[0]
    else:
        # Handle unexpected shapes (e.g., raise error or return input)
        # For this task, we strictly expect 1xN based on examples
        raise ValueError("Input grid must have shape 1xN")

    output_row_list = []
    i = 0
    n = len(input_row)

    # Iterate through the input row sequence
    while i < n:
        # Get the current pixel's color
        current_pixel = input_row[i]

        # If the pixel is white (0), copy it directly
        if current_pixel == 0:
            output_row_list.append(0)
            i += 1 # Move to the next pixel
        else:
            # If the pixel is non-white, identify the object
            object_color = current_pixel
            object_length = 0
            start_index = i
            
            # Find the length of the contiguous non-white object
            # Scan forward while we are within bounds and the color matches
            while i < n and input_row[i] == object_color:
                object_length += 1
                i += 1 # Advance index past the object pixels within this inner loop
            
            # Apply transformation based on object length
            if object_length == 1:
                # Expand single-pixel object to three pixels
                output_row_list.extend([object_color] * 3)
            else:
                # Copy multi-pixel object as is
                # We already know the color and length
                output_row_list.extend([object_color] * object_length)
                
            # Note: Index 'i' is already advanced past the object by the inner while loop,
            # so the outer loop will continue from the correct position.

    # Convert the resulting list into a 1xM NumPy array
    # Ensure it's at least 2D with shape (1, M)
    output_grid = np.array([output_row_list], dtype=input_grid.dtype)

    return output_grid