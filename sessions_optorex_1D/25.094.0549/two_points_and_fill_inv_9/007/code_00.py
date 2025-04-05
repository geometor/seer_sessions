"""
Modifies a 2D grid (NumPy array) of integers by altering horizontal sequences 
of identical non-zero digits within each row. If a contiguous horizontal 
sequence of an identical non-zero digit has a length of 3 or more, its 
internal elements (all except the first and last elements of the sequence) 
are replaced with 0. Sequences of length 1 or 2 remain unchanged. '0' 
digits act as separators and are not part of sequences.
"""

import numpy as np
import copy

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D NumPy array of integers.

    Returns:
        A new 2D NumPy array with the transformation applied.
    """
    # Ensure input is a NumPy array
    if not isinstance(input_grid, np.ndarray):
        try:
            input_grid = np.array(input_grid)
        except Exception as e:
            raise TypeError(f"Input could not be converted to a NumPy array: {e}")

    # Check if the input is 2D
    if input_grid.ndim != 2:
        # Handle potential 1D input from previous errors by reshaping
        if input_grid.ndim == 1:
             # Check if it looks like a flattened single row example
             # This is a heuristic based on typical ARC task sizes.
             # Adjust threshold if necessary.
             if input_grid.shape[0] < 50: 
                 input_grid = input_grid.reshape(1, -1) 
             else:
                 raise ValueError("Input is 1D and doesn't look like a single row grid.")
        else:
             raise ValueError(f"Input grid must be 2D, but got {input_grid.ndim} dimensions.")


    # Initialize output_grid as a deep copy of the input grid
    # This ensures the original input is unchanged and we modify the copy.
    output_grid = copy.deepcopy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row of the grid
    for r in range(rows):
        c = 0 # Initialize column index for the current row
        # Iterate through the columns of the current row to find sequences
        while c < cols:
            current_val = input_grid[r, c]

            # Check if the current element is non-zero (potential start of a sequence)
            if current_val != 0:
                start_col = c
                
                # Find the end of the contiguous sequence of the same non-zero value
                # Move 'c' forward as long as we are within bounds and the value matches
                while c + 1 < cols and input_grid[r, c + 1] == current_val:
                    c += 1
                
                # The sequence ends at the current column index 'c'
                end_col = c 
                # Calculate the length of the sequence
                length = end_col - start_col + 1

                # Apply the transformation rule based on sequence length
                # If the sequence length is 3 or more, modify the output grid
                if length >= 3:
                    # Iterate through the internal elements of the sequence 
                    # (indices from start_col + 1 up to, but not including, end_col + 1, which is end_col)
                    # and set them to 0 in the output grid for the current row.
                    for k in range(start_col + 1, end_col):
                        output_grid[r, k] = 0
                
                # Move the column index past the currently processed sequence
                c += 1 
            else:
                # If the current element is 0, just move to the next column
                c += 1

    # Return the modified grid
    return output_grid