```python
"""
Transforms a single-row grid by identifying a contiguous segment of non-white pixels 
and keeping only the start and end pixels of that segment, turning the pixels in between white. 
The surrounding white pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): A single-row grid represented as a list containing one list of integers.

    Returns:
        list of lists: The transformed single-row grid.
    """

    # Ensure input is treated as a 1D array (the single row)
    # Use numpy for efficient array operations
    input_row = np.array(input_grid[0])
    
    # Initialize the output row with the same shape, filled with white (0)
    output_row = np.zeros_like(input_row) 

    # Find the column indices of all non-white (non-zero) pixels
    non_white_indices = np.where(input_row != 0)[0]

    # Check if there are any non-white pixels
    if len(non_white_indices) > 0:
        # Identify the start index (first non-white pixel)
        start_index = non_white_indices[0]
        # Identify the end index (last non-white pixel)
        end_index = non_white_indices[-1]
        
        # Get the color of the segment from the input grid (using the start index)
        segment_color = input_row[start_index]

        # Place the segment's color at the start index in the output grid
        output_row[start_index] = segment_color
        
        # Place the segment's color at the end index in the output grid
        # This handles segments of length 1 correctly (start_index == end_index)
        # and segments of length > 1.
        output_row[end_index] = segment_color
        
    # If there were no non-white pixels, the output_row remains all white (0), 
    # which is the correct transformation in that case.

    # Convert the numpy row back to the required list-of-lists format
    output_grid = [output_row.tolist()]
    
    return output_grid

```