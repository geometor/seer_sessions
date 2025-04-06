"""
Transforms an input grid by propagating the last seen non-zero value downwards within each column. 
Zeros below a non-zero number in a column are replaced by that number until another non-zero number is encountered in that column, or the bottom of the column is reached.
"""

import numpy as np
import copy # Keep copy for potential list input, though numpy is preferred

# Helper function concept (though simple enough to inline for this task)
# def get_grid_dimensions(grid):
#     if isinstance(grid, np.ndarray):
#         return grid.shape
#     elif isinstance(grid, list) and grid:
#         return len(grid), len(grid[0])
#     else:
#         return 0, 0

def transform(input_grid):
    """
    Applies the downward propagation transformation to the input grid.

    Args:
        input_grid: A 2D list or NumPy array representing the input grid of integers.

    Returns:
        A 2D NumPy array representing the transformed grid.
    """
    # Ensure input is a NumPy array for consistent handling
    if not isinstance(input_grid, np.ndarray):
        # Attempt conversion, handle potential errors if input is malformed
        try:
            input_np = np.array(input_grid, dtype=int)
        except ValueError:
            # Handle cases like empty lists or lists of lists with inconsistent lengths
            if not input_grid or not input_grid[0]:
                 return np.array([], dtype=int) # Or handle as error
            # If conversion fails for other reasons, re-raise or return error state
            raise ValueError("Input grid could not be converted to a NumPy array.")
    else:
        input_np = input_grid

    # Check for empty input after potential conversion
    if input_np.size == 0:
        return np.array([], dtype=int) # Return empty array for empty input

    # Get grid dimensions
    height, width = input_np.shape

    # Initialize output_grid as a copy of the input numpy array
    output_grid = input_np.copy()

    # Iterate through each column
    for c in range(width):
        # Initialize the last non-zero value seen in this column
        last_non_zero_value = 0

        # Iterate through each row within the current column, from top to bottom
        for r in range(height):
            # Get the value from the original input grid for reference
            input_value = input_np[r, c]

            # If the input value is non-zero, update the last seen non-zero value
            # The output_grid already has this value from the copy.
            if input_value != 0:
                last_non_zero_value = input_value
            # If the input value is zero AND we have previously seen a non-zero value in this column
            elif last_non_zero_value != 0:
                # Update the corresponding cell in the output grid with the last non-zero value
                output_grid[r, c] = last_non_zero_value
            # If the input value is zero and no non-zero value has been seen yet,
            # the output_grid cell retains its original zero value from the copy.

    # Return the fully transformed grid as a NumPy array
    return output_grid