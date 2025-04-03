```python
import numpy as np

"""
Shift a contiguous block of non-white pixels one position to the right within a single row.

1. Identify the single contiguous block of non-white pixels in the input row.
2. Note its color (C) and its starting and ending indices (start_index, end_index).
3. Create a new row (output_grid) initialized as a copy of the input row.
4. Change the pixel value at start_index in the output_grid to white (0).
5. Change the pixel value at end_index + 1 in the output_grid to the color C.
6. Return the output_grid.
"""

def find_non_white_block(row):
    """Finds the start index, end index, and color of a contiguous non-white block."""
    start_index = -1
    end_index = -1
    color = 0
    for i, pixel in enumerate(row):
        if pixel != 0:
            if start_index == -1:
                start_index = i
                color = pixel
            end_index = i
        elif start_index != -1: # Found the end of the block
            break
    return start_index, end_index, color

def transform(input_grid):
    """
    Transforms the input grid by shifting the non-white block one step to the right.

    Args:
        input_grid (list or np.array): A 1D list or array representing the input row.

    Returns:
        np.array: A 1D numpy array representing the transformed row.
    """
    # Ensure input is a numpy array for easier manipulation
    input_row = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = input_row.copy()

    # Find the non-white block
    start_index, end_index, color = find_non_white_block(input_row)

    # Check if a block was found
    if start_index != -1:
        # Change the original start position to white
        output_grid[start_index] = 0
        
        # Check if the shift is within bounds before changing the new end position
        if end_index + 1 < len(output_grid):
             # Change the pixel to the right of the original block to the block's color
            output_grid[end_index + 1] = color
        # else: the block hits the right edge, part of it disappears - this case isn't shown in examples but handled defensively.
        # In the provided examples, there's always space to shift right.

    return output_grid.tolist() # Return as list as per original format if needed, or np.array
```