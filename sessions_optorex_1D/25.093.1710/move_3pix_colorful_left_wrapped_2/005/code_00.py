import numpy as np

"""
Performs a left rotation by 3 positions on the single row of a 1x12 input grid.
The input is expected as a 2D NumPy array with shape (1, 12). The first 3 elements
of the row are moved to the end, and the remaining 9 elements shift to the left, 
maintaining their relative order. The output is also a 2D NumPy array with shape (1, 12).
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by rotating its single row left by 3 positions.

    Args:
        input_grid: A NumPy array of shape (1, 12) containing integers.

    Returns:
        A NumPy array of shape (1, 12) representing the transformed grid.
    """

    # Verify input shape (optional but helps catch unexpected inputs)
    if input_grid.shape != (1, 12):
         # Handle error or try to adapt if possible. 
         # For now, assume the shape is correct based on prior analysis.
         # If the shape was (12,), we might reshape: input_grid = input_grid.reshape(1, 12)
         # If it's completely different, raising an error is appropriate.
         # Based on the previous errors, the input IS (1, 12), so this check might not be strictly needed 
         # unless we want robustness against future changes.
         # Let's proceed assuming the input is (1, 12) as diagnosed.
         pass # Or raise ValueError(f"Expected shape (1, 12), got {input_grid.shape}")

    # Extract the single row from the input grid
    # input_grid[0] selects the first (and only) row, resulting in a 1D array of shape (12,)
    input_row = input_grid[0]

    # Identify the first 3 elements of the row
    first_part = input_row[:3]

    # Identify the remaining 9 elements (from index 3 onwards)
    second_part = input_row[3:]

    # Construct the rotated row by concatenating the second part followed by the first part
    # np.concatenate takes a tuple or list of arrays to join
    rotated_row = np.concatenate((second_part, first_part))

    # Reshape the 1D rotated row back into a 2D grid of shape (1, 12)
    # reshape(1, -1) creates 1 row and infers the number of columns needed (which will be 12)
    output_grid = rotated_row.reshape(1, 12)

    # Return the transformed grid
    return output_grid