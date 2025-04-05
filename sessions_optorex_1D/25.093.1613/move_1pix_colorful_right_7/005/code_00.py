import numpy as np
# from skimage import measure # Example import

"""
Transforms an input grid (1xN NumPy array) by shifting the elements in its 
single row one position to the right, inserting a 0 at the beginning of the 
row, and discarding the last element of the original row.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the right-shift transformation to the single row of the input grid.

    Args:
        input_grid: A 2D NumPy array with shape (1, N) containing integers.

    Returns:
        A 2D NumPy array with shape (1, N) containing the transformed row.
    """
    # Extract the first (and only) row from the input grid.
    # This converts the 2D (1, N) array slice into a 1D (N,) array.
    input_row = input_grid[0]

    # Slice the input row to get all elements except the last one.
    # Example: if input_row is [0, 8, 5, ..., 8, 0], sliced_row is [0, 8, 5, ..., 8]
    sliced_row = input_row[:-1]

    # Create the new row by prepending a 0 to the sliced row.
    # Using numpy concatenation requires arrays, so create a 1-element array for 0.
    # Example: [0] concatenated with [0, 8, 5, ..., 8] becomes [0, 0, 8, 5, ..., 8]
    new_row_1d = np.concatenate(([0], sliced_row))

    # Reshape the resulting 1D array back into a 2D array with one row.
    # The shape should match the original input grid's shape.
    # Example: [0, 0, 8, ..., 8] becomes [[0, 0, 8, ..., 8]]
    output_grid = new_row_1d.reshape(1, -1) # -1 infers the number of columns

    return output_grid