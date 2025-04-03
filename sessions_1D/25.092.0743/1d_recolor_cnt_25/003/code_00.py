"""
Transforms a 1-row grid by changing the color of contiguous horizontal runs of yellow (4) pixels based on their length. Runs of length 1 become azure (8), length 2 become red (2), and length 3 become magenta (6). White (0) pixels remain unchanged. The input and output are 2D NumPy arrays.
"""

import numpy as np

def find_runs(row, target_color):
    """
    Finds contiguous runs of a target color in a 1D array (row).

    Args:
        row (np.array): The 1D array representing the grid row.
        target_color (int): The color value to find runs of.

    Yields:
        tuple: A tuple (start_index, end_index, run_length) for each found run.
               end_index is exclusive (suitable for slicing).
    """
    n = len(row)
    i = 0
    while i < n:
        if row[i] == target_color:
            j = i
            # Find the end of the contiguous run
            while j < n and row[j] == target_color:
                j += 1
            run_length = j - i
            yield i, j, run_length
            # Move index past the current run
            i = j
        else:
            # Move to the next pixel if not the target color
            i += 1

def transform(input_grid):
    """
    Applies a color transformation to runs of yellow pixels in a 1-row grid based on run length.

    Args:
        input_grid (np.array): A 2D NumPy array representing the input grid (expected 1xN).

    Returns:
        np.array: A 2D NumPy array representing the transformed output grid.
    """
    # Ensure the input is a NumPy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Verify input is 1 row (or handle appropriately if needed, for now assume 1 row)
    if input_grid.shape[0] != 1:
         # Handle error or adapt logic if multiple rows are possible
         # For this specific task based on examples, assume 1 row.
         # If it might receive 1D array, reshape it.
         if len(input_grid.shape) == 1:
             input_grid = input_grid.reshape(1, -1)
         else:
              # If more than 1 row and unsure how to handle, maybe return input or raise error
              print(f"Warning: Input grid has {input_grid.shape[0]} rows, expected 1. Processing only the first row.")
              # Or raise ValueError("Input grid must have exactly one row for this transformation.")


    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Define the mapping from run length to output color
    length_to_color = {
        1: 8,  # azure
        2: 2,  # red
        3: 6   # magenta
    }
    target_color = 4 # yellow

    # Process the first row
    first_row = output_grid[0]

    # Iterate through the identified runs of the target color
    for start_index, end_index, run_length in find_runs(first_row, target_color):
        # Determine the replacement color based on the run length
        # Default to the original target color if length is not in the map
        replacement_color = length_to_color.get(run_length, target_color)

        # Apply the transformation to the output grid slice for the current run
        first_row[start_index:end_index] = replacement_color

    # The modifications were made in place on the first_row, which is a view of output_grid[0]
    # So, output_grid is already updated.

    return output_grid