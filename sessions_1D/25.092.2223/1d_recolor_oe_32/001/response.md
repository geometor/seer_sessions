```python
import numpy as np
import math

"""
Processes a 1D input grid (represented as a list or 1D numpy array).
Identifies contiguous horizontal blocks of yellow pixels (value 4).
If a block's length is even, all pixels in that block are changed to maroon (9) in the output.
If a block's length is odd, all pixels in that block are changed to azure (8) in the output.
White pixels (value 0) remain unchanged.
"""

def find_contiguous_blocks(grid_row, target_color):
    """
    Finds contiguous blocks of a specific color in a 1D list.

    Args:
        grid_row: A list of integers representing a row of the grid.
        target_color: The integer value of the color to find blocks of.

    Returns:
        A list of tuples, where each tuple contains (start_index, end_index, length)
        for a found block.
    """
    blocks = []
    n = len(grid_row)
    i = 0
    while i < n:
        if grid_row[i] == target_color:
            start_index = i
            # Find the end of the block
            while i < n and grid_row[i] == target_color:
                i += 1
            end_index = i - 1
            length = end_index - start_index + 1
            blocks.append((start_index, end_index, length))
        else:
            i += 1
    return blocks

def transform(input_grid):
    """
    Transforms the input grid based on the lengths of contiguous yellow blocks.

    Args:
        input_grid: A list of lists or numpy array representing the input grid.
                    Expected to be 1xN for this specific task based on examples.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Convert input to numpy array for easier handling, assuming it might be list of lists
    input_array = np.array(input_grid, dtype=int)

    # Ensure it's effectively 1D as per the examples
    if input_array.shape[0] != 1:
         # Handle potential multi-row case if needed in future, or raise error
         # For now, assume first row if multiple exist, or error if not 1xN
         if input_array.ndim == 1: # If it's already a flat list passed in
              input_row = input_array
         else:
              # This case shouldn't happen based on task description/examples
              # If it does, we might need clarification. Let's assume first row for now.
              # print("Warning: Input grid has multiple rows, processing only the first.")
              input_row = input_array[0]
    else:
        input_row = input_array[0] # Get the single row

    # Initialize output_grid as a copy of the input row
    output_row = input_row.copy()

    # Define colors
    yellow = 4
    maroon = 9
    azure = 8

    # Find all contiguous blocks of yellow
    yellow_blocks = find_contiguous_blocks(input_row, yellow)

    # Process each yellow block
    for start, end, length in yellow_blocks:
        # Determine the replacement color based on length parity
        if length % 2 == 0:  # Even length
            replacement_color = maroon
        else:  # Odd length
            replacement_color = azure

        # Update the output row in the block's range
        output_row[start : end + 1] = replacement_color

    # Reshape the output row back into a 2D array (1xN)
    output_grid = output_row.reshape(1, -1)

    return output_grid.tolist() # Return as list of lists as per ARC standard

```